import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundConfiguration

class DBObjectTestCase(unittest.TestCase):

    def _build_default_round(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_12312313")
        builder.set_start_model(Model("123", "123/123", "34353").to_json())
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration("50", "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()

    def test_save_to_load_from_db_1_pass(self):
        round = self._build_default_round()

        db_ = InMemoryDBInterface()

        self.assertTrue(round.save_to_db(db_))
        self.assertEqual(DBObject.load_from_db(Round, "test_id", db_).to_json(), round.to_json())
