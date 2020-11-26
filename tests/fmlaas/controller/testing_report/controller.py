from collections import namedtuple

from dependencies.python.fmlaas.controller.testing_report import \
    TestingReportController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsDevice, ProjectContainsDevice, ProjectContainsJob)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject, Job, Status
from dependencies.python.fmlaas.request_processor import (
    AuthContextProcessor, TestingReportProcessor)

from ..abstract_testcase import AbstractTestCase


class TestingReportControllerTestCase(AbstractTestCase):

    def setup_resources(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.add_job(job)
        experiment.start_model = job.start_model
        experiment.current_model = job.start_model
        experiment.proceed_to_next_job()

        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        testing_report_json = {
            "accuracy": 83.43,
            "loss": 2.3123,
            "confusion_matrix": [[10, 0, 0], [0, 10, 0], [0, 0, 10]]
        }
        testing_report_processor = TestingReportProcessor(testing_report_json)

        Resources = namedtuple('Resources', 'project_db job_db project job auth_context testing_report_json testing_report_processor')
        return Resources(project_db,
                         job_db,
                         project,
                         job,
                         auth_context,
                         testing_report_json,
                         testing_report_processor)

    def test_execute_pass(self):
        resources = self.setup_resources()
        resources.job.status = Status.COMPLETED
        resources.job.save_to_db(resources.job_db)

        TestingReportController(resources.project_db,
                                resources.job_db,
                                resources.job.id,
                                resources.testing_report_processor,
                                resources.auth_context).execute()

        updated_job = DBObject.load_from_db(Job, resources.job.id, resources.job_db)

        correct_json = resources.testing_report_json
        correct_json["device_id"] = "12344"

        self.assertTrue("12344" in updated_job.testing_reports)
        self.assertEqual(correct_json, updated_job.testing_reports["12344"])

    def test_execute_fail(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.job_db,
                                             resources.job.id,
                                             resources.testing_report_processor,
                                             resources.auth_context)
        self.assertRaises(ValueError, controller.execute)

    def test_get_auth_conditions_pass(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.job_db,
                                             resources.job.id,
                                             resources.testing_report_processor,
                                             resources.auth_context)

        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsDevice(),
                ProjectContainsJob(resources.project, resources.job),
                ProjectContainsDevice(resources.project)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)
