from flask import Flask,request,Response,jsonify,Blueprint
from flask_cors import cross_origin
from bson.objectid import ObjectId
from Database.Database import Database as mydb
import jwt
from functools import wraps
# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)

followers = Blueprint('followers', __name__)
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

@followers.route("/followers")
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_list_of_followers(current_user):
    user_id = request.args.get('user_id')
    try:
        objInstance_user = ObjectId(user_id)
    except:
        return jsonify({"message": "Please, Eneter a valid object User ID"}) , 400

    if user_id == None:
        return jsonify({"message": "Please, Eneter a User ID"}) , 400
    my_collection = mydb["User"]
    myquery = {"_id": objInstance_user}
    user_document = my_collection.find_one(myquery)
    if not user_document:
        return {"message": "User Doesn't Exist"} , 404

    creation_date_objec = user_document['creation_date']
    followers_list = user_document['followers']

    if len(followers_list) < 1:
        return {"message": "User Doesn't have followers"},204

 
    return  {"followers": followers_list}  


