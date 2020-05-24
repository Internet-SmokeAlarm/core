from .request_processor import RequestProcessor

class IDProcessor(RequestProcessor):

    GROUP_NAME_KEY = "group_name"
    GROUP_ID_KEY = "group_id"
    ROUND_ID_KEY = "job_id"
    DEVICE_ID_KEY = "device_id"
    PREVIOUS_ROUND_ID_KEY = "previous_job_id"

    def __init__(self, json):
        self.json = json

    def get_group_name(self, throw_exception=True):
        group_name = self.json.get(IDProcessor.GROUP_NAME_KEY, None)

        if not self._is_string_name_valid(group_name) and throw_exception:
            raise ValueError("Group name invalid.")

        return group_name

    def get_group_id(self, throw_exception=True):
        """
        :return: string
        """
        group_id = self.json.get(IDProcessor.GROUP_ID_KEY, None)

        if not self._is_string_name_valid(group_id) and throw_exception:
            raise ValueError("Group id invalid.")

        return group_id

    def get_job_id(self, throw_exception=True):
        """
        :return: string
        """
        job_id = self.json.get(IDProcessor.ROUND_ID_KEY, None)

        if not self._is_string_name_valid(job_id) and throw_exception:
            raise ValueError("Job id invalid.")

        return job_id

    def get_previous_job_id(self, throw_exception=True):
        """
        :return: string
        """
        job_id = self.json.get(IDProcessor.PREVIOUS_ROUND_ID_KEY, None)

        if not self._is_string_name_valid(job_id) and throw_exception:
            raise ValueError("Previous job id invalid.")

        return job_id

    def get_device_id(self, throw_exception=True):
        """
        :return: string
        """
        device_id = self.json.get(IDProcessor.DEVICE_ID_KEY, None)

        if not self._is_string_name_valid(device_id) and throw_exception:
            raise ValueError("Device id invalid.")

        return device_id
