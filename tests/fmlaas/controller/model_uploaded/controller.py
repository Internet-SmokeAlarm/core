import unittest

from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.model_uploaded import models_uploaded_controller
from dependencies.python.fmlaas.controller.model_uploaded import get_model_process_function
from dependencies.python.fmlaas.controller.model_uploaded import handle_device_model_update
from dependencies.python.fmlaas.controller.model_uploaded import handle_round_aggregate_model

class ModelUploadedControllerTestCase(unittest.TestCase):

    def _build_default_round(self):
        round_builder = RoundBuilder()
        round_builder.set_id("2345")
        configuration = RoundConfiguration("1", "RANDOM")
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_builder.set_start_model(Model("1234", "1234/1234", "123211").to_json())

        return round_builder.build()

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        return group_builder.build()

    def test_get_model_process_function_pass_1(self):
        model = Model("1234", "1234/23456/435647", "923843287")

        self.assertEqual(handle_device_model_update, get_model_process_function(model.get_name()))

    def test_get_model_process_function_pass_2(self):
        model = Model("1234", "1234/23456/23456", "923843287")

        self.assertEqual(handle_round_aggregate_model, get_model_process_function(model.get_name()))

    def test_handle_device_model_update_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/2345/3456", "1232131")

        round = self._build_default_round()
        round.save_to_db(db_)

        self.assertFalse(round.is_device_model_submitted("3456"))

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)

        self.assertTrue(round_2.is_device_model_submitted("3456"))

    def test_handle_device_model_update_pass_no_aggregation(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/2345/3456", "1232131")

        round = self._build_default_round()
        round.configuration = RoundConfiguration("2", "RANDOM").to_json()
        round.devices = ["3456", "4567"]
        round.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)
        self.assertTrue(round.is_in_progress())
        self.assertFalse(round.is_ready_for_aggregation())

    def test_handle_device_model_update_duplicate_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/2345/3456", "1232131")
        model_2 = Model(None, "1234/2345/3456", "66665")

        round = self._build_default_round()
        round.save_to_db(db_)

        handle_device_model_update(model, None, db_)
        handle_device_model_update(model_2, None, db_)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)
        self.assertTrue(round_2.is_device_model_submitted("3456"))
        self.assertEqual("66665", round_2.models["3456"]["size"])

    def test_handle_device_model_update_pass_agg_in_progress(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/2345/3456", "1232131")

        round = self._build_default_round()
        round.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)

    def test_handle_round_aggregate_model_pass(self):
        db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(db_)

        model = Model(None, "1234/2345/3456", "1232131")
        handle_device_model_update(model, None, db_)

        aggregate_model = Model(None, "1234/2345/2345", "435345")
        should_aggregate = handle_round_aggregate_model(aggregate_model, None, db_)
        self.assertFalse(should_aggregate)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)

        self.assertTrue(round_2.is_complete())
        self.assertEqual(round_2.get_aggregate_model().get_size(), "435345")

    def test_models_uploaded_controller_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "test_id/test_id", "1232131")

        group = self._build_default_group()
        group.save_to_db(db_)

        models_uploaded_controller(db_, None, [model])

        group_2 = DBObject.load_from_db(FLGroup, group.get_id(), db_)

        self.assertEqual(group_2.get_initial_model().to_json(), model.to_json())
