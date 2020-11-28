from ...aws import create_presigned_post, get_models_bucket_name
from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ...s3_storage import StartModelPointer
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class SubmitExperimentStartModelController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 auth_context: AuthContextProcessor):
        super(SubmitExperimentStartModelController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)
        self._experiment = self._project.get_experiment(self._experiment_id)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60
        FIELDS = {}
        CONDITIONS = []

        s3_pointer = StartModelPointer(self._project_id, self._experiment.id)
        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            str(s3_pointer),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)

        return not self._experiment.configuration.is_parameters_set(), presigned_url
