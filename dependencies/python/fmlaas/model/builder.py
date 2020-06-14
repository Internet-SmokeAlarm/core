from abc import abstractmethod


class Builder:

    @abstractmethod
    def build(self):
        raise NotImplementedError("build() not implemented")

    @abstractmethod
    def _validate_paramaters(self):
        raise NotImplementedError("_validate_paramaters() not implemented")
