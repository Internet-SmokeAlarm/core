from ...database import DB
from ...request_processor import AuthContextProcessor
from ...aws import create_presigned_post
from ...s3_storage import StartModelPointer
from ...aws import get_models_bucket_name
from ...database import DynamoDBInterface
from ...model import Job
from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..utils import termination_check
from ..abstract_controller import AbstractController


class SubmitExperimentStartModelController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 auth_context: AuthContextProcessor):
        super(SubmitExperimentStartModelController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_id = project_id
        self.experiment_id = experiment_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)
        self.experiment = self.project.get_experiment(self.experiment_id)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60
        FIELDS = {}
        CONDITIONS = []

        s3_pointer = StartModelPointer(self.project_id, self.experiment.id)
        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            str(s3_pointer),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)

        return not self.experiment.is_start_model_set(), presigned_url
