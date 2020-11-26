from typing import Dict

from .job import Job
from .experiment_configuration import ExperimentConfiguration


class Experiment:

    def __init__(self,
                 id: str,
                 name: str,
                 description: str,
                 jobs: Dict[str, Job],
                 configuration: ExperimentConfiguration,
                 current_job_id: str):
        self._id = id
        self._name = name
        self._description = description
        self._jobs = jobs
        self._configuration = configuration
        self._current_job_id = current_job_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def jobs(self) -> Dict[str, Job]:
        return self._jobs
    
    @property
    def current_job(self) -> Job:
        if self._current_job_id not in self._jobs:
            return None
        
        return self._jobs[self._current_job_id]
    
    @property
    def configuration(self) -> ExperimentConfiguration:
        return self._configuration

    def contains_job(self, id: str) -> bool:
        return id in self._jobs

    def add_or_update_job(self, job: Job) -> None:
        job_exists = self.contains_job(job.id)
        self._jobs[job.id] = job
        
        if not job_exists:
            self.add_new_job(job)
        else:
            self.update_job(job)
    
    def add_new_job(self, job: Job) -> None:
        if self.current_job is None:
            self._current_job_id = job.id
            job.start_model = self._configuration.parameters

            self._jobs[job.id] = job
        elif self.current_job.is_complete():
            self.proceed_to_next_job()
    
    def update_job(self, job: Job) -> None:
        if self.current_job.id == job.id and (job.is_complete() or job.is_cancelled()):
            self.proceed_to_next_job()

    def proceed_to_next_job(self) -> None:
        next_job_id = str(int(self.current_job.id) + 1)

        if next_job_id in self._jobs:
            next_job = self._jobs[next_job_id]
            next_job.start_model = self.current_job.end_model

            self._current_job_id = next_job_id
    
    def handle_termination_check(self) -> None:
        """
        If the current job should be terminated, then this will terminate the job,
        and proceed to the next job.
        """
        current_job = self.current_job

        if current_job.should_terminate():
            current_job.cancel()

        self.add_or_update_job(current_job)

    
    def convert_jobs_to_json(self) -> Dict[str, dict]:
        converted_jobs = dict()
        for id, job in self._jobs.items():
            converted_jobs[id] = job.to_json()

        return converted_jobs
    
    @staticmethod
    def convert_json_to_jobs(json_data: Dict[str, dict]) -> Dict[str, Job]:
        converted_jobs = dict()
        for id, job in json_data.items():
            converted_jobs[id] = Job.from_json(job)

        return converted_jobs

    @staticmethod
    def from_json(json_data):
        return Experiment(json_data["ID"],
                          json_data["name"],
                          json_data["description"],
                          Experiment.convert_json_to_jobs(json_data["jobs"]),
                          ExperimentConfiguration.from_json(json_data["configuration"]),
                          json_data["current_job_id"])

    def to_json(self) -> dict:
        return {
            "ID": self._id,
            "name": self._name,
            "description": self._description,
            "jobs": self.convert_jobs_to_json(),
            "configuration": self._configuration.to_json(),
            "current_job_id": self._current_job_id
        }

    def __eq__(self, other) -> bool:
        return (type(other) == type(self)) and \
            (self._id == other._id) and \
            (self._name == other._name) and \
            (self._description == other._description) and \
            (self._jobs == other._jobs) and \
            (self._configuration == other._configuration) and \
            (self._current_job_id == other._current_job_id)
