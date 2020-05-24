from abc import abstractmethod


class AggregationAlgorithm:

    @abstractmethod
    def combine_models(model_1, model_2):
        """
        Sums parameters from both models, with summed values in model_1.

        :param model_1: ordereddict
        :param model_2: ordereddict
        :returns: dict
        """
        raise NotImplementedError("combine_models() not implemented")

    @abstractmethod
    def scale_model(model, num_models):
        """
        Scale down model parameters based on the # of models that were aggregated.

        :param model: ordereddict
        :param num_models: int
        """
        raise NotImplementedError("scale_model() not implemented")
