from collections import namedtuple

from dependencies.python.fmlaas.controller.testing_report import \
    TestingReportController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsDevice, ProjectContainsDevice)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject, Project
from dependencies.python.fmlaas.request_processor import (
    AuthContextProcessor, TestingReportProcessor)

from ..abstract_testcase import AbstractTestCase


class TestingReportControllerTestCase(AbstractTestCase):

    def setup_resources(self):
        project_db = InMemoryDBInterface()

        job = self._build_simple_job()

        project = self._build_simple_project()

        experiment, _ = self._build_simple_experiment("1")

        experiment.add_or_update_job(job)

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

        Resources = namedtuple('Resources', 'project_db project experiment job auth_context testing_report_json testing_report_processor')
        return Resources(project_db,
                         project,
                         experiment,
                         job,
                         auth_context,
                         testing_report_json,
                         testing_report_processor)

    def test_execute_pass(self):
        resources = self.setup_resources()
        
        resources.job.complete()
        resources.experiment.add_or_update_job(resources.job)
        resources.project.add_or_update_experiment(resources.experiment)
        resources.project.save_to_db(resources.project_db)

        TestingReportController(resources.project_db,
                                resources.project.id,
                                resources.experiment.id,
                                resources.job.id,
                                resources.testing_report_processor,
                                resources.auth_context).execute()

        updated_project = DBObject.load_from_db(Project, resources.project.id, resources.project_db)
        updated_job = updated_project.get_experiment(resources.experiment.id).get_job(resources.job.id)

        correct_json = resources.testing_report_json
        correct_json["device_id"] = "12344"

        self.assertTrue("12344" in updated_job.testing_reports)
        self.assertEqual(correct_json, updated_job.testing_reports["12344"])

    def test_execute_fail(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.project.id,
                                             resources.experiment.id,
                                             resources.job.id,
                                             resources.testing_report_processor,
                                             resources.auth_context)
        self.assertRaises(ValueError, controller.execute)

    def test_get_auth_conditions_pass(self):
        resources = self.setup_resources()

        controller = TestingReportController(resources.project_db,
                                             resources.project.id,
                                             resources.experiment.id,
                                             resources.job.id,
                                             resources.testing_report_processor,
                                             resources.auth_context)

        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsDevice(),
                ProjectContainsDevice(resources.project)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)
