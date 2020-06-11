import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import JobContainsDevice
from ....abstract_controller_testcase import AbstractControllerTestCase


class JobContainsDeviceTestCase(AbstractControllerTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        job = self._build_simple_job()

        self.assertFalse(JobContainsDevice(job).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        job = self._build_simple_job()

        self.assertTrue(JobContainsDevice(job).verify(auth_context))

    def test_eq_pass(self):
        job = self._build_simple_job()

        self.assertEqual(JobContainsDevice(job), JobContainsDevice(job))

    def test_eq_fail(self):
        job = self._build_simple_job()
        job_2 = self._build_simple_job()
        job_2.complete()

        self.assertNotEqual(JobContainsDevice(job), JobContainsDevice(job_2))

    def test_eq_fail_2(self):
        job = self._build_simple_job()

        self.assertNotEqual(JobContainsDevice(job), IsDevice())
