from ...database import DB
from ...model import (ApiKeyFactory, ApiKeyTypeEnum, DBObject, Project,
                      ProjectPrivilegeTypesEnum, DeviceFactory)
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class RegisterDeviceController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 key_db: DB,
                 project_id: str,
                 auth_context: AuthContextProcessor):
        super(RegisterDeviceController, self).__init__(auth_context)

        self._project_db = project_db
        self._key_db = key_db
        self._project_id = project_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        api_key, key_plaintext = ApiKeyFactory.create_api_key(self.auth_context.get_entity_id(),
                                                              ApiKeyTypeEnum.DEVICE)
        api_key.save_to_db(self._key_db)

        self._project.add_device(DeviceFactory.create_device(api_key.id))
        self._project.save_to_db(self._project_db)

        return api_key.id, key_plaintext
