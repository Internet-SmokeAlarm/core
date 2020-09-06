from ...database import DB
from ...request_processor import AuthContextProcessor
from ...request_processor import TestingReportProcessor
from ...model import Job
from ...model import Project
from ...model import DBObject
from ..utils.auth.conditions import IsDevice
from ..utils.auth.conditions import ProjectContainsJob
from ..utils.auth.conditions import ProjectContainsDevice
from ..abstract_controller import AbstractController


class TestingReportController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 job_id: str,
                 testing_report_processor: TestingReportProcessor,
                 auth_context: AuthContextProcessor):
        super(TestingReportController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.job_id = job_id
        self.testing_report_processor = testing_report_processor

    def load_data(self):
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)
        self.project = DBObject.load_from_db(Project, self.job.get_project_id(), self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                ProjectContainsJob(self.project, self.job),
                ProjectContainsDevice(self.project)
            ]
        ]

    def execute_controller(self):
        if not self.job.is_complete():
            raise ValueError("Cannot submit testing report for incomplete job")

        testing_report = self.testing_report_processor.generate_testing_report(self.auth_context.get_entity_id())
        self.job.add_testing_report(testing_report)

        self.job.save_to_db(self.job_db)
