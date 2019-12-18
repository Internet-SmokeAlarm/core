from abc import abstractmethod

class RequestProcessor:

    @abstractmethod
    def get_group_name(self):
        """
        :return: string
        """
        raise NotImplementedError("get_group_name() not implemented")

    @abstractmethod
    def get_group_id(self):
        """
        :return: string
        """
        raise NotImplementedError("get_group_id() not implemented")

    @abstractmethod
    def get_round_id(self):
        """
        :return: string
        """
        raise NotImplementedError("get_round_id() not implemented")

    @abstractmethod
    def get_device_id(self):
        """
        :return: string
        """
        raise NotImplementedError("get_device_id() not implemented")
