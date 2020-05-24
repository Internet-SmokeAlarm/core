from abc import abstractmethod


class RequestProcessor:

    def _is_string_name_valid(self, string_name):
        """
        :param string_name: string
        :return: boolean
        """
        return string_name is not None and isinstance(
            string_name, type("string"))

    def _is_int_name_valid(self, int_name):
        """
        :param int_name: string
        :return: boolean
        """
        return int_name is not None and isinstance(int_name, type(0))
