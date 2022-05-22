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
from flask_cors import cross_origin
from Database.Database import Database as mydb

# try:
#     app = Flask(__name__)
#     client = pymongo.MongoClient(
#         "mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
#     app.db = client.Twitter_new
# except:
#     print("can't connect")

# api = Api(app)

get_blocked_users = Blueprint('get_blocked_users', __name__)


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


@get_blocked_users.route("/block", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def blockuser(current_user):
    if request.method == 'GET':

        user_id = request.args.get('user_id')
        objInstance_user = ObjectId(user_id)

        my_collection = mydb["User"]
        myquery = {"_id": objInstance_user}
        user_document = my_collection.find_one(myquery)
        if not user_document:
            return {"message": "User Doesn't Exist"}, 404
        blocking_list = user_document['blocking']

        return {"blocking": blocking_list}


# if __name__ == "__main__":
#     app.run(port=8081, debug=True)
