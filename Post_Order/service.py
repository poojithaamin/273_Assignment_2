# -*- coding: utf-8 -*-
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
   menuId = event.get("menu_id")
   order_id = event.get("order_id")
   customer_name = event.get("customer_name")
   customer_email = event.get("customer_email")   
   item = {
       'order_id': {"S":order_id},
       'customer_name':{"S": customer_name},
       'customer_email':{"S": customer_email},
       'menu_id': {"S":menuId}
   }
   res = client.put_item(TableName= 'Order', Item = item)   
   data =  client.get_item(TableName='Menu', Key={'menu_id':{'S':menuId}})['Item']
   choice = data[u'selection']
   choiceList = choice[u'SS']
   for item in choiceList:
       count = count + 1
       temp = temp + str(count) + ". " + item + " "
       choiceDict[str(count)]=str(item).strip('')
 
   userChoice = "Hi " +customer_name + ", please choose one of these selections: " + temp    
   return userChoice