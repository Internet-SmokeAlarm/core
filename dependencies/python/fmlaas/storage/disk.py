import json

class DiskModelStorage:

    @staticmethod
    def store_model(file_obj, state_dict):
        """
        :param file_obj: file-like object
        :param state_dict: dictionary (Must be json serializable)
        """
        json.dump(state_dict, file_obj)

    @staticmethod
    def load_model(file_obj):
        """
        :param file_obj: file-like object
        :param state_dict: dictionary (Must be json serializable)
        """
        return json.load(file_obj)
