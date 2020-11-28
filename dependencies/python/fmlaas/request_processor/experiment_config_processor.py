from typing import List

from ..model import (AggregationStrategy, DataCollectionConfig,
                     ExperimentConfiguration, InitializationStrategy, MLType,
                     Runtime)
from .request_processor import RequestProcessor


class ExperimentConfigProcessor(RequestProcessor):

    RUNTIME_KEY = "runtime"
    ML_TYPE_KEY = "ml_type"
    AGGREGATION_STRATEGY_KEY = "aggregation_strategy"
    INITIALIZATION_STRATEGY_KEY = "initialization_strategy"
    DATA_COLLECTION_CONFIG_KEY = "data_collection"
    CODE_KEY = "code"
    LEARNING_PARAMETERS_KEY = "learning_parameters"

    def __init__(self, json: dict):
        self._json = json

    def get_code(self) -> str:
        code = self._json.get(ExperimentConfigProcessor.CODE_KEY, None)

        if not code:
            raise ValueError("Code invalid. Must not be none")

        return code
    
    def get_learning_parameters(self) -> dict:
        return self._json.get(ExperimentConfigProcessor.LEARNING_PARAMETERS_KEY, dict())

    def get_runtime(self) -> Runtime:
        return Runtime(self._json.get(ExperimentConfigProcessor.RUNTIME_KEY, None))

    def get_ml_type(self) -> MLType:
        return MLType(self._json.get(ExperimentConfigProcessor.ML_TYPE_KEY, None))
    
    def get_aggregation_strategy(self) -> AggregationStrategy:
        return AggregationStrategy(self._json.get(ExperimentConfigProcessor.AGGREGATION_STRATEGY_KEY, None))
    
    def get_initialization_strategy(self) -> InitializationStrategy:
        return InitializationStrategy(self._json.get(ExperimentConfigProcessor.INITIALIZATION_STRATEGY_KEY, None))
    
    def get_data_collection_config(self) -> DataCollectionConfig:
        return DataCollectionConfig(self._json.get(ExperimentConfigProcessor.DATA_COLLECTION_CONFIG_KEY, None))

    def generate_experiment_config(self) -> ExperimentConfiguration:
        return ExperimentConfiguration(self.get_data_collection_config(),
                                       self.get_runtime(),
                                       self.get_aggregation_strategy(),
                                       self.get_ml_type(),
                                       self.get_initialization_strategy(),
                                       self.get_code(),
                                       self.get_learning_parameters(),
                                       dict())
