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
  
    params = event.get("params")
    order_id = params.get(u'order-id')
  
    body = event.get("body")
    user_input = body.get("input")
   
    
    orderData =  client.get_item(TableName='Order', Key={'order_id':{'S':order_id}})['Item']
    menu_id = orderData[u'menu_id']
    menu_id = menu_id[u'S']
   
    menuData =  client.get_item(TableName='Menu', Key={'menu_id':{'S':menu_id}})['Item']

    choice = menuData[u'selection']
    choiceList = choice[u'SS']   

    for item in choiceList:
        count = count + 1
        temp = temp + str(count) + ". " + item + " "
        choiceDict[str(count)]=str(item).strip('')

    size = menuData[u'Size']
    sizeList = size[u'SS']
   
    temp = ''
    count = 0
    for item in sizeList:
        count = count + 1
        temp = temp + str(count) + ". " + item + " "
        sizeDict[str(count)]=str(item).strip('')

    if not 'orderD' in orderData:

        userChoice = choiceDict[user_input]
        
        client.update_item(TableName="Order",
                           Key={"order_id":{"S":order_id}},
                           UpdateExpression="SET orderD = :ord",
                           ExpressionAttributeValues=
                           {":ord": {"M":{"selection": {"S":userChoice}
                 }}})
        
        selectSize = "Which size do you want? " + temp
        message = selectSize
    else:
        price = menuData[u'price']
        priceList = price[u'NS']
        count = 0
        sizeIn = user_input
        sel = orderData[u'orderD']
        sel = sel[u'M']
        sel = sel[u'selection']
        sel = sel[u'S']
        
        
        for item in priceList:
            count = count +1
            priceDict[str(count)]=str(item).strip('')
       
        orderDate = time.strftime("%m-%d-%y")  
        orderTime = time.strftime("%H:%M:%S")
        orderTimestamp = orderDate + "@" + orderTime
       
        orderItem = {
             
                 "selection": {"S":sel},
                 "size": {"S":sizeDict[sizeIn]},
                 "costs":{"S":priceDict[sizeIn]},
                 "order_time": {"S":orderTimestamp}
             }
         
        client.update_item(TableName="Order",
                           Key={"order_id":{"S":order_id}},
                           UpdateExpression="SET orderD = :ord, order_status =:sts",
                           ExpressionAttributeValues=
                           {":ord": {"M":orderItem}, ":sts":{"S":"processing"}
                           })        
        message =  "Your order costs $" + priceDict[sizeIn] + ". We will email you when the order is ready. Thank you!"        
    return message      