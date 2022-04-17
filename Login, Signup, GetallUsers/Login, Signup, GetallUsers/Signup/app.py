from unicodedata import name
import bcrypt
from flask import Flask, request, jsonify, url_for, render_template, Response
from pymongo import MongoClient
import datetime
from flask_mail import Mail, Message
import jwt
from bson import ObjectId
import requests
import math, random


app = Flask(__name__)
client = MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")

app.db = client.Twitter_new
client.server_info()
app.config.from_pyfile('config.cfg')
mail = Mail(app)


# function to generate OTP
def generateOTP():
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP




@app.route("/verify", methods=["GET"])
def verify():   
    data = request.get_json()
    email = data["email"]
    isfound = app.db.User.find_one({'email': email})
    #isExists = validate_email(email, verify=True)
    if isfound:
        return jsonify({"400": "Email does already exist"}), 400

    #elif isExists == False:
        #return jsonify({"404": "Email doesn't exist"}), 404 
        #GENERATING TOO MANY ERRORS, WILL BE CONSIDERED LATER

    else:
        OTP = generateOTP()
        token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 120)},"SecretKey1911")
        app.db.OTPs.insert_one({"OTP":OTP,"token": token, "email": email})
        msg = Message('Confirm Email', sender='mohamedmohsen96661@gmail.com', recipients=[email])
        msg.html = render_template('OTP_EMAIL.html',OTP=OTP)
        mail.send(msg)
        return jsonify({"200": "OTP Sent",
        "OTP": OTP}), 200




       

@app.route("/signup", methods=["POST"])
def home():
    data = request.get_json() 
    email = data["email"]
    username = data["username"]
    name = data["name"]
    date_of_birth = data["date_of_birth"]
    password = data["password"]
    password_byte = bytes(password, "ascii")
    hashed_pw = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    isfound = app.db.User.find_one({"username": username})
    if isfound == None:
        app.db.User.insert_one({
            "email": email,
            "password": hashed_pw,
            "name": name,
            "username": username,
            "date_of_birth": date_of_birth,
            "creation_date": datetime.datetime.now(),
            "admin": False,
            "profile_picture_url": "https://hips.hearstapps.com/digitalspyuk.cdnds.net/17/13/1490989105-twitter1.jpg?resize=480:*"
            })
    
        return jsonify({"200": "Successufly inserted new user"}),200
    else:
        return jsonify({"400": "username exists"}),400


    



@app.route('/confirm_email', methods=["GET"])
def confirm_email():
    OTP = request.args.get('OTP')
    email = request.args.get('email')
    OTP_ON_DB = app.db.OTPs.find_one({"OTP": OTP})
    if not OTP_ON_DB or email != OTP_ON_DB["email"] :
        return jsonify({"404": "OTP IS Invalid"}), 404
    else:
        Token = OTP_ON_DB["token"]
        email = OTP_ON_DB["email"]
        app.db.OTPs.delete_one({"OTP": OTP})
        try: 
            data = jwt.decode(Token, "SecretKey1911", "HS256")
        except:
            return jsonify({'401': 'OTP expired!'}), 401

    return jsonify({
        "200": "Email verified",
        "email": email
    }), 200
    
    



