from ...database import DB
from ...aws import create_presigned_post
from ...s3_storage import DeviceModelPointer
from ...aws import get_models_bucket_name
from ...request_processor import AuthContextProcessor
from ...model import Job
from ...model import Project
from ...model import DBObject
from ..utils.auth.conditions import IsDevice
from ..utils.auth.conditions import ProjectContainsJob
from ..utils.auth.conditions import JobContainsDevice
from ..utils import termination_check
from ..abstract_controller import AbstractController


class SubmitModelUpdateController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 project_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(SubmitModelUpdateController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._project_id = project_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)
        self._job = DBObject.load_from_db(Job, self._job_id, self._job_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                ProjectContainsJob(self._project, self._job),
                JobContainsDevice(self._job)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60
        FIELDS = {}
        CONDITIONS = []

        s3_object_pointer = DeviceModelPointer(
            self._project.id,
            self._job.experiment_id,
            self._job.id,
            self.auth_context.get_entity_id()
        )
        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            str(s3_object_pointer),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)

        can_submit_model_to_job = self._job.is_in_progress() and self._job.is_device_active(
            self.auth_context.get_entity_id())

        termination_check(self._job, self._job_db, self._project_db)

        return can_submit_model_to_job, presigned_url
