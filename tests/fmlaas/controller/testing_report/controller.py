from ..abstract_testcase import AbstractTestCase
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.request_processor import TestingReportProcessor
from dependencies.python.fmlaas.controller.testing_report import TestingReportController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsDevice
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from collections import namedtuple


class TestingReportControllerTestCase(AbstractTestCase):

    def setup_resources(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.id = "experiment_id_1"
        experiment.add_job(job)

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
        resources.job.set_status(JobStatus.COMPLETED)
        resources.job.save_to_db(resources.job_db)

        TestingReportController(resources.project_db,
                                resources.job_db,
                                resources.job.get_id(),
                                resources.testing_report_processor,
                                resources.auth_context).execute()

        updated_job = DBObject.load_from_db(Job, resources.job.get_id(), resources.job_db)

        correct_json = resources.testing_report_json
        correct_json["device_id"] = "12344"

        self.assertTrue("12344" in updated_job.get_testing_reports())
        self.assertEqual(correct_json, updated_job.get_testing_reports()["12344"])

    def test_execute_fail(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.job_db,
                                             resources.job.get_id(),
                                             resources.testing_report_processor,
                                             resources.auth_context)
        self.assertRaises(ValueError, controller.execute)

    def test_load_data_pass(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.job_db,
                                             resources.job.get_id(),
                                             resources.testing_report_processor,
                                             resources.auth_context)
        controller.load_data()

        self.assertEqual(controller.job, resources.job)
        self.assertEqual(controller.project, resources.project)

    def test_get_auth_conditions_pass(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.job_db,
                                             resources.job.get_id(),
                                             resources.testing_report_processor,
                                             resources.auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        correct_auth_conditions = [
            [
                IsDevice(),
                ProjectContainsJob(resources.project, resources.job),
                ProjectContainsDevice(resources.project)
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)
