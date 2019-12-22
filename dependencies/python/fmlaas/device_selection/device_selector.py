from abc import abstractmethod

class DeviceSelector:

    @abstractmethod
    def select_devices(self, devices, round_configuration):
        """
        :param devices: list(string)
        :param round_configuration: RoundConfiguration
        :return: list(string)
        """
        raise NotImplementedError("select_devices() not implemented")
