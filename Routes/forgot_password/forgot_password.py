from flask_restful import Resource, Api, reqparse
import bcrypt
from flask import Flask, request, Response, jsonify, Blueprint, render_template
from bson import json_util
from bson.objectid import ObjectId
import pymongo
import jwt
import datetime
import json
from functools import wraps
from flask_cors import cross_origin
from flask_mail import Mail, Message
import math
import random
from Database.Database import Database as mydb


forgot_password = Blueprint("forgot_password", __name__)
mail = Mail()


############################################


def generateOTP():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


##########################################################


@forgot_password.route("/forgot_password/OTP", methods=["POST", "GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def forgotpasswordOTP():

    if request.method == 'POST':
        data = request.get_json()
        email = data['email']

        my_collection = mydb["User"]
        myquery1 = {"email": email}

        user_document = my_collection.find_one(
            myquery1)  # Source User to add to the followers list

        if user_document == None:
            return Response(
                response=json.dumps(
                    {"message": "User not found"
                     }),
                status=404,
                mimetype="application/json"
            )
        else:
            OTP = generateOTP()

        collection = mydb["OTPs"]

        token = jwt.encode({'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=1440)}, "SecretKey1911")

        db_response = collection.insert_one(
            {'email': email, 'OTP': OTP, 'type': 'forgot_password', 'token': token})

        msg = Message(
            'Confirm Email', sender='mohamedmohsen96661@gmail.com', recipients=[email])
        msg.html = render_template(
            'reset_password.html', username=user_document['username'], OTP=OTP)
        mail.send(msg)

        return jsonify({"message": "OTP Sent", "OTP": OTP}), 200
    else:
        collection = mydb["OTPs"]
        OTP = request.args.get('OTP')
        email = request.args.get('email')
        db_response = collection.find_one(
            {'OTP': OTP, 'email': email, 'type': 'forgot_password'})
        if db_response == None:
            return jsonify({"message": "wrong OTP"}), 404
        else:
            token = db_response['token']
            collection.delete_one({'OTP': OTP})
            try:
                jwt.decode(token, "SecretKey1911", "HS256")
            except:
                return jsonify({'message': 'OTP Expired'}), 401

    return jsonify({
        "message": "Email verified",
        "email": email
    }), 200


@forgot_password.route("/forgot_password", methods=["PUT"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def change_password(current_user):
    # print(request.form["_id"])
    if request.method == 'PUT':
        try:
            data = request.get_json()
            password = data["password"]
            password_byte = bytes(password, "ascii")
            hashed_pw = bcrypt.hashpw(password_byte, bcrypt.gensalt())

            user_id = ObjectId(current_user["_id"])

            db_response = mydb.User.update_one(
                {"_id": user_id},
                {"$set": {"password": hashed_pw}}
            )

            user = mydb.User.find_one(user_id)
            del user['password']
            user["creation_date"] = user["creation_date"].date()
            user["creation_date"] = user["creation_date"].strftime("%Y-%m-%d")
            user["_id"] = str(user["_id"])
            return Response(
                response=json.dumps(
                    {"message": "The request was succesful"
                     }),
                status=200,
                mimetype="application/json")
        except Exception as ex:
            print("**********")
            print(ex)
            print("**********")


#############################################
