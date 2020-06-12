from abc import abstractmethod
from ..model import ProjectPrivilegeTypesEnum
from ..exception import raise_default_request_forbidden_error
from ..request_processor import AuthContextProcessor

class AbstractController:

    def __init__(self, auth_context: AuthContextProcessor):
        self.auth_context = auth_context

    def verify_auth(self):
        """
        Verify each authorization condition is satisfied. If any
        conditions are not satisfied, will throw a request forbidden
        error.

        Each inner list is ANDed, and the outer lists are ORed.
        """
        conditions = self.get_auth_conditions()

        for cond_group in conditions:
            local_is_true = True
            for cond in cond_group:
                if not cond.verify(self.auth_context):
                    local_is_true = False

                    break

            if local_is_true:
                return

        raise_default_request_forbidden_error()

    def load_data(self):
        """
        Load data
        """
        pass

    @abstractmethod
    def get_auth_conditions(self):
        """
        :returns: list(list(AbstractCondition))
        """
        raise NotImplementedError("get_auth_conditions() is not implemented")

    @abstractmethod
    def execute_controller(self):
        raise NotImplementedError("execute_controller() is not implemented")

    def execute(self):
        self.load_data()
        self.verify_auth()

        return self.execute_controller()
