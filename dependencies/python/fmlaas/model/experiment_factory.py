from dependencies.python.fmlaas.model.experiment_configuration import ExperimentConfiguration
from .experiment import Experiment


class ExperimentFactory:
    
    @staticmethod
    def create_experiment(id: str,
                          name: str,
                          description: str,
                          config: ExperimentConfiguration) -> Experiment:
        jobs = dict()
        current_job_id = ""

        return Experiment(id,
                          name,
                          description,
                          jobs,
                          config,
                          current_job_id)
