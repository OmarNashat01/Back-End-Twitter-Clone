from flask import Flask,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
from Database.Database import Database as mydb

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)

following = Blueprint('following', __name__)

@following.route("/users/following",methods=['GET','POST','DELETE'])
def follow_user():
    if request.method == 'POST':
        data = request.get_json()
        source_user = data['source_user_id']
        target_user = data['target_user_id']
        try:
            objInstance_source = ObjectId(source_user)
            objInstance_target= ObjectId(target_user)
        except:
            return jsonify({"message": "Please, Eneter a valid object User ID"}) , 400
        my_collection = mydb["User"]
        myquery1 = {"_id": objInstance_source}
        myquery2 = {"_id": objInstance_target}
        filter = {"_id": 0,'password':0}

        source_user_document = my_collection.find_one(myquery1,filter)## Source User to add to the followers list
        target_user_document = my_collection.find_one(myquery2,filter) 
       
        if not source_user_document or not target_user_document:
            return  {"message": "User Doesn't Exist"} , 404
#$push

        followers_list = target_user_document['followers'].copy()
        following_list = source_user_document['following'].copy()

        name = source_user_document['name']
        user_name =source_user_document['username']
        email = source_user_document['email']
        source_user_to_add = {"name":name,"user_name":user_name,"email":email}
        #################
        name2 = target_user_document['name']
        user_name2 =target_user_document['username']
        email2 = target_user_document['email']
        target_user_to_add = {"name":name2,"user_name":user_name2,"email":email2}
###############################

        if (source_user_to_add in followers_list) and (target_user_to_add in following_list) :
            return jsonify({"message": "User already followed"}),400
            
        else:
            followers_list.append(source_user_to_add)
            following_list.append(target_user_to_add)
           
         

        my_collection.update_one(myquery2,{"$set": {"followers": followers_list}})
        my_collection.update_one(myquery1,{"$set": {"following": following_list}})

        return {"Message": "Sucessfully followed the user"} , 200

    if request.method == 'GET':

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
        following_list = user_document['following']
        if len(following_list) < 1:
            return {"message": "User Doesn't Follow anyone"},204

    
        return  {"following": following_list}  

    if request.method == 'DELETE':
        my_collection = mydb["User"]

        source_user = request.args.get('source_user_id')
        target_user = request.args.get('target_user_id')
        try:
            objInstance_source = ObjectId(source_user)
            objInstance_target= ObjectId(target_user)
        except:
            return jsonify({"message": "Please, Eneter a valid object User ID"}) , 400

        myquery1 = {"_id": objInstance_source}
        myquery2 = {"_id": objInstance_target}

        filter = {"_id": 0,'password':0}
        source_user_document = my_collection.find_one(myquery1,filter) ## Source User to add to the followers list
        target_user_document = my_collection.find_one(myquery2,filter) 
        
        if not source_user_document or not target_user_document:
            return  {"message": "User Doesn't Exist"} , 404
       
        followers_list = target_user_document['followers'].copy()
        following_list = source_user_document['following'].copy()

        name = source_user_document['name']
        user_name =source_user_document['username']
        email = source_user_document['email']
        source_user_to_add = {"name":name,"user_name":user_name,"email":email}
        #################
        name2 = target_user_document['name']
        user_name2 =target_user_document['username']
        email2 = target_user_document['email']
        target_user_to_add = {"name":name2,"user_name":user_name2,"email":email2}

        if (source_user_to_add in followers_list) and (target_user_to_add in following_list):
            followers_list.remove(source_user_to_add)
            following_list.remove(target_user_to_add)
        else:
            return jsonify({"message": " User already Unfollowed"}),400

        my_collection.update_one(myquery2,{"$set": {"followers": followers_list}})
        my_collection.update_one(myquery1,{"$set": {"following": following_list}})

        return jsonify(target_user_document)
    else:
        return jsonify({"Message":"Access Not allowed"}),400

