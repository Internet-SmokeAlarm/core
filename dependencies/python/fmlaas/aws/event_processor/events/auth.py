class AuthEvent:

    def __init__(self, token, method_arn, path_parameters, aws_account_id, rest_api_id, region, stage):
        """
        :param token: string
        :param method_arn: string
        :param path_parameters: dict
        :param aws_account_id: string
        :param rest_api_id: string
        :param region: string
        :param stage: string
        """
        self.token = token
        self.method_arn = method_arn
        self.path_parameters = path_parameters
        self.aws_account_id = aws_account_id
        self.rest_api_id = rest_api_id
        self.region = region
        self.stage = stage

    def get_token(self):
        """
        :return: string
        """
        return self.token

    def get_method_arn(self):
        """
        :return: string
        """
        return self.method_arn

    def get_path_parameters(self):
        """
        :return: dict
        """
        return self.path_parameters

    def get_aws_account_id(self):
        """
        :return: string
        """
        return self.aws_account_id

    def get_rest_api_id(self):
        """
        :return: string
        """
        return self.rest_api_id

    def get_region(self):
        """
        :return: string
        """
        return self.region

    def get_stage(self):
        """
        :return: string
        """
        return self.stage
