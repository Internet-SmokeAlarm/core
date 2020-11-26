from ...database import DB
from ...model import DBObject, Job, Project
from ...request_processor import AuthContextProcessor, TestingReportProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import (IsDevice, ProjectContainsDevice,
                                     ProjectContainsJob)


class TestingReportController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 job_id: str,
                 testing_report_processor: TestingReportProcessor,
                 auth_context: AuthContextProcessor):
        super(TestingReportController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._job_id = job_id
        self._testing_report_processor = testing_report_processor

        self._job = DBObject.load_from_db(Job, self._job_id, self._job_db)
        self._project = DBObject.load_from_db(Project, self._job.project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                ProjectContainsJob(self._project, self._job),
                ProjectContainsDevice(self._project)
            ]
        ]

    def execute_controller(self) -> None:
        if not self._job.is_complete():
            raise ValueError("Cannot submit testing report for incomplete job")

        testing_report = self._testing_report_processor.generate_testing_report(self.auth_context.get_entity_id())
        self._job.add_testing_report(testing_report)

        self._job.save_to_db(self._job_db)
