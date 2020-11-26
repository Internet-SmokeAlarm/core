import unittest
from typing import Tuple

from dependencies.python.fmlaas.model import (ApiKeyFactory, ApiKeyTypeEnum,
                                              Experiment, ExperimentFactory,
                                              JobConfiguration, JobFactory,
                                              Model, ProjectFactory, Status, Device)
from dependencies.python.fmlaas.model.api_key_type import ApiKeyTypeEnum
from dependencies.python.fmlaas.model.device_factory import DeviceFactory
from dependencies.python.fmlaas.model.device_selection_strategy import \
    DeviceSelectionStrategy
from dependencies.python.fmlaas.model.experiment_configuration import (
    AggregationStrategy, DataCollectionConfig, ExperimentConfiguration,
    InitializationStrategy, MLType, Runtime)
from dependencies.python.fmlaas.model.user_factory import UserFactory
from dependencies.python.fmlaas.s3_storage import (JobAggregateModelPointer,
                                                   StartModelPointer)


class AbstractModelTestCase(unittest.TestCase):

    def _create_test_user(self, username: str = "valetolpegin"):
        user = UserFactory.create_user(username)
        user_json = {
            "ID": username,
            "projects": dict(),
            "api_keys": list()
        }

        return user, user_json

    def _create_api_key(self, entity_id: str = "123123"):
        res = ApiKeyFactory.create_api_key(entity_id, ApiKeyTypeEnum.USER)

        return res[0], res[1]
    
    def _create_job(self, id: str):
        job_config = JobConfiguration(2, 0, DeviceSelectionStrategy.RANDOM, [])
        devices = ["123", "234"]

        job = JobFactory.create_job(id,
                                    job_config,
                                    devices)

        job_json = {
            "ID": id,
            "status": Status.INITIALIZED.value,
            "devices": devices,
            "aggregate_model": dict(),
            "start_model": dict(),
            "configuration": job_config.to_json(),
            "models": dict(),
            "created_at": str(job.created_at),
            "billable_size": "0",
            "testing_reports": dict()
        }

        return job, job_json
    
    def _create_device(self, id: str) -> Device:        
        return DeviceFactory.create_device(id)
    
    def _create_experiment(self,
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

    def _create_project(self, id: str):
        name = "test_name"
        description = "test_description"

        json_repr = {
            "name": name,
            "ID": id,
            "devices": dict(),
            "experiments": dict(),
            "members": dict(),
            "billing": dict(),
            "description": description
        }

        project = ProjectFactory.create_project(id, name, description)

        return project, json_repr

    def _create_model(self):
        entity_id = "1234"
        size = 123552
        name = str(JobAggregateModelPointer("4456", "5567", "1234"))

        json_repr = {
            "entity_id": entity_id,
            "name": name,
            "size": str(size)
        }
        
        model = Model(entity_id, name, size)

        return model, json_repr
