from ...model import DBObject
from ...model import JobBuilder
from ...model import Job
from ...model import FLGroup
from ...model import Model
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ... import generate_unique_id
from ...device_selection import DeviceSelectorFactory

def get_device_selector(job_configuration):
    """
    :param job_configuration: JobConfiguration
    :return: DeviceSelector
    """
    factory = DeviceSelectorFactory()
    return factory.get_device_selector(job_configuration.get_device_selection_strategy())

def create_job(devices, parent_group_id, job_config):
    """
    :param devices: list
    :param parent_group_id: string
    :param job_config: JobConfiguration
    """
    job_id = generate_unique_id()

    builder = JobBuilder()
    builder.set_id(job_id)
    builder.set_parent_group_id(parent_group_id)
    builder.set_configuration(job_config.to_json())
    builder.set_devices(devices)

    return builder.build()

def start_job_controller(job_db,
                           group_db,
                           group_id,
                           job_config,
                           previous_job_id,
                           auth_context_processor):
    """
    :param job_db: DB
    :param group_db: DB
    :param group_id: string
    :param job_config: JobConfiguration
    :param previous_job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    group_device_list = group.get_device_list()
    if job_config.get_num_devices() > len(group_device_list):
        raise ValueError("Cannot start job with more devices than exist in group.")

    device_selector = get_device_selector(job_config)
    devices = device_selector.select_devices(group_device_list, job_config)

    new_job = create_job(devices, group_id, job_config)

    if previous_job_id == "":
        group.create_job_path(new_job.get_id())
        group.add_current_job_id(new_job.get_id())
    else:
        if not previous_job_id in group.get_current_job_ids():
            previous_job = DBObject.load_from_db(Job, previous_job_id, job_db)
            new_job.set_start_model(previous_job.get_end_model())

            group.add_current_job_id(new_job.get_id())

        group.add_job_to_path_prev_id(previous_job_id, new_job.get_id())

    new_job.save_to_db(job_db)
    group.save_to_db(group_db)

    return new_job.get_id()
