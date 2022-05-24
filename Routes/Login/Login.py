import json
import os
import bcrypt
import requests
from flask import Blueprint, request, jsonify, session, abort, redirect, request
from flask_cors import cross_origin
import jwt
import datetime
from Database.Database import Database
import math, random
import sys
sys.path.append("..")
from Routes.notifications.push_functions import add_device_token_to_database







Login = Blueprint("Login" ,__name__)




@Login.route("", methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def Home():
    Login_data = request.get_json()
    device_token = Login_data["device_token"]
    email = Login_data["email"]
    password = Login_data["password"]
    if password == None:
        password = "NULL"
    password_byte = bytes(password, "ascii")
    
    isfound = Database.User.find_one({'email': email})

    if isfound and password == "NULL":
        return jsonify({"message": "user found", "prof_pic_url": isfound["prof_pic_url"]}), 200
    elif isfound:
        if bcrypt.checkpw(password_byte, isfound["password"]):
            user_id = isfound['_id']
            user_id = str(user_id)
            admin = isfound["admin"]
            token = jwt.encode({'_id': str(isfound["_id"]), 'admin': admin, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 525600)}, "SecretKey1911") 
            add_device_token_to_database(user_id = user_id, device_token = device_token)
            return jsonify({'message': "user found", 'token': token, '_id': user_id, "admin": isfound["admin"] }), 201
        else:
            return jsonify({"message": "incorrect password"}), 400
    else:
            return jsonify({"message": "email doesn't exist"}),404




    







       

    


    



  
    
