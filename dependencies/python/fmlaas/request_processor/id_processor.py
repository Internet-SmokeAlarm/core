from .request_processor import RequestProcessor

class IDProcessor(RequestProcessor):

    GROUP_NAME_KEY = "group_name"
    GROUP_ID_KEY = "group_id"
    ROUND_ID_KEY = "round_id"
    DEVICE_ID_KEY = "device_id"

    def __init__(self, json):
        self.json = json

    def get_group_name(self):
        group_name = self.json.get(IDProcessor.GROUP_NAME_KEY, None)

        if not self._is_string_name_valid(group_name):
            raise ValueError("Group name invalid.")

        return group_name

    def get_group_id(self):
        """
        :return: string
        """
        group_id = self.json.get(IDProcessor.GROUP_ID_KEY, None)

        if not self._is_string_name_valid(group_id):
            raise ValueError("Group id invalid.")

        return group_id

    def get_round_id(self):
        """
        :return: string
        """
        round_id = self.json.get(IDProcessor.ROUND_ID_KEY, None)

        if not self._is_string_name_valid(round_id):
            raise ValueError("Round id invalid.")

        return round_id

    def get_device_id(self):
        """
        :return: string
        """
        device_id = self.json.get(IDProcessor.DEVICE_ID_KEY, None)

        if not self._is_string_name_valid(device_id):
            raise ValueError("Device id invalid.")

        return device_id
