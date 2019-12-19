class RoundConfiguration:

    def __init__(self, num_devices):
        self.num_devices = num_devices

    def get_num_devices(self):
        return self.num_devices

    def to_json(self):
        return {
            "num_devices" : self.num_devices
        }

    @staticmethod
    def from_json(json_data):
        return RoundConfiguration(json_data["num_devices"])
