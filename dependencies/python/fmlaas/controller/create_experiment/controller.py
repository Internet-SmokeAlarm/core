from ...database import DB
from ...model import (DBObject, Experiment, ExperimentFactory, Project,
                      ProjectPrivilegeTypesEnum)
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class CreateExperimentController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_name: str,
                 auth_context: AuthContextProcessor):
        super(CreateExperimentController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_name = experiment_name

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self) -> Experiment:
        experiment = ExperimentFactory.create_experiment(self._project.get_num_experiments(),
                                                         self.experiment_name)

        self._project.add_or_update_experiment(experiment)
        self._project.save_to_db(self._project_db)

        return experiment
