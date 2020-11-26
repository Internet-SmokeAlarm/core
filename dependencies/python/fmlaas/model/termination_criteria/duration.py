from ...utils import get_epoch_time
from .termination_criteria import TerminationCriteria


class DurationTerminationCriteria(TerminationCriteria):

    def __init__(self, max_duration_sec: int, start_epoch_time: int):
        self._max_duration_sec = max_duration_sec
        self._start_epoch_time = start_epoch_time

    @property
    def max_duration_sec(self) -> int:
        return self._max_duration_sec

    @property
    def start_epoch_time(self) -> int:
        return self._start_epoch_time

    def is_criteria_satisfied(self) -> bool:
        return get_epoch_time() - self._start_epoch_time >= self._max_duration_sec

    def reset(self) -> None:
        self._start_epoch_time = get_epoch_time()

    def to_json(self) -> dict:
        return {
            "type": DurationTerminationCriteria.__name__,
            "max_duration_sec": str(self._max_duration_sec),
            "start_epoch_time": str(self._start_epoch_time)
        }

    @staticmethod
    def from_json(json_data):
        # We do something special here...if we don't have a start epoch time,
        #   then we set it. Why? We don't want to fail to load json because
        #   the user didn't specify a start epoch time.
        if "start_epoch_time" in json_data:
            start_epoch_time = int(json_data["start_epoch_time"])
        else:
            start_epoch_time = get_epoch_time()

        return DurationTerminationCriteria(int(json_data["max_duration_sec"]),
                                           start_epoch_time)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._max_duration_sec == other._max_duration_sec) and \
            (self._start_epoch_time == other._start_epoch_time)