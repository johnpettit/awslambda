import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
        
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)
        
def lambda_handler(event, context):
    theid = event['params']['meterid']
    table = dynamodb.Table('meter')
    response = table.get_item(Key={'meterid':theid,})
    resultbody = response['Item']
    
    return {
        'statusCode': 200,
        'body': json.dumps(resultbody,separators=(',', ':'),cls=CustomJsonEncoder)
    }
