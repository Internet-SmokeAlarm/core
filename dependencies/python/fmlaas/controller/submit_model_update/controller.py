from ...database import DB
from ...aws import create_presigned_post
from ...s3_storage import DeviceModelPointer
from ...aws import get_models_bucket_name
from ...request_processor import AuthContextProcessor
from ...database import DynamoDBInterface
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

        self.project_db = project_db
        self.job_db = job_db
        self.project_id = project_id
        self.job_id = job_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                ProjectContainsJob(self.project, self.job),
                JobContainsDevice(self.job)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60
        FIELDS = {}
        CONDITIONS = []

        s3_object_pointer = DeviceModelPointer(
            self.project.get_id(),
            self.job.get_experiment_id(),
            self.job.get_id(),
            self.auth_context.get_entity_id()
        )
        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            str(s3_object_pointer),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)

        can_submit_model_to_job = self.job.is_in_progress() and self.job.is_device_active(
            self.auth_context.get_entity_id())

        termination_check(self.job, self.job_db, self.project_db)

        return can_submit_model_to_job, presigned_url
