import unittest

from dependencies.python.fmlaas.model import (AggregationStrategy,
                                              DataCollectionConfig,
                                              ExperimentConfiguration,
                                              InitializationStrategy, MLType,
                                              Model, Runtime)
from dependencies.python.fmlaas.model.experiment_configuration import \
    DataCollectionConfig


class ExperimentConfigurationTestCase(unittest.TestCase):

    def _create_experiment_config(self):
        experiment_configuration = ExperimentConfiguration(DataCollectionConfig.MINIMAL_RETAIN,
                                                           Runtime.CUSTOM,
                                                           AggregationStrategy.AVERAGE,
                                                           MLType.NN,
                                                           InitializationStrategy.CUSTOMER_PROVIDED,
                                                           "",
                                                           dict(),
                                                           dict())

        json_repr = {
            "data_collection_config": DataCollectionConfig.MINIMAL_RETAIN.value,
            "runtime": Runtime.CUSTOM.value,
            "aggregation_strategy": AggregationStrategy.AVERAGE.value,
            "ml_type": MLType.NN.value,
            "initialization_strategy": InitializationStrategy.CUSTOMER_PROVIDED.value,
            "code": "",
            "learning_config": dict(),
            "parameters": dict()
        }

        return experiment_configuration, json_repr

    def test_to_json_pass(self):
        config, json_repr = self._create_experiment_config()

        self.assertEqual(config.to_json(), json_repr)

    def test_from_json_pass(self):
        config, json_repr = self._create_experiment_config()

        loaded_config = ExperimentConfiguration.from_json(json_repr)

        self.assertEqual(config, loaded_config)
    
    def test_is_parameters_set_pass(self):
        config, _ = self._create_experiment_config()

        self.assertFalse(config.is_parameters_set())

        config.parameters = Model("1231233", "123123/start_model", 1423423)

        self.assertTrue(config.is_parameters_set())

    def test_equals_pass_1(self):
        config_1, _ = self._create_experiment_config()
        config_2, _ = self._create_experiment_config()

        self.assertEqual(config_1, config_2)

    def test_equals_pass_2(self):
        config_1, _ = self._create_experiment_config()
        config_2, _ = self._create_experiment_config()
        config_2.parameters = Model("1231233", "123123/start_model", 1423423)

        self.assertNotEqual(config_1, config_2)
