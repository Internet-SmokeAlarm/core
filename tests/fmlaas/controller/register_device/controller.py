from dependencies.python.fmlaas.controller.register_device import \
    RegisterDeviceController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (ApiKey, DBObject,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class RegisterDeviceControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = RegisterDeviceController(project_db_,
                                              key_db_,
                                              project.id,
                                              5,
                                              auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        devices = controller.execute()

        self.assertEqual(len(devices), 5)
        for id, key_plaintext in devices:
            self.assertIsNotNone(id)
            self.assertIsNotNone(key_plaintext)
            self.assertEqual(id, DBObject.load_from_db(ApiKey, id, key_db_).id)
