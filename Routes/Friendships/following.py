from flask import Flask,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
from Database.Database import Database as mydb
import jwt
from functools import wraps

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)

following = Blueprint('following', __name__)
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


@following.route("/users/following",methods=['GET','POST','DELETE'])
@token_required
def follow_user(current_user):
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
        #email = source_user_document['email']
        user_id_ = source_user
        prof_pic = source_user_document['prof_pic_url']
        user_bio = source_user_document['bio']
        user_followers_count = source_user_document['followers_count']
        user_following_count=source_user_document['following_count']

        source_user_to_add = {"user_id":user_id_,"name":name,"username":user_name,"prof_pic_url":prof_pic,"bio":user_bio,"followers_count":user_followers_count,"following_count":user_following_count}
        #source_user_to_add = {"name":name,"user_name":user_name,"email":email}
        #################
        name2 = target_user_document['name']
        user_name2 =target_user_document['username']
        #email2 = target_user_document['email']
        user_id_2 = target_user
        prof_pic2 = target_user_document['prof_pic_url']
        user_bio2 = target_user_document['bio']
        user_followers_count2 = target_user_document['followers_count']
        user_following_count2 = target_user_document['following_count']

        target_user_to_add = {"user_id":user_id_2,"name":name2,"username":user_name2,"prof_pic_url":prof_pic2,"bio":user_bio2,"followers_count":user_followers_count2,"following_count":user_following_count2}

        #target_user_to_add = {"name":name2,"username":user_name2,"email":email2}
###############################

        if (source_user_to_add in followers_list) and (target_user_to_add in following_list) :
            return jsonify({"message": "User already followed"}),400
            
        else:
            my_collection.update_one(myquery2,{"$set": {"followers_count": user_followers_count2+1}})
            my_collection.update_one(myquery1,{"$set": {"following_count": user_following_count+1}})

            user_following_count = user_following_count +1
            source_user_to_add = {"user_id":user_id_,"name":name,"username":user_name,"prof_pic_url":prof_pic,"bio":user_bio,"followers_count":user_followers_count,"following_count":user_following_count}
            
            user_followers_count2 = user_followers_count2 +1
            target_user_to_add = {"user_id":user_id_2,"name":name2,"username":user_name2,"prof_pic_url":prof_pic2,"bio":user_bio2,"followers_count":user_followers_count2,"following_count":user_following_count2}

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
        
        # if len(following_list) < 1:
        #     return {"message": "User Doesn't Follow anyone"},204

    
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
        #email = source_user_document['email']
        user_id_ = source_user
        prof_pic = source_user_document['prof_pic_url']
        user_bio = source_user_document['bio']
        user_followers_count = source_user_document['followers_count']
        user_following_count=source_user_document['following_count']

        source_user_to_add = {"user_id":user_id_,"name":name,"username":user_name,"prof_pic_url":prof_pic,"bio":user_bio,"followers_count":user_followers_count,"following_count":user_following_count}
        # name = source_user_document['name']
        # user_name =source_user_document['username']
        # email = source_user_document['email']
        # source_user_to_add = {"name":name,"user_name":user_name,"email":email}
        #################
        name2 = target_user_document['name']
        user_name2 =target_user_document['username']
        #email2 = target_user_document['email']
        user_id_2 = target_user
        prof_pic2 = target_user_document['prof_pic_url']
        user_bio2 = target_user_document['bio']
        user_followers_count2 = target_user_document['followers_count']
        user_following_count2 = target_user_document['following_count']

        target_user_to_add = {"user_id":user_id_2,"name":name2,"username":user_name2,"prof_pic_url":prof_pic2,"bio":user_bio2,"followers_count":user_followers_count2,"following_count":user_following_count2}        
        # name2 = target_user_document['name']
        # user_name2 =target_user_document['username']
        # email2 = target_user_document['email']
        # target_user_to_add = {"name":name2,"user_name":user_name2,"email":email2}

        if (source_user_to_add in followers_list) and (target_user_to_add in following_list):
            my_collection.update_one(myquery2,{"$set": {"followers_count": user_followers_count2-1}})
            my_collection.update_one(myquery1,{"$set": {"following_count": user_following_count-1}})

            followers_list.remove(source_user_to_add)
            following_list.remove(target_user_to_add)
        else:
            return jsonify({"message": " User already Unfollowed"}),400

        my_collection.update_one(myquery2,{"$set": {"followers": followers_list}})
        my_collection.update_one(myquery1,{"$set": {"following": following_list}})

        return jsonify({"Message":"Unfollowed the user successfully"}),200
    else:
        return jsonify({"Message":"Access Not allowed"}),400

