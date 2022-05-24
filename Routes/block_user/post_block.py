from email import message
import json

import os
from unicodedata import digit
import bcrypt
import requests
from flask import Blueprint, request, jsonify, session, abort, redirect, request
from flask_cors import cross_origin
import jwt
import datetime
from Database.Database import Database
from functools import wraps
from bson.objectid import ObjectId
import sys
sys.path.append("..")
from notifications.Send_notifications import send_notification



block = Blueprint("block" ,__name__)




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
            current_user = Database.User.find_one({'_id': user_id})

        except:
            return jsonify({'message': 'Token is invalid!'}), 401


        return f(current_user, *args, **kwargs)
       
    return decorated




@block.route("/block", methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def block_user(current_user):
    user_data = request.get_json()
    user_id = user_data["_id"]
    duration_in_minutes = user_data["minutes"]
    duration_in_minutes = int(duration_in_minutes)

    db_response = Database.User.find_one({"_id": ObjectId(user_id)})
    if db_response == None:
        return jsonify({"message": 'Target user ID not found'}), 404

    if current_user['admin'] == True:
        db_response = Database.blocked_users.find_one({'_id': user_id})
        if db_response == None:
            token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= duration_in_minutes)}, "SecretKey1911")
            date_blocked = datetime.datetime.utcnow() + datetime.timedelta(minutes= duration_in_minutes + 120)
            date_time = date_blocked.strftime("%Y-%m-%d, %H:%M")
            db_response = Database.blocked_users.insert_one({'_id': user_id, 'token':token, 'unblock_date': date_time })
            send_notification(user_receiving_id = user_id, block_duration = int(duration_in_minutes), notification_type="block_event")
            return jsonify({"message": "The request was successful"}),200
        else:
            check_token = db_response['token']
            try:
                jwt.decode(check_token, "SecretKey1911", "HS256")
            except:
                db_response = Database.blocked_users.delete_one({'_id': user_id})
                token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= duration_in_minutes)}, "SecretKey1911")
                db_response = Database.blocked_users.insert_one({'_id': user_id, 'token': token})
                send_notification(user_receiving_id = user_id, block_duration = int(duration_in_minutes), notification_type="block_event")
                return jsonify({"message": "The request was successful"}),200

        return jsonify({"message": "user is already blocked"}),400
    else:
        return jsonify({"message": "user is not admin"}),401



    
        
        

