from .db_object import DBObject
from .model import Model


class JobSequence(DBObject):

    def __init__(self,
                 id,
                 jobs,
                 learning_parameters,
                 current_job,
                 start_model,
                 is_active):
        """
        :param id: string
        :param jobs: List(string)
        :param learning_parameters: dict(string : string)
        :param current_job: string
        :param start_model: json
        :param is_active: bool
        """
        self._id = id
        self._jobs = jobs
        self._learning_parameters = learning_parameters
        self._current_job = current_job
        self._start_model = start_model
        self._is_active = is_active

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        """
        :param value: string
        """
        self._id = value

    @property
    def jobs(self):
        return self._jobs

    @property
    def current_job(self):
        return self._current_job

    @current_job.setter
    def current_job(self, value):
        """
        :param value: string
        """
        self._current_job = value

    @property
    def start_model(self):
        return Model.from_json(self._start_model)

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        """
        :param value: bool
        """
        self._is_active = value

    @start_model.setter
    def start_model(self, value):
        """
        :param value: Model
        """
        self._start_model = value.to_json()

    @staticmethod
    def from_json(json_data):
        return JobSequence(json_data["ID"],
                           json_data["jobs"],
                           json_data["learning_parameters"],
                           json_data["current_job"],
                           json_data["start_model"],
                           json_data["is_active"])

    def to_json(self):
        return {
            "ID" : self._id,
            "jobs" : self._jobs,
            "learning_parameters" : self._learning_parameters,
            "current_job" : self._current_job,
            "start_model" : self._start_model,
            "is_active" : self._is_active
        }

    def proceed_to_next_job(self):
        for i in range(len(self.jobs) - 1):
            if self.current_job == self.jobs[i]:
                self.current_job = self.jobs[i + 1]
                return

        self.is_active = False

    def add_job(self, job):
        """
        :param job: Job
        """
        self._jobs.append(job.get_id())

        if self.current_job == "NONE" or not self.is_active:
            self.current_job = job.get_id()
            self.is_active = True

    def __eq__(self, other):
        return (self._id == other._id) and (self._jobs == other._jobs) and (self._learning_parameters == other._learning_parameters) and (self._current_job == other._current_job) and (self._start_model == other._start_model) and (self.is_active == other.is_active)
