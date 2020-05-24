from .event_processor import EventProcessor
from .events import AuthEventBuilder


class AuthEventProcessor(EventProcessor):

    def process_event(self, json_data):
        auth_event_builder = AuthEventBuilder()

        method_arn = json_data["methodArn"]

        auth_event_builder.set_token(json_data["headers"]["Authorization"])
        auth_event_builder.set_method_arn(method_arn)
        auth_event_builder.set_path_parameters(json_data["pathParameters"])

        tmp = method_arn.split(':')
        apiGatewayArnTmp = tmp[5].split('/')

        auth_event_builder.set_aws_account_id(tmp[4])
        auth_event_builder.set_rest_api_id(apiGatewayArnTmp[0])
        auth_event_builder.set_region(tmp[3])
        auth_event_builder.set_stage(apiGatewayArnTmp[1])

        return auth_event_builder.build()
