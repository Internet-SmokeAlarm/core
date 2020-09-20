from .request_processor import RequestProcessor


class IDProcessor(RequestProcessor):

    PROJECT_NAME_KEY = "project_name"
    PROJECT_DESCRIPTION_KEY = "project_description"
    PROJECT_ID_KEY = "project_id"
    JOB_ID_KEY = "job_id"
    DEVICE_ID_KEY = "device_id"
    API_KEY_KEY = "api_key"
    EXPERIMENT_ID_KEY = "experiment_id"

    def __init__(self, json):
        self.json = json

    def get_project_name(self, throw_exception: bool = True) -> str:
        project_name = self.json.get(IDProcessor.PROJECT_NAME_KEY, None)

        if not self._is_string_name_valid(project_name) and throw_exception:
            raise ValueError("Project name invalid.")

        return project_name

    def get_project_id(self, throw_exception: bool = True) -> str:
        project_id = self.json.get(IDProcessor.PROJECT_ID_KEY, None)

        if not self._is_string_name_valid(project_id) and throw_exception:
            raise ValueError("Project id invalid.")

        return project_id

    def get_project_description(self, throw_exception: bool = True) -> str:
        project_description = self.json.get(IDProcessor.PROJECT_DESCRIPTION_KEY, None)

        if not self._is_string_name_valid(project_description) and throw_exception:
            raise ValueError("Project description invalid.")

        return project_description

    def get_experiment_id(self, throw_exception: bool = True) -> str:
        experiment_id = self.json.get(IDProcessor.EXPERIMENT_ID_KEY, None)

        if not self._is_string_name_valid(experiment_id) and throw_exception:
            raise ValueError("Experiment id invalid.")

        return experiment_id

    def get_job_id(self, throw_exception: bool = True) -> str:
        job_id = self.json.get(IDProcessor.JOB_ID_KEY, None)

        if not self._is_string_name_valid(job_id) and throw_exception:
            raise ValueError("Job id invalid.")

        return job_id

    def get_api_key(self, throw_exception: bool = True) -> str:
        api_key = self.json.get(IDProcessor.API_KEY_KEY, None)

        if not self._is_string_name_valid(api_key) and throw_exception:
            raise ValueError("Provided API key is invalid.")

        return api_key

    def get_device_id(self, throw_exception: bool = True) -> str:
        device_id = self.json.get(IDProcessor.DEVICE_ID_KEY, None)

        if not self._is_string_name_valid(device_id) and throw_exception:
            raise ValueError("Device id invalid.")

        return device_id
