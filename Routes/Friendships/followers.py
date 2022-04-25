from flask import Flask,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
from Database.Database import Database as mydb

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)

followers = Blueprint('followers', __name__)

@followers.route("/users/followers")
def get_list_of_followers():
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


