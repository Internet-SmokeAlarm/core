from abc import abstractmethod
from ..model import ProjectPrivilegeTypesEnum
from ..exception import raise_default_request_forbidden_error


class AbstractController:

    def __init__(self, auth_context):
        """
        :param auth_context: AuthContextProcessor
        """
        self.auth_context = auth_context

    def verify_auth(self):
        """
        Verify each authorization condition is satisfied. If any
        conditions are not satisfied, will throw a request forbidden
        error.

        :param conditions: list(AuthorizationCondition)
        """
        conditions = self.get_auth_conditions()

        for cond in conditions:
            if not cond.verify(self.auth_context):
                raise_default_request_forbidden_error()

    def load_data(self):
        """
        Load data
        """
        pass

    @abstractmethod
    def get_auth_conditions(self):
        """
        :returns: list(AbstractCondition)
        """
        raise NotImplementedError("get_auth_conditions() is not implemented")

    def execute(self):
        self.load_data()
        self.verify_auth()

        return self.execute_controller()
