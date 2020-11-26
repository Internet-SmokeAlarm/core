import unittest
from collections import namedtuple
from typing import Dict, List, Tuple

from dependencies.python.fmlaas.model import (ApiKey, DeviceFactory,
                                              Experiment, ExperimentFactory,
                                              JobConfiguration, JobFactory,
                                              Model, ProjectFactory,
                                              ProjectPrivilegeTypesEnum,
                                              UserFactory)
from dependencies.python.fmlaas.model.device_selection_strategy import \
    DeviceSelectionStrategy
from dependencies.python.fmlaas.model.experiment_configuration import (
    AggregationStrategy, DataCollectionConfig, ExperimentConfiguration,
    InitializationStrategy, MLType, Runtime)
from dependencies.python.fmlaas.s3_storage import StartModelPointer


class AbstractTestCase(unittest.TestCase):

    def _build_simple_project(self):
        project = ProjectFactory.create_project("test_id",
                                                "test_name")

        project.add_device(DeviceFactory.create_device("12344"))
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        return project
    
    def _build_simple_experiment(self,
                           id: str,
                           name: str = "exp_name",
                           description: str = "test description",
                           project_id: str = "test123") -> Tuple[Experiment, dict]:
        config_code = "Code!"
        config_learning_config = dict()
        config_parameters = Model("0", str(StartModelPointer.from_str(f"{project_id}/{id}/start_model")), 1234).to_json()
        config = ExperimentConfiguration(DataCollectionConfig.MINIMAL_RETAIN,
                                         Runtime.CUSTOM,
                                         AggregationStrategy.AVERAGE,
                                         MLType.NN,
                                         InitializationStrategy.CUSTOMER_PROVIDED,
                                         config_code,
                                         config_learning_config,
                                         config_parameters)

        experiment_json = {
            "ID" : id,
            "name": name,
            "description": description,
            "jobs" : dict(),
            "configuration": {
                "data_collection_config": DataCollectionConfig.MINIMAL_RETAIN.value,
                "runtime": Runtime.CUSTOM.value,
                "aggregation_strategy": AggregationStrategy.AVERAGE.value,
                "ml_type": MLType.NN.value,
                "initialization_strategy": InitializationStrategy.CUSTOMER_PROVIDED.value,
                "code": config_code,
                "learning_config": config_learning_config,
                "parameters": config_parameters
            },
            "current_job_id" : ""
        }

        return ExperimentFactory.create_experiment(id,
                                                   name,
                                                   description,
                                                   config), experiment_json

    def _build_simple_job(self):
        job_configuration = JobConfiguration(1, 0, DeviceSelectionStrategy.RANDOM, [])
        start_model = Model("12312414",
                            "12312414/start_model",
                            "123211")

        job = JobFactory.create_job("job_test_id",
                                     job_configuration,
                                     ["12344"])
        job.start_model = start_model

        return job

    def _build_simple_api_key(self):
        id = "fasdf234af21ad1ds5d66f64dl2jjsmc6"
        hash = "kgfldsxknjvdoi49f34sofgjna3qouthe03hQFDFH5gffdge"
        created_on = "123123.234"
        event_log = {}
        key_type = "USER"
        entity_id = "user_123442"
        api_key = ApiKey(id, hash, created_on, event_log, key_type, entity_id)

        ApiKeyTuple = namedtuple("ApiKeyTuple", "id hash created_on event_log key_type entity_id api_key")

        return ApiKeyTuple(id,
                           hash,
                           created_on,
                           event_log,
                           key_type,
                           entity_id,
                           api_key)

    def _create_empty_user(self, username: str = "valetolpegin"):
        user = UserFactory.create_user(username)
        user_json = {
            "ID": username,
            "projects": dict(),
            "api_keys": list()
        }

        return user, user_json
