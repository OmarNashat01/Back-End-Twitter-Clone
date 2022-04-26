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

get_user = Blueprint('get_user', __name__)

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

@get_user.route("/user_id", methods=["GET"])
@token_required
def singleuser(current_user):
    # print(request.args["_id"])
    try:
        query = {"_id": ObjectId(request.args["_id"])}
        user = mydb.User.find_one(query)
        if(not user):
            return Response(
                response=json.dumps(
                    {"message": "User ID not found"
                     }),
                status=404,
                mimetype="application/json"
            )
        user_to_get = {"_id": request.args["_id"]}
        user_id = request.args["_id"]
        db_response = mydb.User.find_one(user_to_get)
        del user['password']
        user["creation_date"] = user["creation_date"].date()
        user["creation_date"] = user["creation_date"].strftime("%Y-%m-%d")
        user["_id"] = str(user["_id"])
        # print(db_response)
        return Response(
            response=json.dumps(
                {"message": "The request was succesful",
                 "user": f"{user}"
                 }),
            status=200,
            mimetype="application/json")
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")
        return Response(
            response=json.dumps(
                {"message": "User ID not found"
                 }),
            status=404,
            mimetype="application/json")


#############################################
# if __name__ == "__main__":
#     app.run(port=8081, debug=True)