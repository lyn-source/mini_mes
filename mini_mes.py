import requests
import time
from bioreactor import Bioreactor
from valve import Valve

BASE_URL = "http://mini-mes.resilience.com"

def run_batch():
    """Return True if the batch run was successful.  Otherwise, return
    False.
    """

    fill_percent = 70  # percent
    fill_tolerance = 2 # percent
    max_pressure = 200     # kPa
    pressure_tolerance = 0 # kPa
    max_temperature = 80      # deg C
    temperature_tolerance = 1 # deg C
    bioreactor1.set_limits(fill_percent,
                           fill_tolerance,
                           max_pressure,
                           pressure_tolerance,
                           max_temperature,
                           temperature_tolerance)

    print("Input valve name is ", bioreactor1.input_valve.name)
    print("Output valve name is ", bioreactor1.output_valve.name)

    # assume close the output valve when starting
    if not bioreactor1.output_valve.set_valve("closed"): 
        return False

    if not bioreactor1.input_valve.set_valve("open"):
        return False

    sample_seconds = 5
    if not bioreactor1.fill(sample_seconds):
        return False
    elif not bioreactor1.input_valve.set_valve("closed"):
        return False

    if bioreactor1.process_batch(sample_seconds):
        return bioreactor1.output_valve.set_valve("open")
    else:
        return False
            

if __name__ == "__main__":
    
    bioreactor1 = Bioreactor(BASE_URL)
    print("Bioreactor1 id: ", bioreactor1.id)
    start_time = time.time()
    success = run_batch()
    end_time = time.time()
    print("Batch was {}.  Elapsed time {} seconds.".format(
          "successful" if success else "unsuccessful",
          end_time - start_time))
    bioreactor1.print_report()
