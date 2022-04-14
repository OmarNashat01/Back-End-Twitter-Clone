import bcrypt
import jsonify
from flask import request, Response, jsonify, Blueprint
import jwt
import datetime

# For using the Database, use it as Database not app.db
from Database.Database import Database



Login = Blueprint('Login', __name__)


@Login.route("/", methods=['POST'])
def Home():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    password_byte = bytes(password, "ascii")
   
    isfound = Database.User.find_one({'email': email})

    if isfound:
    
         if bcrypt.checkpw(password_byte, isfound["password"]):

            token = jwt.encode({'user': isfound["name"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 59)}, "SecretKey1911") 
            return jsonify({'User found': True, 'token': token})

         else:

             return Response(
        response= "pasword doesn't match", 
        status = 400)
        
    else:

        return Response(
        response= "user not found", 
        status = 400)
