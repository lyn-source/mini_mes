from rest_hacks import rest_get_json, rest_put

class Valve:

    def __init__(self, name, vessel_id, base_url):
        self.name = name
        self.vessel_id = vessel_id
        self.base_url = base_url

    def set_valve(self, new_state):
        """Set the vessel valve to new_state.

        Return True if the new state is verified.  Otherwise, return
        False.

        """
        if new_state not in ["open", "closed"]:
            return False
        
        url = self.base_url + "/bioreactor/" + self.vessel_id
        value = self.name + " valve " + new_state
        rest_put(url, value)

        # Verify valve state
        new_state_verified = False
        response = rest_get_json(url)
        state = None
        try:
            state = response["state"]
            new_state_verified = (state == new_state)
        except KeyError:
            pass # log  message

        print("Valve {} new_state {} verified {}".format(
            self.name, new_state, new_state_verified))
        return new_state_verified

