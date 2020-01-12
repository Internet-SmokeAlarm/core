from ...model import DBObject
from ...model import RoundBuilder
from ...model import Round
from ...model import FLGroup
from ...model import Model
from ... import generate_unique_id
from ...device_selection import DeviceSelectorFactory

def get_device_selector(round_configuration):
    """
    :param round_configuration: RoundConfiguration
    :return: DeviceSelector
    """
    factory = DeviceSelectorFactory()
    return factory.get_device_selector(round_configuration.get_device_selection_strategy())

def create_round(devices, previous_round_id, start_model, round_config):
    """
    :param devices: list
    :param previous_round_id: string
    :param start_model: Model
    :param round_config: RoundConfiguration
    """
    round_id = generate_unique_id()

    builder = RoundBuilder()
    builder.set_id(round_id)
    builder.set_previous_round_id(previous_round_id)
    builder.set_configuration(round_config.to_json())
    builder.set_start_model(start_model.to_json())
    builder.set_devices(devices)

    return builder.build()

def start_round_controller(round_db, group_db, group_id, round_config):
    group = DBObject.load_from_db(FLGroup, group_id, group_db)

    device_selector = get_device_selector(round_config)
    devices = device_selector.select_devices(group.get_device_list(), round_config)

    previous_round_id = group.get_current_round_id()
    if previous_round_id != "N/A":
        previous_round = DBObject.load_from_db(Round, previous_round_id, round_db)
        previous_round.cancel()
        previous_round.save_to_db(round_db)

        new_round = create_round(devices, previous_round.get_id(), previous_round.get_end_model(), round_config)
    else:
        new_round = create_round(devices, previous_round_id, group.get_initial_model(), round_config)

    group.add_round(new_round.get_id())
    group.set_current_round_id(new_round.get_id())

    new_round.save_to_db(round_db)
    group.save_to_db(group_db)

    return new_round.get_id()
