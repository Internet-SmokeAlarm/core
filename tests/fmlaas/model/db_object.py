import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobConfiguration

class DBObjectTestCase(unittest.TestCase):

    def _build_default_job(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_12312313")
        builder.set_start_model(Model("123", "123/123", "34353").to_json())
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(50, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()

    def test_save_to_load_from_db_1_pass(self):
        job = self._build_default_job()

        db_ = InMemoryDBInterface()

        self.assertTrue(job.save_to_db(db_))
        self.assertEqual(DBObject.load_from_db(Job, "test_id", db_).to_json(), job.to_json())
