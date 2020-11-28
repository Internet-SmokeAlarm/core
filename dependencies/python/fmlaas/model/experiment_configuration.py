from enum import Enum

from .model import Model


class DataCollectionConfig(Enum):

    MINIMAL_PURGE = "MINIMAL_PURGE"
    MINIMAL_RETAIN = "MINIMAL_RETAIN"


class Runtime(Enum):

    CUSTOM = "CUSTOM"


class AggregationStrategy(Enum):

    AVERAGE = "AVERAGE"


class MLType(Enum):

    NN = "NN"


class InitializationStrategy(Enum):

    CUSTOMER_PROVIDED = "CUSTOMER_PROVIDED"


class ExperimentConfiguration:

    def __init__(self,
                 data_collection_config: DataCollectionConfig,
                 runtime: Runtime,
                 aggregation_strategy: AggregationStrategy,
                 ml_type: MLType,
                 initialization_strategy: InitializationStrategy,
                 code: str,
                 learning_config: dict,
                 parameters: dict):
        self._data_collection_config = data_collection_config
        self._runtime = runtime
        self._aggregation_strategy = aggregation_strategy
        self._ml_type = ml_type
        self._initialization_strategy = initialization_strategy
        self._code = code
        self._learning_config = learning_config
        self._parameters = parameters
    
    @property
    def data_collection_config(self) -> DataCollectionConfig:
        return self._data_collection_config
    
    @property
    def runtime(self) -> Runtime:
        return self._runtime

    @property
    def aggregation_strategy(self) -> AggregationStrategy:
        return self._aggregation_strategy
    
    @property
    def ml_type(self) -> MLType:
        return self._ml_type
    
    @property
    def initialization_strategy(self) -> InitializationStrategy:
        return self._initialization_strategy
    
    @property
    def code(self) -> str:
        return self._code
    
    @property
    def learning_config(self) -> dict:
        return self._learning_config
    
    @property
    def parameters(self) -> Model:
        return Model.from_json(self._parameters)
    
    @parameters.setter
    def parameters(self, parameters: Model) -> None:
        self._parameters = parameters.to_json()
    
    def is_parameters_set(self) -> bool:
        return Model.is_valid_json(self._parameters)
    
    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._data_collection_config == other._data_collection_config) and \
            (self._runtime == other._runtime) and \
            (self._aggregation_strategy == other._aggregation_strategy) and \
            (self._ml_type == other._ml_type) and \
            (self._initialization_strategy == other._initialization_strategy) and \
            (self._code == other._code) and \
            (self._learning_config == other._learning_config) and \
            (self._parameters == other._parameters)

    def to_json(self) -> dict:
        return {
            "data_collection_config": self._data_collection_config.value,
            "runtime": self._runtime.value,
            "aggregation_strategy": self._aggregation_strategy.value,
            "ml_type": self._ml_type.value,
            "initialization_strategy": self._initialization_strategy.value,
            "code": self._code,
            "learning_config": self._learning_config,
            "parameters": self._parameters
        }
    
    @staticmethod
    def from_json(json_data):
        return ExperimentConfiguration(DataCollectionConfig(json_data["data_collection_config"]),
                                       Runtime(json_data["runtime"]),
                                       AggregationStrategy(json_data["aggregation_strategy"]),
                                       MLType(json_data["ml_type"]),
                                       InitializationStrategy(json_data["initialization_strategy"]),
                                       json_data["code"],
                                       json_data["learning_config"],
                                       json_data["parameters"])
