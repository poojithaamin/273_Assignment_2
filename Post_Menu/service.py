
# -- coding: utf-8 --
import boto3
import json
import time
print "loading function..."
def handler(event, context):
   count = 0
   temp = ''
   choiceDict = {}
   sizeDict={}
   priceDict={}   
   client = boto3.client('dynamodb',region_name='us-east-2', aws_access_key_id='AKIAI4MVIAVBQGCMSEKA', aws_secret_access_key='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')
   store_hours={}
   for item in event["store_hours"]:
       shDict1=dict()
       shDict1["S"] = event["store_hours"][item]
       store_hours[item] = shDict1
   item ={"menu_id":{"S":event["menu_id"]},
        "store_name": {"S":event["store_name"]},
        "selection":{"SS":event["selection"]},
        "size":{"SS":event["size"]},
        "price":{"NS":event["price"]},
        "store_hours":{"M":store_hours}}
 
   client.put_item(TableName="Menu", Item= item)
   return "ok"