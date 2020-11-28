import base64
import unittest

from dependencies.python.fmlaas.model import (AggregationStrategy,
                                              DataCollectionConfig,
                                              ExperimentConfiguration,
                                              InitializationStrategy, MLType,
                                              Runtime)
from dependencies.python.fmlaas.request_processor import \
    ExperimentConfigProcessor


class ExperimentConfigProcessorTestCase(unittest.TestCase):

    def test_get_runtime_pass(self):
        data = {
            "runtime": Runtime.CUSTOM.value
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual(Runtime.CUSTOM, config_processor.get_runtime())

    def test_get_ml_type_pass(self):
        data = {
            "ml_type": MLType.NN.value
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual(MLType.NN, config_processor.get_ml_type())
    
    def test_get_aggregation_strategy_pass(self):
        data = {
            "aggregation_strategy": AggregationStrategy.AVERAGE.value
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual(AggregationStrategy.AVERAGE, config_processor.get_aggregation_strategy())

    def test_get_data_collection_config_pass(self):
        data = {
            "data_collection": DataCollectionConfig.MINIMAL_RETAIN
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual(DataCollectionConfig.MINIMAL_RETAIN, config_processor.get_data_collection_config())

    def test_get_code_pass(self):
        data = {
            "code": "123123123123"
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual("123123123123", config_processor.get_code())

    def test_get_initialization_strategy_pass(self):
        data = {
            "initialization_strategy": InitializationStrategy.CUSTOMER_PROVIDED.value
        }
        config_processor = ExperimentConfigProcessor(data)

        self.assertEqual(InitializationStrategy.CUSTOMER_PROVIDED, config_processor.get_initialization_strategy())
    
    def test_generate_experiment_config_pass(self):
        b64_code = base64.b64encode("This is a test string".encode("utf-8"))

        data = {
            "runtime": Runtime.CUSTOM.value,
            "initialization_strategy": InitializationStrategy.CUSTOMER_PROVIDED.value,
            "data_collection": DataCollectionConfig.MINIMAL_RETAIN.value,
            "aggregation_strategy": AggregationStrategy.AVERAGE.value,
            "ml_type": MLType.NN.value,
            "code": b64_code,
            "learning_parameters": dict()
        }
        config_processor = ExperimentConfigProcessor(data)
        
        experiment_config = config_processor.generate_experiment_config()
        correct_experiment_config = ExperimentConfiguration(DataCollectionConfig.MINIMAL_RETAIN,
                                                            Runtime.CUSTOM,
                                                            AggregationStrategy.AVERAGE,
                                                            MLType.NN,
                                                            InitializationStrategy.CUSTOMER_PROVIDED,
                                                            b64_code,
                                                            dict(),
                                                            dict())

        self.assertEqual(correct_experiment_config, experiment_config)
