from ...model import DBObject
from ...model import JobBuilder
from ...model import Job
from ...model import Project
from ...model import Model
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ... import generate_unique_id
from ...device_selection import DeviceSelectorFactory


def get_device_selector(job_configuration):
    """
    :param job_configuration: JobConfiguration
    :return: DeviceSelector
    """
    factory = DeviceSelectorFactory()
    return factory.get_device_selector(
        job_configuration.get_device_selection_strategy())


def create_job(devices, parent_project_id, job_config):
    """
    :param devices: list
    :param parent_project_id: string
    :param job_config: JobConfiguration
    """
    job_id = generate_unique_id()

    builder = JobBuilder()
    builder.set_id(job_id)
    builder.set_parent_project_id(parent_project_id)
    builder.set_configuration(job_config.to_json())
    builder.set_devices(devices)

    return builder.build()


def start_job_controller(job_db,
                         project_db,
                         project_id,
                         job_config,
                         previous_job_id,
                         auth_context_processor):
    """
    :param job_db: DB
    :param project_db: DB
    :param project_id: string
    :param job_config: JobConfiguration
    :param previous_job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    project = DBObject.load_from_db(Project, project_id, project_db)
    if not project.does_member_have_auth(
            auth_context_processor.get_entity_id(), ProjectPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    project_device_list = project.get_device_list()
    if job_config.get_num_devices() > len(project_device_list):
        raise ValueError(
            "Cannot start job with more devices than exist in project.")

    device_selector = get_device_selector(job_config)
    devices = device_selector.select_devices(project_device_list, job_config)

    new_job = create_job(devices, project_id, job_config)

    if previous_job_id == "":
        project.create_job_path(new_job.get_id())
        project.add_current_job_id(new_job.get_id())
    else:
        if not previous_job_id in project.get_current_job_ids():
            previous_job = DBObject.load_from_db(Job, previous_job_id, job_db)
            new_job.set_start_model(previous_job.get_end_model())

            project.add_current_job_id(new_job.get_id())

        project.add_job_to_path_prev_id(previous_job_id, new_job.get_id())

    new_job.save_to_db(job_db)
    project.save_to_db(project_db)

    return new_job.get_id()
