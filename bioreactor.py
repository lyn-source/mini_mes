import time
import sys

from rest_hacks import rest_get_json
from valve import Valve

class Bioreactor:

    def __init__(self, base_url):
        self.base_url = base_url
        self.id = self.get_id()

        # Initialize min/max parameter values
        self.temperature_min = sys.maxsize
        self.temperature_max = -sys.maxsize - 1
        self.pH_min = sys.maxsize
        self.pH_max = -sys.maxsize - 1
        self.pressure_min = sys.maxsize
        self.pressure_max = -sys.maxsize - 1

        self.actual_fill_level = sys.maxsize
        self.fill_met_level = False

        self.input_valve = Valve("input", self.id, base_url)
        self.output_valve = Valve("output", self.id, base_url)
        
        
    def continue_process(self, current):
        """Return True if the vessel should continue to process.  Otherwise,
        return False.
        """
        
        return current["temperature"] < self.min_temperature_limit \
            and not (current["temperature"] > self.max_temperature_limit) \
            and current["pressure"] < self.pressure_limit

        
    def fill(self, sample_seconds):
        """Fill the vessel.

        Return True if filled properly.  Otherwise, return False.

        Parameter sample_seconds is the period (seconds) for sampling
        the vessel temp, pressure, pH.

        """
        current_state = self.get_vessel_state()
        self.log_vessel_state(current_state)

        # Consider a timeout or max tries.
        while current_state["fill_percent"] < self.min_fill_limit:
            time.sleep(sample_seconds)
            current_state = self.get_vessel_state()
            self.log_vessel_state(current_state)

        # Cache the vessel level now that filling is done.
        self.actual_fill_level = current_state["fill_percent"]
        self.fill_met_level = \
            self.actual_fill_level >= self.min_fill_limit \
            and self.actual_fill_level <= self.max_fill_limit

        return self.fill_met_level

    def get_id(self):
        """Get the id of the bioreactor."""

        url = self.base_url + "/bioreactor/0"
        response = rest_get_json(url)
        id = None
        try:
            id = response["id"]
        except KeyError:
            pass # log message

        return id

    def get_vessel_state(self):
        """Get state of the bioreactor's vessel.
        State includes the fill level (%), pH, pressure (kPa), Temp deg C.
        """

        url = self.base_url + "/bioreactor/" + self.id
        return rest_get_json(url)

    def log_vessel_state(self, current):
        """Track the range of the vessel state parameters."""

        self.temperature_min = min(self.temperature_min, current["temperature"])
        self.temperature_max = max(self.temperature_max, current["temperature"])
        self.pH_min = min(self.pH_min, current["pH"])
        self.pH_max = max(self.pH_max, current["pH"])
        self.pressure_min = min(self.pressure_min, current["pressure"])
        self.pressure_max = max(self.pressure_max, current["pressure"])

    def process_batch(self, sample):
        
        current_state = self.get_vessel_state()
        self.log_vessel_state(current_state)

        # Consider a timeout or max tries.
        while self.continue_process(current_state):
            time.sleep(sample_seconds)
            current_state = self.get_vessel_state()
            self.log_vessel_state(current_state)

        if current_state["pressure"] >= self.pressure_limit:
            # Abort message
            return False
        else:
            return True

    def print_report(self):
        """Print report from this batch record."""

        print("Actual fill level:", self.actual_fill_level)
        print("Temperature range: {} - {} deg C".format(
            self.temperature_min,
            self.temperature_max))
        print("pH range: {} - {}".format(
            self.pH_min,
            self.pH_max))
        print("Pressure range: {} - {} kPa".format(
            self.pressure_min,
            self.pressure_max))
        print("CPP for vessel fill level met:", self.fill_met_level)
        cpp_temp_met = self.temperature_max >= self.min_temperature_limit \
            and self.temperature_max <= self.max_temperature_limit
        print("CPP for maximum temperature met:", cpp_temp_met)
        print("CPP for pressure held below maximum met:",
              self.pressure_max < self.pressure_limit)


    def set_limits(self,
                   fill_percent,
                   fill_tolerance,
                   max_pressure,
                   pressure_tolerance,
                   max_temperature,
                   temperature_tolerance):
        """Set limits for the processing.

        Units are: 
        fill_percent (percent)
        fill_tolerance (percent)
        max_pressure (kPa)
        pressure_tolerance (kPa)
        temperature (deg C)
        temperature_tolerance (deg C)
        """
        
        self.min_fill_limit = fill_percent - fill_tolerance
        self.max_fill_limit = fill_percent + fill_tolerance
        self.min_temperature_limit = max_temperature - temperature_tolerance
        self.max_temperature_limit = max_temperature + temperature_tolerance
        self.pressure_limit = max_pressure - pressure_tolerance


        
