from flask import Flask, jsonify,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
from datetime import date, datetime, timedelta
### integration
from Database.Database import Database as mydb
from flask_cors import cross_origin
from functools import wraps
import jwt

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
#app = Flask(__name__)

all_notifications = Blueprint('all_notifications', __name__)

#################
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
########################################

@all_notifications.route('/all')
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required

def get_all_notifications():
    user_id = request.args.get('user_id')
    try:
        user_id_object = ObjectId(user_id)
    except:
        return jsonify({"message": "Please, Eneter a valid object User ID"}) , 400

    if user_id == None:
        return jsonify({"message": "Please, Eneter a User ID"}) , 400

    user_collection = mydb['User']
    myquery = {"_id": user_id_object}
    user_document = user_collection.find_one(myquery)

    if not user_document:
        return jsonify({"message": "User Doesn't Exist"}), 404

    notifications_list = user_document['notifications']
    for notification in notifications_list:
        notification['_id'] = str(notification['_id'])

    return jsonify({"notifications": notifications_list}),200


