from unicodedata import name
import bcrypt
from flask import Flask, request, Response, jsonify
from pymongo import MongoClient
import jwt
import datetime


try:
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
    app.db = client.Twitter_new
except: 
    print("can't connect")



@app.route("/Login", methods=['POST'])
def Home():
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        password_byte = bytes(password, "ascii")
       
        isfound = app.db.User.find_one({'email': email})

        if isfound:
             if 'admin' in isfound:
                 admin = isfound['admin']
             else:
                 admin = False
             if bcrypt.checkpw(password_byte, isfound["password"]):
                
                token = jwt.encode({'user_id': str(isfound["_id"]), 'Admin': admin, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 1440)}, "SecretKey1911") 
                return jsonify({'User found': True, 'token': token})

             else:

                 return jsonify({"400": "password doesn't match"}),400
            
        else: 

            return jsonify({"400": "user not found"}),400
            
    

  
    