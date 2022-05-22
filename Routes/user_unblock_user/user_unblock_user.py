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

user_unblock_user = Blueprint('user_unblock_user', __name__)


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


@user_unblock_user.route("/block", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def singleuser(current_user):
    # print(request.args["_id"])
    my_collection = mydb["User"]

    source_user = request.args.get('source_user_id')
    target_user = request.args.get('target_user_id')
    try:
        objInstance_source = ObjectId(source_user)
        objInstance_target = ObjectId(target_user)
    except:
        return jsonify({"message": "Please, Enter a valid User ID"}), 400

    myquery1 = {"_id": objInstance_source}
    myquery2 = {"_id": objInstance_target}

    filter = {"_id": 0, 'password': 0}
    source_user_document = my_collection.find_one(
        myquery1, filter)  # Source User to add to the followers list
    target_user_document = my_collection.find_one(myquery2, filter)

    if not source_user_document or not target_user_document:
        return {"message": "User Doesn't Exist"}, 404

    blockers_list = target_user_document['blockers'].copy()
    blocking_list = source_user_document['blocking'].copy()

    name = source_user_document['name']
    user_name = source_user_document['username']
    user_id_ = source_user
    prof_pic = source_user_document['prof_pic_url']
    user_bio = source_user_document['bio']
    user_followers_count = source_user_document['followers_count']
    user_following_count = source_user_document['following_count']

    source_user_to_add = {"user_id": user_id_, "name": name, "username": user_name, "prof_pic_url": prof_pic,
                          "bio": user_bio, "followers_count": user_followers_count, "following_count": user_following_count}

    #################

    name2 = target_user_document['name']
    user_name2 = target_user_document['username']
    user_id_2 = target_user
    prof_pic2 = target_user_document['prof_pic_url']
    user_bio2 = target_user_document['bio']
    user_followers_count2 = target_user_document['followers_count']
    user_following_count2 = target_user_document['following_count']

    target_user_to_add = {"user_id": user_id_2, "name": name2, "username": user_name2, "prof_pic_url": prof_pic2,
                          "bio": user_bio2, "followers_count": user_followers_count2, "following_count": user_following_count2}

    #################

    if (source_user_to_add in blockers_list) and (target_user_to_add in blocking_list):
        blockers_list.remove(source_user_to_add)
        blocking_list.remove(target_user_to_add)
        my_collection.update_one(
            myquery2, {"$set": {"blockers": blockers_list}})
        my_collection.update_one(
            myquery1, {"$set": {"blocking": blocking_list}})
        return jsonify({"Message": "Unblocked the user successfully"}), 200
    else:
        return jsonify({"Message": "User not blocked"}), 400
