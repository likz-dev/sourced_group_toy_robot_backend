import boto3
from botocore.exceptions import ClientError

from app.utils.secrets_manager import SecretsManager, SECRET_NAME_DATABASE, SECRET_STRING_DATABASE_NAME
from app.entities.robot import KEY_X, KEY_Y, KEY_FACING

KEY_SESSION_ID = 'session_id'


class ToyRobotSession:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        secrets_manager = SecretsManager()
        db_credentials = secrets_manager.get_value(SECRET_NAME_DATABASE)
        table_name = db_credentials.get(SECRET_STRING_DATABASE_NAME)

        self.table = self.dynamodb.Table(table_name)

    def put_session(self, session_id, robot):
        response = self.table.put_item(
            Item={
                KEY_SESSION_ID: session_id,
                KEY_X: robot.get(KEY_X),
                KEY_Y: robot.get(KEY_Y),
                KEY_FACING: robot.get(KEY_FACING)
            }
        )

        return response

    def get_session(self, session_id):
        try:
            response = self.table.get_item(Key={KEY_SESSION_ID: session_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def update_session(self, session_id, robot):
        response = self.table.update_item(
            Key={
                KEY_SESSION_ID: session_id
            },
            UpdateExpression=f'set {KEY_X}=:x, {KEY_Y}=:y, {KEY_FACING}=:facing',
            ExpressionAttributeValues={
                ':x': robot.get(KEY_X),
                ':y': robot.get(KEY_Y),
                ':facing': robot.get(KEY_FACING)
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
