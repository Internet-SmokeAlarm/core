import unittest
from typing import List
from typing import Dict
from collections import namedtuple
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import User
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum


class AbstractTestCase(unittest.TestCase):

    def _build_simple_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        return project

    def _build_simple_experiment(self):
        builder = ExperimentBuilder()
        builder.id = "test_id_2"

        return builder.build()

    def _build_simple_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_experiment_id("test_id_2")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_aggregate_model(
            Model(
                "1234",
                "1234/aggregate_model",
                "123211").to_json())
        job_builder.set_devices(["12344"])

        return job_builder.build()

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

    def _create_prefilled_user(self):
        username = "valetolpegin"
        projects = [
            {
                "id": "123123afsd1234saf23",
                "name": "vales_first_project"
            }
        ]
        api_keys = [
            "12312124afasdf24qfawqr",
            "46435dsfd4234dfgdfg4fg324dfsdf",
            "6y54ewfdsgsy54y0s0ddfsjd"
        ]

        return self._create_user_tuple(username,
                                       projects,
                                       api_keys)

    def _create_empty_user(self):
        username = "valetolpegin"
        projects = []
        api_keys = []

        return self._create_user_tuple(username,
                                       projects,
                                       api_keys)

    def _create_user_tuple(self,
                           username: str,
                           projects: List[Dict[str, str]],
                           api_keys: List[str]):
        user = User(username,
                    projects,
                    api_keys)

        user_json = {
            "ID": username,
            "projects": projects,
            "api_keys": api_keys
        }

        UserTuple = namedtuple("UserTuple", "username projects api_keys user user_json")

        return UserTuple(username,
                         projects,
                         api_keys,
                         user,
                         user_json)
