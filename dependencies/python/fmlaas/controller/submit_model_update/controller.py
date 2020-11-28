from ...aws import create_presigned_post, get_models_bucket_name
from ...database import DB
from ...model import DBObject, Project
from ...request_processor import AuthContextProcessor
from ...s3_storage import DeviceModelPointer
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsDevice, JobContainsDevice


class SubmitModelUpdateController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(SubmitModelUpdateController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)
        self._experiment = self._project.get_experiment(self._experiment_id)
        self._job = self._experiment.get_job(self._job_id)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                JobContainsDevice(self._job)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60
        FIELDS = {}
        CONDITIONS = []

        s3_object_pointer = DeviceModelPointer(
            self._project_id,
            self._experiment_id,
            self._job_id,
            self.auth_context.get_entity_id()
        )
        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            str(s3_object_pointer),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)
        
        self._experiment.handle_termination_check()
        self._job = self._experiment.get_job(self._job_id)

        self._project.add_or_update_experiment(self._experiment)
        self._project.save_to_db(self._project_db)

        can_submit_model_to_job = self._job.is_device_active(self.auth_context.get_entity_id())

        return can_submit_model_to_job, presigned_url
