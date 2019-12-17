from .request_processor import RequestProcessor

class RequestJSONProcessor(RequestProcessor):

    GROUP_NAME_KEY = "group_name"

    def __init__(self, json):
        self.json = json

    def get_group_name(self):
        group_name = self.json.get(RequestJSONProcessor.GROUP_NAME_KEY, None)

        if not self._is_group_name_valid(group_name):
            raise ValueError("Group name invalid.")

        return group_name

    def _is_group_name_valid(self, group_name):
        """
        :param group_name: string
        """
        return group_name is not None and type(group_name) == type("string")
