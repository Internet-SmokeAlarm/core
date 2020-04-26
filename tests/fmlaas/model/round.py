import unittest

from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria
from dependencies.python.fmlaas.utils import get_epoch_time

class RoundTestCase(unittest.TestCase):

    def _build_default_round(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration(2, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()

    def test_to_json_pass(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED.value,
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"name" : "21313124/21313124", "entity_id" : "21313124", "size" : "21313124"},
            {"config info" : "here"},
            {"test1" : {"size" : "123300"}},
            "December 19th, 2019",
            "1234345",
            "fl_group_12312313")

        round_json = round.to_json()

        self.assertEqual("my_id", round_json["ID"])
        self.assertEqual("COMPLETED", round_json["status"])
        self.assertEqual(["test1", "test2"], round_json["devices"])
        self.assertEqual({"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, round_json["aggregate_model"])
        self.assertEqual({"name" : "21313124/21313124", "entity_id" : "21313124", "size" : "21313124"}, round_json["start_model"])
        self.assertEqual({"config info" : "here"}, round_json["configuration"])
        self.assertEqual({"test1" : {"size" : "123300"}}, round_json["models"])
        self.assertEqual("December 19th, 2019", round_json["created_on"])
        self.assertEqual("1234345", round_json["billable_size"])
        self.assertEqual("fl_group_12312313", round_json["parent_group_id"])

    def test_from_json_pass(self):
        round_json = {'ID': 'my_id', 'status': 'COMPLETED', 'devices': ['test1', 'test2'], 'aggregate_model': {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, 'start_model': {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, 'configuration': {'num_devices' : "5", "num_buffer_devices" : "0", "device_selection_strategy" : "RANDOM", "termination_criteria" : []}, 'models': {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}}, 'created_on': 'December 19th, 2019', "billable_size" : "0", "parent_group_id" : "fl_group_12312313"}

        round = Round.from_json(round_json)

        self.assertEqual(round.get_id(), round_json["ID"])
        self.assertEqual(round.get_status(), RoundStatus.COMPLETED)
        self.assertEqual(round.get_devices(), round_json["devices"])
        self.assertEqual(round.get_aggregate_model().to_json(), round_json["aggregate_model"])
        self.assertEqual(round.get_configuration().to_json(), round_json["configuration"])
        self.assertEqual(round.get_models()["123235345"].to_json(), round_json["models"]["123235345"])
        self.assertEqual(round.get_created_on(), round_json["created_on"])
        self.assertEqual(round.get_start_model().to_json(), round_json["start_model"])
        self.assertEqual(round.get_billable_size(), int(round_json["billable_size"]))
        self.assertEqual(round.get_parent_group_id(), round_json["parent_group_id"])

    def test_add_model_pass(self):
        round = self._build_default_round()

        model = Model("12312312", "2345/device_models/12312312", "234342324")

        round.add_model(model)

        self.assertTrue(model.get_entity_id() in round.models)
        self.assertTrue("12312312" in round.models[model.get_entity_id()]["name"])
        self.assertEqual(model.get_size(), round.models[model.get_entity_id()]["size"])

    def test_get_models(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED,
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"config info" : "here"},
            {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, "1232353465" : {"name" : "21313124/123123/1232353465", "entity_id" : "1232353465", "size" : "2134235"}},
            "December 19th, 2019",
            "0",
            "fl_group_12312313")

        models = round.get_models()

        self.assertEqual(len(models), 2)
        self.assertTrue("123235345" in models)
        self.assertTrue("1232353465" in models)

    def test_is_cancelled_pass_1(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.CANCELLED)

        self.assertTrue(round.is_cancelled())

    def test_is_cancelled_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.COMPLETED)

        self.assertFalse(round.is_cancelled())

    def test_is_in_progress_pass_1(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.IN_PROGRESS)

        self.assertTrue(round.is_in_progress())

    def test_is_in_progress_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.AGGREGATION_IN_PROGRESS)

        self.assertFalse(round.is_in_progress())

    def test_is_aggregation_in_progress_pass_1(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(round.is_aggregation_in_progress())

    def test_is_aggregation_in_progress_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.IN_PROGRESS)

        self.assertFalse(round.is_aggregation_in_progress())

    def test_is_complete_pass_1(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.COMPLETED)

        self.assertTrue(round.is_complete())

    def test_is_complete_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.IN_PROGRESS)

        self.assertFalse(round.is_complete())

    def test_is_active_pass_1(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.COMPLETED)

        self.assertFalse(round.is_active())

    def test_is_active_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.IN_PROGRESS)

        self.assertTrue(round.is_active())

    def test_is_active_pass_3(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(round.is_active())

    def test_contains_device_pass(self):
        round = self._build_default_round()

        self.assertTrue(round.contains_device("123"))
        self.assertFalse(round.contains_device("test10"))
        self.assertTrue(round.contains_device("234"))

    def test_is_device_active_pass(self):
        round = self._build_default_round()

        round.set_start_model(Model("34234342", "34234342/start_model", "234514"))

        self.assertTrue(round.is_device_active("123"))
        self.assertTrue(round.is_device_active("234"))

        round.add_model(Model("123", "34234342/device_models/123", "12355"))

        self.assertFalse(round.is_device_active("123"))
        self.assertTrue(round.is_device_active("234"))

    def test_is_device_active_pass_2(self):
        round = self._build_default_round()
        round.set_status(RoundStatus.COMPLETED)

        self.assertFalse(round.is_device_active("123"))
        self.assertFalse(round.is_device_active("234"))

    def test_is_aggregate_model_set_pass_1(self):
        round = self._build_default_round()

        self.assertFalse(round.is_aggregate_model_set())

    def test_is_aggregate_model_set_pass_2(self):
        round = self._build_default_round()

        round.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertTrue(round.is_aggregate_model_set())

    def test_is_ready_for_aggregation_pass(self):
        round = self._build_default_round()

        self.assertFalse(round.is_ready_for_aggregation())
        self.assertEqual(round.get_status(), RoundStatus.INITIALIZED)

    def test_is_in_initialization_pass_1(self):
        round = self._build_default_round()

        self.assertTrue(round.is_in_initialization())
        self.assertEqual(round.get_status(), RoundStatus.INITIALIZED)

    def test_is_in_initialization_pass_2(self):
        round = self._build_default_round()

        round.set_start_model(Model("1234", "1234/start_model", "1234345"))

        self.assertFalse(round.is_in_initialization())
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)

    def test_set_start_model_pass_1(self):
        round = self._build_default_round()

        start_model = Model("1234", "1234/start_model", "1234345")
        round.set_start_model(start_model)

        self.assertEqual(start_model.to_json(), round.get_start_model().to_json())
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)

    def test_set_start_model_pass_2(self):
        round = self._build_default_round()

        start_model = Model("1234", "1234/start_model", "1234345")
        round.set_start_model(start_model)
        round.set_start_model(Model("123445645", "123445645/start_model", "6435453"))

        self.assertEqual(start_model.to_json(), round.get_start_model().to_json())
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)

    def test_is_ready_for_aggregation_pass_2(self):
        round = self._build_default_round()

        round.add_model(Model("123", "fdldasf", "1231231"))
        round.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(round.is_ready_for_aggregation())

    def test_should_aggregate_pass(self):
        round = self._build_default_round()

        self.assertFalse(round.should_aggregate())
        self.assertEqual(round.get_status(), RoundStatus.INITIALIZED)

    def test_should_aggregate_pass_2(self):
        round = self._build_default_round()

        round.set_start_model(Model("123456", "123456/start_model", "12321"))
        round.add_model(Model("123", "fdldasf", "1231231"))
        round.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(round.should_aggregate())
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)

    def test_should_aggregate_pass_3(self):
        round = self._build_default_round()

        round.add_model(Model("123", "fdldasf", "1231231"))
        round.add_model(Model("234", "fdldasf", "1231231"))
        round.set_status(RoundStatus.COMPLETED)

        self.assertFalse(round.should_aggregate())

    def test_is_device_model_submitted_pass(self):
        round = self._build_default_round()

        self.assertFalse(round.is_device_model_submitted("123"))
        self.assertFalse(round.is_device_model_submitted("234"))

        round.add_model(Model("123", "fdldasf", "1231231"))

        self.assertTrue(round.is_device_model_submitted("123"))
        self.assertFalse(round.is_device_model_submitted("234"))

        round.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(round.is_device_model_submitted("123"))
        self.assertTrue(round.is_device_model_submitted("234"))

    def test_cancel_pass(self):
        round = self._build_default_round()

        round.set_start_model(Model("1234", "1234/start_model", "231241"))

        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)

        round.cancel()

        self.assertEqual(round.get_status(), RoundStatus.CANCELLED)
        self.assertEqual(round.get_start_model().to_json(), round.get_end_model().to_json())
        self.assertEqual(round.get_billable_size(), 231241)

    def test_cancel_pass_2(self):
        round = self._build_default_round()

        round.cancel()

        self.assertEqual(round.get_status(), RoundStatus.CANCELLED)
        self.assertEqual(round.get_billable_size(), 0)

    def test_complete_pass(self):
        round = self._build_default_round()

        round.set_start_model(Model("1234", "1234/start_model", "231241"))

        round.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))
        round.complete()

        self.assertEqual(round.get_status(), RoundStatus.COMPLETED)
        self.assertEqual(round.get_aggregate_model().to_json(), round.get_end_model().to_json())
        self.assertEqual(round.get_billable_size(), 243565)

    def test_calculate_billable_size_pass_1(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration(50, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())
        round = builder.build()

        round.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(round.calculate_billable_size(), "12324")

    def test_calculate_billable_size_pass_2(self):
        round = self._build_default_round()

        round.add_model(Model("1231241241", "123/345/1231241241", "55543"))
        round.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(round.calculate_billable_size(), "67867")

    def test_should_terminate_pass(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(0, 2313123.1231).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        round = builder.build()

        self.assertTrue(round.should_terminate())

    def test_should_terminate_pass_2(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(10, float(get_epoch_time())).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        round = builder.build()

        self.assertFalse(round.should_terminate())

    def test_reset_termination_criteria_pass(self):
        builder = RoundBuilder()
        builder.set_id("test_id")
        builder.set_parent_group_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = RoundConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(10, float(get_epoch_time()) - 100).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        round = builder.build()

        self.assertTrue(round.should_terminate())

        round.reset_termination_criteria()

        self.assertFalse(round.should_terminate())
