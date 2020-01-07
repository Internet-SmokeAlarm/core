from ...model import DBObject
from ...model import FLGroup
from ...model import Round
from ...model import RoundStatus
from ...aws import trigger_lambda_function
from ...utils import get_aggregation_lambda_func_name

from .lambda_trigger_helper import generate_aggregation_func_payload

def models_uploaded_controller(group_db, round_db, models_uploaded):
    """
    :param group_db: DB
    :param round_db: DB
    :param models_uploaded: list(string)
    """
    for model in models_uploaded:
        model_name = model.get_name()
        handler_function = get_model_process_function(model_name)
        should_trigger_aggregation = handler_function(model_name, group_db, round_db)

        if should_trigger_aggregation:
            payload = generate_aggregation_func_payload(model_name.get_group_id(), model_name.get_round_id())

            trigger_lambda_function(
                get_aggregation_lambda_func_name(),
                model_name.get_group_id(),
                model_name.get_round_id())

def get_model_process_function(model_name):
    if model_name.is_initial_group_model():
        return handle_group_initial_model
    elif model_name.is_device_model_update():
        return handle_device_model_update
    elif model_name.is_round_aggregate_model():
        return handle_round_aggregate_model

def handle_group_initial_model(model, group_db, round_db):
    # TODO : Capture model information (including size) here
    return False

def handle_device_model_update(model, group_db, round_db):
    model.set_entity_id(model.get_name().get_device_id())

    round = DBObject.load_from_db(Round, model.get_name().get_round_id(), round_db)
    round.add_model(model)

    should_aggregate = not round.is_aggregation_in_progress() and round.should_aggregate()
    if should_aggregate:
        round.set_status(RoundStatus.AGGREGATION_IN_PROGRESS)

    round.save_to_db(round_db)

    return should_aggregate

def handle_round_aggregate_model(model, group_db, round_db):
    model.set_entity_id(model.get_name().get_round_id())

    round = DBObject.load_from_db(Round, model.get_name().get_round_id(), round_db)
    round.set_aggregate_model(model)
    round.complete()
    round.save_to_db(round_db)

    return False
