from tokenize import String
from flask import Flask, jsonify,request
import pymongo
from bson.objectid import ObjectId
from datetime import date, datetime, timedelta
from Routes.notifications.push_functions import get_device_token , push_notification
### integration
from Database.Database import Database as mydb
from flask_cors import cross_origin
from functools import wraps
import jwt

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]


######################### Sending Notifications with defined arguments for each case #############################
# Notification Types (block_event - tweet_liked_event - user_tweeted_event)


def send_notification(user_receiving_id='',notification_type='',block_duration = 0,liker_name='',user_tweeted_id =''):
    type = notification_type
    creation_date = datetime.now()
    reciver_id = user_receiving_id
    body = ''

############# User got blocked ##############
   
    if type == 'block_event':
        ## Configuring the notification 

        body = 'Enjoy your {} minutes block'.format(block_duration)
        notification = {"_id": ObjectId(),'user_id': reciver_id,'type':type,'creation_date': creation_date,'message': body}

        ######## Datebase Queries ###########
        #notifications_collection=mydb["notifications"]
        #notifications_collection.insert_one(notification)

        # adding a notification to the notifications list of the user using user_id
        users_collection = mydb["User"]
        user_query = {"_id": ObjectId(reciver_id)}

        ## could use addToSet which only pushes if element doesnt exist
        myquery={ "$push": {'notifications':notification }}
        users_collection.update_one(user_query,myquery)
        device_token_returned = get_device_token(user_receiving_id)
        push_notification(device_token= device_token_returned,message_title=type,message_body=body)

        return body

############# User liked a tweet ##############

    elif type == 'tweet_liked_event':
        body = '{} liked your tweet'.format(liker_name)

        notification = {"_id": ObjectId(),'user_id': reciver_id,'type':type,'creation_date': creation_date,'message': body}
        users_collection = mydb["User"]
        user_query = {"_id": ObjectId(reciver_id)}

        ## could use $addToSet which only pushes if element doesnt exist
        myquery={ "$push": {'notifications':notification }}
        users_collection.update_one(user_query,myquery)
        device_token_returned = get_device_token(user_receiving_id)
        push_notification(device_token= device_token_returned,message_title=type,message_body=body)
        return body

############# User Tweeted ##############
        
    elif type == 'user_tweeted_event':
        #test = []
        ## Retriving the user name and followers
        user_tweeted_id_object = ObjectId(user_tweeted_id)
        users_collection = mydb["User"]
        myquery = {"_id": user_tweeted_id_object}
        user_document = users_collection.find_one(myquery) 
        display_name = user_document['username']
        body = 'Recent Tweet from {}'.format(display_name)  ## Body of the notification with the username of tweet owner 
        #########
        followers_list = user_document['followers']

        for user in followers_list:
            reciver_id = user['user_id']
            user_query = {"_id": ObjectId(reciver_id)}
            notification = {"_id": ObjectId(),'user_id': reciver_id,'type':type,'creation_date': creation_date,'message': body}
            myquery={ "$push": {'notifications':notification }}
            users_collection.update_one(user_query,myquery)
            device_token_returned = get_device_token(reciver_id)
            push_notification(device_token= device_token_returned,message_title=type,message_body=body)
            #test.append(notification['message'])

        return 'Done'
