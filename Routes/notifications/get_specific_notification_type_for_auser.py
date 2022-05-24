import queue
from flask import Flask, jsonify,request,Blueprint
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
# app = Flask(__name__)

notification_by_type = Blueprint('notification_by_type', __name__)

#################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, "SecretKey1911", "HS256")
            user_id = ObjectId(data['_id'])
            current_user = mydb.User.find_one({'_id': user_id})

        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
########################################

@notification_by_type.route('/type')
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_specific_type_notification(current_user):
    user_id = request.args.get('user_id')
    notification_type = request.args.get('notification_type')
    types_list = ['block_event','tweet_liked_event' ,'user_tweeted_event']
    if notification_type not in types_list:
        return jsonify({"Error message": "Please, Select one of these types [block_event - tweet_liked_event - user_tweeted_event]"}) , 400
    ## targeting the given user
    user_collection = mydb['User']
    try:
        query = {"_id": ObjectId(user_id)}
    except:
        return jsonify({'Error Message: ': "Enter valid user id"}) , 400
    target_user_document = user_collection.find_one(query)
    
    if user_id == None:
        return jsonify({"Error message": "Please, Eneter a User ID"}) , 400

    if target_user_document == None:
        return jsonify({'Error Message: ': "User Not found"}) , 404
        
    ## Getting the notifications of specific Type
    list_to_return = []
    list_of_specific_type_notifications = target_user_document['notifications']
    for notification in list_of_specific_type_notifications:
        if len(list_of_specific_type_notifications) < 1:
            break
        if notification['type'] == notification_type:
            notification['_id'] = str(notification['_id'])
            list_to_return.append(notification)
        else:
            continue
    return jsonify({"notifications": list_to_return})


