from ...model import DBObject
from ...model import FLGroup
from ...model import Round

def update_round_path(current_round, round_db, group_db):
    """
    Removes the current_round object from a group's active rounds, identifies
    the next round that should be initialized in sequence (if any), and activates it.

    :param current_round: Round
    :param round_db: DB
    :param group_db: DB
    """
    group = DBObject.load_from_db(FLGroup, current_round.get_parent_group_id(), group_db)
    group.remove_current_round_id(current_round.get_id())

    round_id = group.get_next_round_in_sequence(current_round.get_id())
    while round_id is not None:
        round = DBObject.load_from_db(Round, round_id, round_db)
        if not round.is_cancelled():
            group.add_current_round_id(round_id)

            round.set_start_model(current_round.get_end_model())
            round.reset_termination_criteria()
            round.save_to_db(round_db)

            break

        round_id = group.get_next_round_in_sequence(round_id)

    group.save_to_db(group_db)

    return

def termination_check(current_round, round_db, group_db):
    """
    Checks to see whether or not the current round should be terminated. If so,
    handle termination, and update.

    :param current_round: Round
    :param round_db: DB
    :param group_db: DB
    """
    if current_round.should_terminate():
        current_round.cancel()

        update_round_path(current_round, round_db, group_db)

        current_round.save_to_db(round_db)
