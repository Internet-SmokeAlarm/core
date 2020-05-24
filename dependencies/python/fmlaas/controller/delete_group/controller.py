from ...model import FLGroup
from ...model import DBObject
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error

def delete_group_controller(group_db, job_db, group_id, auth_context_processor):
    """
    :param group_db: DB
    :param job_db: DB
    :param group_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    try:
        group = DBObject.load_from_db(FLGroup, group_id, group_db)
    except:
        raise_default_request_forbidden_error()

    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.ADMIN):
        raise_default_request_forbidden_error()

    job_ids = group.get_job_info().keys()
    for job_id in job_ids:
        job_db.delete_object(job_id)

    group_db.delete_object(group_id)
