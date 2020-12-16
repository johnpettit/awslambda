import sys
import json
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    
    item_count = 0
    
    #Read Json File
    with open('data.json') as json_file:
       meterdata = json.load(json_file)
       for meter in meterdata:
          isoccupied = meter['isOccupied']
          meternumber = meter['meter']['number']
          meteraddress = meter['meter']['address']
          latitude = meter['meter']['location'][0]
          longitude = meter['meter']['location'][1]
          timestamp = meter['timestamp']
          
          # build md5() idhash 
          theidH = hashlib.md5(str(meternumber).encode()+meteraddress.encode()+str(latitude).encode()+str(longitude).encode())
          theid = theidH.hexdigest()

          table = dynamodb.Table('meter')
          table.put_item(
            Item={
              'meterid': theid,
              'lastdata': timestamp,
              'isoccupied': isoccupied,
              'address': meteraddress,
              'number': meternumber,
              'latitude': latitude,
              'longitude': longitude
            }
          )
    
          #Insert data point into Dynamo
          table = dynamodb.Table('meterdata')
          table.put_item(
            Item={
                'meterid': theid,
                'timestamp': timestamp,
                'isoccupied': isoccupied
            }
          )
          item_count += 1

    return "Added %d items to DynamoDB: " %(item_count)
