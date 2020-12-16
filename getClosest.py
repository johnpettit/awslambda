import json
import boto3
from decimal import Decimal
import math

dynamodb = boto3.resource('dynamodb')
        
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)
        
def lambda_handler(event, context):
    if 'latitude' not in event['body']:
        return return_nokey_error()
    if 'longitude' not in event['body']:
        return return_nokey_error()
        
    pointOfUser = [event['body']['latitude'],event['body']['longitude']]
    lowestDistance = 0
    lowestItem = None
    
    # Get all meters
    table = dynamodb.Table('meter')
    response = table.scan()
    items = response['Items']
    for item in items:
        pointOfMeter = [float(item['latitude']), float(item['longitude'])]
        distance = math.sqrt( ((pointOfUser[0]-pointOfMeter[0])**2)+((pointOfUser[1]-pointOfMeter[1])**2) )

        if lowestDistance == 0:
            lowestDistance = distance
            lowestItem = item
        else:
            if distance < lowestDistance:
                lowestDistance = distance
                lowestItem = item
                
    lowestItem['distanceToMeter'] = lowestDistance

    return {
        'statusCode': 200,
        'body': json.dumps(lowestItem,separators=(',', ':'),cls=CustomJsonEncoder)
    }

def return_nokey_error():
    return {
        'statusCode': 400,
        'body': json.dumps('Missing Parameters')
    }
