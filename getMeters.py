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

    table = dynamodb.Table('meter')
    response = table.scan()
    items = response['Items']
    resultbody = []
    resultbody.extend(response['Items']) 
    
    return {
        'statusCode': 200,
        'body': json.dumps(resultbody,separators=(',', ':'),cls=CustomJsonEncoder)
    }
