from abc import abstractmethod


class TerminationCriteria:

    @abstractmethod
    def is_criteria_satisfied(self) -> bool:
        raise NotImplementedError("is_criteria_satisfied() not implemented")

    @abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError("to_json() not implemented")

    @abstractmethod
    def reset(self) -> None:
        """
        Resets the termination criteria data.

        Designed for timing resets which occur when a round is prescheduled but not run
        until far later after the scheduling.
        """
        raise NotImplementedError("reset() not implemented")
