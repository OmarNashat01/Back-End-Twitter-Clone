from email import message
import json

import os
import bcrypt
import requests
from flask import Blueprint, request, jsonify, session, abort, redirect, request
from flask_cors import cross_origin
import jwt
import datetime
from Database.Database import Database
from functools import wraps
from bson.objectid import ObjectId



getblock = Blueprint("getblock" ,__name__)




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




@getblock.route("/block", methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def block_user(current_user):
    if current_user['admin'] == True:
        blocked_user_array = []
        db_response = Database.blocked_users.find({})
        #print(list(db_response))
        for i in db_response:
            try:
                jwt.decode(i['token'], "SecretKey1911", "HS256")
            except:
                print("exception")
                Database.blocked_users.delete_one({'token': i['token']})
                continue
            obj_id = ObjectId(i['_id'])
            print(obj_id)
            
            db_response = Database.User.find_one({'_id': obj_id})
            print(db_response)
            if 'password' in db_response:
                del db_response['password']
            if 'notifications' in db_response:
                del db_response['notifications']
            db_response["creation_date"] = db_response["creation_date"].date()
            db_response["creation_date"] = db_response["creation_date"].strftime("%Y-%m-%d")
            db_response["_id"] = str(db_response["_id"])
            db_responses = Database.blocked_users.find_one({'token': i['token']})
            db_response["unblock_date"] = db_responses['unblock_date']
            blocked_user_array.append(db_response)

        return jsonify({"blocked_users": blocked_user_array}),200
    else:
        return jsonify({"Message": "user is not admin"}), 403