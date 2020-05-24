from ....model import Builder
from .auth import AuthEvent


class AuthEventBuilder(Builder):

    def __init__(self):
        self.token = None
        self.method_arn = None
        self.path_parameters = None
        self.aws_account_id = None
        self.rest_api_id = None
        self.region = None
        self.stage = None

    def set_token(self, token):
        """
        :param token: string
        """
        self.token = token

    def set_method_arn(self, method_arn):
        """
        :param method_arn: string
        """
        self.method_arn = method_arn

    def set_path_parameters(self, path_parameters):
        """
        :param path_parameters: dict
        """
        self.path_parameters = path_parameters

    def set_aws_account_id(self, aws_account_id):
        """
        :param aws_account_id: string
        """
        self.aws_account_id = aws_account_id

    def set_rest_api_id(self, rest_api_id):
        """
        :param rest_api_id: string
        """
        self.rest_api_id = rest_api_id

    def set_region(self, region):
        """
        :param region: string
        """
        self.region = region

    def set_stage(self, stage):
        """
        :param stage: string
        """
        self.stage = stage

    def build(self):
        self._validate_parameters()

        return AuthEvent(
            self.token,
            self.method_arn,
            self.path_parameters,
            self.aws_account_id,
            self.rest_api_id,
            self.region,
            self.stage)

    def _validate_parameters(self):
        if self.token is None:
            raise ValueError("Token must not be None")
        elif not isinstance(self.token, type("str")):
            raise ValueError("Token must be of type string")

        if self.method_arn is None:
            raise ValueError("Method ARN must not be None")
        elif not isinstance(self.method_arn, type("str")):
            raise ValueError("Method ARN must be of type string")

        if self.path_parameters is None:
            raise ValueError("Path Parameters must not be None")
        elif not isinstance(self.path_parameters, type({})):
            raise ValueError("Path Parameters must be of type dictionary")

        if self.aws_account_id is None:
            raise ValueError("AWS Account ID must not be None")
        elif not isinstance(self.aws_account_id, type("str")):
            raise ValueError("AWS Account ID must be of type string")

        if self.rest_api_id is None:
            raise ValueError("Rest API ID must not be None")
        elif not isinstance(self.rest_api_id, type("str")):
            raise ValueError("Rest API ID must be of type string")

        if self.region is None:
            raise ValueError("Region must not be None")
        elif not isinstance(self.region, type("str")):
            raise ValueError("Region must be of type string")

        if self.stage is None:
            raise ValueError("Stage must not be None")
        elif not isinstance(self.stage, type("str")):
            raise ValueError("Stage must be of type string")
