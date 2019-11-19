
def average_nn_parameters(parameters):
    """
    Averages passed parameters.

    :param parameters: nn model named parameters
    :type parameters: list
    """
    new_params = {}
    for name in parameters[0].keys():
        new_params[name] = sum([param[name] for param in parameters])

    return new_params

def combine_models(model_1, model_2):
    """
    Sums parameters from both models, with summed values in model_1.

    :param model_1: ordereddict
    :param model_2: ordereddict
    :returns: dict
    """
    return average_nn_parameters([model_1, model_2])

def scale_model(model, num_models):
    """
    Scale down model parameters based on the # of models that were aggregated.

    :param model: ordereddict
    :param num_models: int
    """
    new_params = {}
    for name in model.keys():
        new_params[name] = model[name] / num_models

    return new_params
