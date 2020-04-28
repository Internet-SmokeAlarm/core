from ...model import DBObject
from ...model import RoundBuilder
from ...model import Round
from ...model import FLGroup
from ...model import Model
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ... import generate_unique_id
from ...device_selection import DeviceSelectorFactory

def get_device_selector(round_configuration):
    """
    :param round_configuration: RoundConfiguration
    :return: DeviceSelector
    """
    factory = DeviceSelectorFactory()
    return factory.get_device_selector(round_configuration.get_device_selection_strategy())

def create_round(devices, parent_group_id, round_config):
    """
    :param devices: list
    :param parent_group_id: string
    :param round_config: RoundConfiguration
    """
    round_id = generate_unique_id()

    builder = RoundBuilder()
    builder.set_id(round_id)
    builder.set_parent_group_id(parent_group_id)
    builder.set_configuration(round_config.to_json())
    builder.set_devices(devices)

    return builder.build()

def start_round_controller(round_db,
                           group_db,
                           group_id,
                           round_config,
                           previous_round_id,
                           auth_context_processor):
    """
    :param round_db: DB
    :param group_db: DB
    :param group_id: string
    :param round_config: RoundConfiguration
    :param previous_round_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    group_device_list = group.get_device_list()
    if round_config.get_num_devices() > len(group_device_list):
        raise ValueError("Cannot start round with more devices than exist in group.")

    device_selector = get_device_selector(round_config)
    devices = device_selector.select_devices(group_device_list, round_config)

    new_round = create_round(devices, group_id, round_config)

    if previous_round_id == "":
        group.create_round_path(new_round.get_id())
        group.add_current_round_id(new_round.get_id())
    else:
        if not previous_round_id in group.get_current_round_ids():
            previous_round = DBObject.load_from_db(Round, previous_round_id, round_db)
            new_round.set_start_model(previous_round.get_end_model())

            group.add_current_round_id(new_round.get_id())

        group.add_round_to_path_prev_id(previous_round_id, new_round.get_id())

    new_round.save_to_db(round_db)
    group.save_to_db(group_db)

    return new_round.get_id()
