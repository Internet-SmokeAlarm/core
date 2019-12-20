from abc import abstractmethod

class RequestProcessor:

    def _is_string_name_valid(self, string_name):
        """
        :param string_name: string
        :return: boolean
        """
        return string_name is not None and type(string_name) == type("string")
