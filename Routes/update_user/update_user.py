from flask_restful import Resource, Api, reqparse
import bcrypt
from flask import Flask, request, Response, jsonify, Blueprint
from bson import json_util
from bson.objectid import ObjectId
import pymongo
import jwt
import datetime
import json
from functools import wraps
from Database.Database import Database as mydb

# try:
#     app = Flask(__name__)
#     client = pymongo.MongoClient(
#         "mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
#     app.db = client.Twitter_new
# except:
#     print("can't connect")

# api = Api(app)

update_user = Blueprint('update_user', __name__)

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


############################################

@update_user.route("/update_profile", methods=["PUT"])
@token_required
def updateuser(current_user):
    # print(request.form["_id"])
    try:
        data = request.get_json()
        name = data["name"]
        date_of_birth = data["date_of_birth"]
        bio = data["bio"]
        location = data["location"]
        website = data["website"]
        prof_pic_url = data["prof_pic_url"]
        cover_pic_url = data["cover_pic_url"]

        #query = {"_id": ObjectId(current_user["_id"])}
        #user = db.User.update_one(query)

        user_id = ObjectId(current_user["_id"])
        # print(user_id)
        db_response = mydb.User.update_one(
            {"_id": user_id},
            {"$set": {
                "name": name,
                "date_of_birth": date_of_birth,
                "bio": bio,
                "location": location,
                "website": website,
                "prof_pic_url": prof_pic_url,
                "cover_pic_url": cover_pic_url
            }}

        )

        user = mydb.User.find_one(user_id)
        del user['password']
        user["creation_date"] = user["creation_date"].date()
        user["creation_date"] = user["creation_date"].strftime("%Y-%m-%d")
        user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(
                {"message": "The request was succesful",
                 "user": user
                 }),
            status=200,
            mimetype="application/json")
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")


#############################################
# if __name__ == "__main__":
#     app.run(port=9090, debug=True)
