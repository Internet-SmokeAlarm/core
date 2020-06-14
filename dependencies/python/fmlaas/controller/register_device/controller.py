from ...database import DB
from ...model import Project
from ...model import ApiKeyBuilder
from ...model import ApiKeyTypeEnum
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret
from ..abstract_controller import AbstractController


class RegisterDeviceController(AbstractController):

    def __init__(self, project_db: DB, key_db: DB, project_id: str, auth_context: AuthContextProcessor):
        super(RegisterDeviceController, self).__init__(auth_context)

        self.project_db = project_db
        self.key_db = key_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_key_type(ApiKeyTypeEnum.DEVICE.value)
        builder.set_entity_id(self.auth_context.get_entity_id())
        api_key = builder.build()
        api_key.save_to_db(self.key_db)

        self.project.add_device(api_key.get_id())
        self.project.save_to_db(self.project_db)

        return id, key_plaintext
