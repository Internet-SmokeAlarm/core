from abc import abstractmethod
from typing import List

from ..exception import raise_default_request_forbidden_error
from ..request_processor import AuthContextProcessor
from .utils.auth.conditions.abstract_condition import AbstractCondition


class AbstractController:

    def __init__(self, auth_context: AuthContextProcessor):
        self._auth_context = auth_context

    @property
    def auth_context(self) -> AuthContextProcessor:
        return self._auth_context

    def verify_auth(self) -> None:
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
                if not cond.verify(self._auth_context):
                    local_is_true = False

                    break

            if local_is_true:
                return

        raise_default_request_forbidden_error()

    @abstractmethod
    def get_auth_conditions(self) -> List[List[AbstractCondition]]:
        raise NotImplementedError("get_auth_conditions() is not implemented")

    @abstractmethod
    def execute_controller(self) -> any:
        raise NotImplementedError("execute_controller() is not implemented")

    def execute(self) -> any:
        self.verify_auth()

        return self.execute_controller()
