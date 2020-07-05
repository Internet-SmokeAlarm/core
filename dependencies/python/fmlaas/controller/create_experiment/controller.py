from ...database import DB
from ... import generate_unique_id
from ...model import Project
from ...model import ExperimentBuilder
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions


class CreateExperimentController(AbstractController):

    def __init__(self, project_db: DB, project_id: str, auth_context: AuthContextProcessor):
        super(CreateExperimentController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        builder = ExperimentBuilder()
        builder.id = generate_unique_id()
        experiment = builder.build()

        self.project.add_or_update_experiment(experiment)
        self.project.save_to_db(self.project_db)

        return experiment
