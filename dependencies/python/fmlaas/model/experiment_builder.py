from .experiment import Experiment
from .builder import Builder


class ExperimentBuilder(Builder):

    def __init__(self):
        self._id = None
        self._jobs = []
        self._hyperparameters = {}
        self._current_job = "NONE"
        self._start_model = {}
        self._current_model = {}
        self._is_active = False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        """
        :param value: string
        """
        self._id = value

    def build(self):
        self._validate_parameters()

        return Experiment(
            self._id,
            self._jobs,
            self._hyperparameters,
            self._current_job,
            self._start_model,
            self._current_model,
            self._is_active)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif not isinstance(self.id, type("str")):
            raise ValueError("ID must be type string")
