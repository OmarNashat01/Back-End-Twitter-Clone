import bcrypt
from flask import Blueprint, request, jsonify, render_template
from flask_cors import cross_origin
import datetime
from flask_mail import Mail, Message
import jwt
import math, random
from Database.Database import Database
#from app import mail
#from app import app


signup = Blueprint("signup" ,__name__)
mail = Mail()


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




@signup.route("/verify", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def verify():   
    user_email = request.get_json()
    email = user_email["email"]
    isfound = Database.User.find_one({'email': email})
    #isExists = validate_email(email, verify=True)
    if isfound:
        return jsonify({"email status": "Email does already exist"}), 400

    #elif isExists == False:
        #return jsonify({"404": "Email doesn't exist"}), 404 
        #GENERATING TOO MANY ERRORS, WILL BE CONSIDERED LATER

    else:
        OTP = generateOTP()
        token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 1440)},"SecretKey1911")
        Database.OTPs.insert_one({"OTP":OTP,"token": token, "email": email})
        msg = Message('Confirm Email', sender='mohamedmohsen96661@gmail.com', recipients=[email])
        msg.html = render_template('OTP_EMAIL.html',OTP=OTP)
        mail.send(msg)
        return jsonify({"message": "OTP Sent",
        "OTP": OTP}), 200




       

@signup.route("/", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def home():
    user_data = request.get_json() 
    email = user_data["email"]
    username = user_data["username"]
    gender = user_data["gender"]
    name = user_data["name"]
    location = user_data["location"]
    website = user_data["website"]
    date_of_birth = user_data["date_of_birth"]
    password = user_data["password"]
    password_byte = bytes(password, "ascii")
    hashed_pw = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    isfound = Database.User.find_one({"username": username})
    creation_date = datetime.datetime.now()
    if isfound == None:
        following = []
        followers = []
        Database.User.insert_one({
            "email": email,
            "password": hashed_pw,
            "name": name,
            "username": username,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "creation_date": creation_date,
            "admin": False,
            "bio": None,
            "webiste": website,
            "location": location,
            "prof_pic_url": "https://pbs.twimg.com/media/EEI178KWsAEC79p.jpg",
            "cover_pic_url": "https://i.pinimg.com/564x/a2/64/b4/a264b464b6fd6138d972448e19ba764d.jpg",
            "following_count": 0,
            "followers_count": 0,
            "following": following,
            "followers": followers,
            "tweet_count": 0 
            })
    
        return jsonify({"message": "Successufly inserted new user"}),200
    else:
        return jsonify({"messsage": "username exists"}),400


    



@signup.route('/confirm_email', methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
def confirm_email():
    OTP = request.args.get('OTP')
    email = request.args.get('email')
    OTP_ON_DB = Database.OTPs.find_one({"OTP": OTP})
    if not OTP_ON_DB or email != OTP_ON_DB["email"] :
        return jsonify({"message": "OTP IS Invalid"}), 404
    else:
        Token = OTP_ON_DB["token"]
        email = OTP_ON_DB["email"]
        Database.OTPs.delete_one({"OTP": OTP})
        try: 
            data = jwt.decode(Token, "SecretKey1911", "HS256")
        except:
            return jsonify({'message': 'OTP Expired'}), 401

    return jsonify({
        "message": "Email verifiedd",
        "email": email
    }), 200
    
    



