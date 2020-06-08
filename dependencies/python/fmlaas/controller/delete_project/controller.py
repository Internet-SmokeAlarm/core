from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class DeleteProjectController(AbstractController):

    def __init__(self, project_db, job_db, project_id, auth_context):
        """
        :param project_db: DB
        :param job_db: DB
        :param project_id: string
        :param auth_context: auth_context
        """
        super(DeleteProjectController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.project_id = project_id

    def load_data(self):
        try:
            self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)
        except BaseException:
            raise_default_request_forbidden_error()

    def get_auth_conditions(self):
        return [
            IsUser(),
            HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.ADMIN)
        ]

    def execute_controller(self):
        for job_id in self.project.get_all_job_ids():
            self.job_db.delete_object(job_id)

        self.project_db.delete_object(self.project_id)
