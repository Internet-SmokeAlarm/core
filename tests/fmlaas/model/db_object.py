from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobConfiguration
from .abstract_model_testcase import AbstractModelTestCase


class DBObjectTestCase(AbstractModelTestCase):

    def test_save_to_load_from_db_1_pass(self):
        job = self._build_job(1)

        db_ = InMemoryDBInterface()

        self.assertTrue(job.save_to_db(db_))
        self.assertEqual(
            DBObject.load_from_db(
                Job,
                "test_id_1",
                db_),
            job)
