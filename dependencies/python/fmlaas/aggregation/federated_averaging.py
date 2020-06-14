from .aggregation_algo import AggregationAlgorithm


class FederatedAveraging(AggregationAlgorithm):

    def average_nn_parameters(self, parameters):
        """
        Averages passed parameters.

        :param parameters: nn model named parameters
        :type parameters: list
        """
        new_params = {}
        for name in parameters[0].keys():
            new_params[name] = sum([param[name] for param in parameters])

        return new_params

    def combine_models(self, model_1, model_2):
        return self.average_nn_parameters([model_1, model_2])

    def scale_model(self, model, num_models):
        new_params = {}
        for name in model.keys():
            new_params[name] = model[name] / num_models

        return new_params
