from abc import abstractmethod

class TerminationCriteria:

    @abstractmethod
    def is_criteria_satisfied(self, round):
        """
        Checks to see whether the passed round satisfies this termination criteria.

        :return: boolean. True if the round should be terminated
        """
        raise NotImplementedError("is_criteria_satisfied() not implemented")

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("to_json() not implemented")
