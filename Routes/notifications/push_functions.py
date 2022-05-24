from pyfcm import FCMNotification
from tokenize import String
from flask import Flask, jsonify,request
import pymongo
from bson.objectid import ObjectId
from datetime import date, datetime, timedelta
### integration
from Database.Database import Database as mydb
from flask_cors import cross_origin
from functools import wraps
import jwt

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]

############################ For Login ############################

# Will be used in the login to register the logged in device for each user in the database
def add_device_token_to_database(user_id,device_token):
        logged_in_user_id = ObjectId(user_id)
        users_collection = mydb["User"]
        myquery = {"_id": logged_in_user_id}
        new_value_query={ "$set": {'logged_device':device_token }}
        users_collection.update_one(myquery,new_value_query)
        return 'Device Token added'

############################ For Sending Notification ############################

# Return device token using user_id from database
def get_device_token(user_id):
    logged_in_user_id = ObjectId(user_id)
    users_collection = mydb["User"]
    myquery = {"_id": logged_in_user_id}
    user_doc = users_collection.find_one(myquery)
    logged_in_device_token = user_doc['logged_device']
    return logged_in_device_token

##############################################

## will be used in the sending notifications
def push_notification(device_token,message_title,message_body):
    push_service = FCMNotification(api_key="AAAACldZwsA:APA91bElQiXIN4lqQODAGOcS6l_LvWkbs7jQ00iIp39V4UEH5Raa4sbC5fpyPSMHQYMvqBQKiGts_TpHYC2x8svgPMYxNyhZ8rFMzkB8zpJmHmcbFQ_4orsVimEaSjXexf4go99AKjO3")

    registration_id = device_token
    #message_title = "User Like"
    #message_body = "Hi Ahmed, mark liked your tweet"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return result

########## just testing ###########
# result = push_notification()
# print (result)
