from abc import abstractmethod

class RequestProcessor:

    def _is_string_name_valid(self, string_name):
        """
        :param string_name: string
        :return: boolean
        """
        return string_name is not None and type(string_name) == type("string")

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
