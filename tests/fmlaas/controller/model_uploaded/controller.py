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
from dependencies.python.fmlaas.controller.model_uploaded import handle_round_start_model

class ModelUploadedControllerTestCase(unittest.TestCase):

    def _build_default_round(self):
        round_builder = RoundBuilder()
        round_builder.set_id("1234")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM", [])
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_builder.set_start_model(Model("1234", "1234/start_model", "123211").to_json())

        return round_builder.build()

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        return group_builder.build()

    def test_get_model_process_function_pass_1(self):
        model = Model("1232344", "1234/device_models/1232344", "923843287")

        self.assertEqual(handle_device_model_update, get_model_process_function(model.get_name()))

    def test_get_model_process_function_pass_2(self):
        model = Model("1234", "1234/aggregate_model", "923843287")

        self.assertEqual(handle_round_aggregate_model, get_model_process_function(model.get_name()))

    def test_get_model_process_function_pass_3(self):
        model = Model("1234", "1234/start_model", "923843287")

        self.assertEqual(handle_round_start_model, get_model_process_function(model.get_name()))

    def test_handle_device_model_update_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/device_models/1232344", "1232131")

        round = self._build_default_round()
        round.save_to_db(db_)

        self.assertFalse(round.is_device_model_submitted("1232344"))

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)

        self.assertTrue(round_2.is_device_model_submitted("1232344"))

    def test_handle_device_model_update_pass_no_aggregation(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/device_models/1232344", "1232131")

        round = self._build_default_round()
        round.configuration = RoundConfiguration("2", "RANDOM", []).to_json()
        round.devices = ["1232344", "4567"]
        round.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)
        self.assertTrue(round.is_in_progress())
        self.assertFalse(round.is_ready_for_aggregation())

    def test_handle_device_model_update_duplicate_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/device_models/3456", "1232131")
        model_2 = Model(None, "1234/device_models/3456", "66665")

        round = self._build_default_round()
        round.save_to_db(db_)

        handle_device_model_update(model, None, db_)
        handle_device_model_update(model_2, None, db_)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)
        self.assertTrue(round_2.is_device_model_submitted("3456"))
        self.assertEqual("66665", round_2.models["3456"]["size"])

    def test_handle_device_model_update_pass_agg_in_progress(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "1234/device_models/3456", "1232131")

        round = self._build_default_round()
        round.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)

    def test_handle_round_aggregate_model_pass(self):
        group_db = InMemoryDBInterface()
        db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(db_)

        group = self._build_default_group()
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db)

        model = Model(None, "1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, db_)

        aggregate_model = Model(None, "1234/device_models/2345", "435345")
        should_aggregate = handle_round_aggregate_model(aggregate_model, group_db, db_)
        self.assertFalse(should_aggregate)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)

        self.assertTrue(round_2.is_complete())
        self.assertEqual(round_2.get_aggregate_model().get_size(), "435345")

    def test_handle_round_aggregate_model_pass_2(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db)

        round_builder = RoundBuilder()
        round_builder.set_id("12341")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM", [])
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_2 = round_builder.build()
        round_2.save_to_db(round_db)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())
        group.save_to_db(group_db)

        model = Model(None, "1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, round_db)
        aggregate_model = Model(None, "1234/device_models/2345", "435345")
        handle_round_aggregate_model(aggregate_model, group_db, round_db)

        group_from_db = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        self.assertEqual(1, len(group_from_db.get_current_round_ids()))
        self.assertEqual(round_2.get_id(), group_from_db.get_current_round_ids()[0])

        round_2_from_db = DBObject.load_from_db(Round, round_2.get_id(), round_db)
        round_from_db = DBObject.load_from_db(Round, round.get_id(), round_db)
        self.assertEqual(round_from_db.get_aggregate_model().to_json(), round_2_from_db.get_start_model().to_json())

    def test_handle_round_aggregate_model_pass_3(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db)

        round_builder = RoundBuilder()
        round_builder.set_id("12341")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM", [])
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_2 = round_builder.build()
        round_2.cancel()
        round_2.save_to_db(round_db)

        round_builder = RoundBuilder()
        round_builder.set_id("12342")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM", [])
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_3 = round_builder.build()
        round_3.save_to_db(round_db)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())
        group.add_round_to_path_prev_id(round_2.get_id(), round_3.get_id())
        group.save_to_db(group_db)

        model = Model(None, "1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, round_db)
        aggregate_model = Model(None, "1234/device_models/2345", "435345")
        handle_round_aggregate_model(aggregate_model, group_db, round_db)

        group_from_db = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        self.assertEqual(1, len(group_from_db.get_current_round_ids()))
        self.assertEqual(round_3.get_id(), group_from_db.get_current_round_ids()[0])

        round_3_from_db = DBObject.load_from_db(Round, round_3.get_id(), round_db)
        round_from_db = DBObject.load_from_db(Round, round.get_id(), round_db)
        self.assertEqual(round_from_db.get_aggregate_model().to_json(), round_3_from_db.get_start_model().to_json())

    def test_handle_round_start_model_pass(self):
        db_ = InMemoryDBInterface()

        round_builder = RoundBuilder()
        round_builder.set_id("1234")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM", [])
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round = round_builder.build()

        round.save_to_db(db_)

        model = Model(None, "1234/start_model", "1232131")
        should_aggregate = handle_round_start_model(model, None, db_)

        self.assertFalse(should_aggregate)

        round_2 = DBObject.load_from_db(Round, round.get_id(), db_)

        self.assertTrue(round_2.is_in_progress())
