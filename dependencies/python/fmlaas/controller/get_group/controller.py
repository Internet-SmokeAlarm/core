from ...exception import raise_default_request_forbidden_error
from ...request_processor import AuthContextProcessor
from ...model import FLGroup
from ...model import DBObject

def get_group_controller(db_, group_id, auth_json):
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, db_)

    if not group.is_member(auth_context_processor.get_entity_id()):
        raise_default_request_forbidden_error()

    group_json = group.to_json()
    group_json["is_initial_model_set"] = group.is_initial_model_set()

    return group_json
