from ...database import DB
from ...model import (DBObject, Experiment, ExperimentConfiguration,
                      ExperimentFactory, Project, ProjectPrivilegeTypesEnum)
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class CreateExperimentController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 name: str,
                 description: str,
                 configuration: ExperimentConfiguration,
                 auth_context: AuthContextProcessor):
        super(CreateExperimentController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._name = name
        self._description = description
        self._configuration = configuration

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self) -> Experiment:
        next_id = str(self._project.get_num_experiments() + 1)

        experiment = ExperimentFactory.create_experiment(next_id,
                                                         self._name,
                                                         self._description,
                                                         self._configuration)

        self._project.add_or_update_experiment(experiment)
        self._project.save_to_db(self._project_db)

        return experiment
