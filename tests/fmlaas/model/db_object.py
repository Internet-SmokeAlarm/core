from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject, Project

from .abstract_model_testcase import AbstractModelTestCase


class DBObjectTestCase(AbstractModelTestCase):

    def test_save_to_load_from_db_1_pass(self):
        project, _ = self._create_project("1")

        db_ = InMemoryDBInterface()

        self.assertTrue(project.save_to_db(db_))
        self.assertEqual(
            DBObject.load_from_db(
                Project,
                "1",
                db_),
            project)
