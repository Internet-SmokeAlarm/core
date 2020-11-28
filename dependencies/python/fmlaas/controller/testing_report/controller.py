from ...database import DB
from ...model import DBObject, Project
from ...request_processor import AuthContextProcessor, TestingReportProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsDevice, ProjectContainsDevice


class TestingReportController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_id: str,
                 testing_report_processor: TestingReportProcessor,
                 auth_context: AuthContextProcessor):
        super(TestingReportController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_id = job_id
        self._testing_report_processor = testing_report_processor

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)
        self._experiment = self._project.get_experiment(self._experiment_id)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                ProjectContainsDevice(self._project)
            ]
        ]

    def execute_controller(self) -> None:
        self._experiment.handle_termination_check()
    
        self._job = self._experiment.get_job(self._job_id)

        if not self._job.is_complete():
            raise ValueError("Cannot submit testing report for incomplete job")

        testing_report = self._testing_report_processor.generate_testing_report(self.auth_context.get_entity_id())
        self._job.add_testing_report(testing_report)

        self._experiment.add_or_update_job(self._job)
        self._project.add_or_update_experiment(self._experiment)
        self._project.save_to_db(self._project_db)
