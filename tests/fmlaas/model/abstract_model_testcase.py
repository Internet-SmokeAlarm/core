import unittest
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import JobSequence


class AbstractModelTestCase(unittest.TestCase):

    def _build_default_job_sequence(self):
        sequence = JobSequence(
            "123dafasdf34sdfsdf",
            [],
            {},
            "NONE",
            {},
            False)

        sequence_json = {
            "ID" : "123dafasdf34sdfsdf",
            "jobs" : [],
            "current_job" : "NONE",
            "start_model" : {},
            "learning_parameters" : {},
            "is_active" : False
        }

        return sequence, sequence_json

    def _build_job(self, id):
        builder = JobBuilder()
        builder.set_id("test_id_{}".format(id))
        builder.set_parent_job_sequence_id("123dafasdf34sdfsdf")
        builder.set_parent_project_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(2, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()
