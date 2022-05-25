from Routes.Tweetstruct import Tweet, collectionoftweets, token_required, col_of_users, retweet, col_of_tweets, objectid_of_like_dates, col_of_stats, comment, collectionofcomments, Client, collectionofretweets, saveimages, check_block, col_of_spaces,col_of_lists
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
from datetime import datetime, timedelta
from bson import ObjectId
import operator
import pymongo
import numpy
from Routes.notifications.Send_notifications import send_notification


Spaces_APP = Blueprint("Space_app", __name__)


@Spaces_APP.route("/creation", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def create_spaces(current_user):
    if request.form != None:
        return {"400":"Invalid empty parameters"},400
    status = " "
    if status.lower != "public" and status.lower != "private" or request.form.get("title") == None:
        return {"400":"invalid status modifier or title"},400   
    if status == "public":
        x = col_of_spaces.insert({
            "title": request.form.get("title"),
            "Admins":[str(current_user["_id"])],
            "status": request.form.get("status"),
            "users_in_space":[],
            "cover_pic_url": request.form.get("cover_pic_url"),
            "messages":[]        
        })
    else:
        try:
            password = request.form.get("password")
        except:
            return {"400":"null password"},401
        x = col_of_spaces.insert({
            "title": request.form.get("title"),
            "Admins": [str(current_user["_id"])],
            "status": request.form.get("status"),
            "password":password,
            "users_in_space": [],
            "cover_pic_url": request.form.get("cover_pic_url"),
            "messages": []
        })
    return {"200":f"space was created with space id:{x.inserted_id}"},200


@Spaces_APP.route("/register", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def add_user(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "space doesn't exist in database'"}, 403
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id')), "Admins": current_user["_id"]}) == None:
        return {"401":"user is not admin of Space"},401
    if col_of_users.find_one({"_id": ObjectId(request.form.get('user_id'))}) == None:
        return {"402":"user doesn't exist in database'"},402
    col_of_spaces.update({"_id":ObjectId(request.form.get('Id'))},{"$push":{"users_in_spaces":request.form.get('user_id')}})
    return {"200": f"user was inserted into space"}, 200


@Spaces_APP.route("/admins", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def add_admin(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "space doesn't exist in database'"}, 403
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id')), "Admins": current_user["_id"]}) == None:
        return {"401": "user is not admin of Space"}, 401
    if col_of_users.find_one({"_id": ObjectId(request.form.get('user_id'))}) == None:
        return {"402": "user doesn't exist in database'"}, 402
    col_of_spaces.update({"_id": ObjectId(request.form.get('Id'))}, {
                         "$push": {"Admins": request.form.get('user_id')}})
    return {"200": f"Admin was inserted into space"}, 200


@Spaces_APP.route("/ban", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def eject_user(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "space doesn't exist in database'"}, 403
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id')), "Admins": current_user["_id"]}) == None:
        return {"401": "user is not admin of Space"}, 401
    if col_of_users.find_one({"_id": ObjectId(request.form.get('user_id'))}) == None:
        return {"402": "user doesn't exist in database'"}, 402
    col_of_spaces.update({"_id": ObjectId(request.form.get('Id'))}, {
                         "$pull": {"users_in_spaces": request.form.get('user_id')}})
    return {"200": f"user was thrown out of space  into space"}, 200


    
@Spaces_APP.route("/deletion", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def deletespace(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "space doesn't exist in database'"}, 403
    if col_of_spaces.find_one({"_id":ObjectId(request.form.get('Id')),"Admins":request.form.get('user_id')}) == None:
        return {"401":"user is not admin of Space"},401
    col_of_spaces.delete_one({"_id":ObjectId(request.form.get('user_id'))})
    return {"200": f"space was deleted successfully"}, 200


@Spaces_APP.route("/chat", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def send_message(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "space doesn't exist in database'"}, 403
    if col_of_spaces.find_one({"_id": ObjectId(request.form.get('user_id'))}) == None:
        return {"402": "user doesn't exist in database'"}, 402
    col_of_spaces.update({"_id": request.form.get('Id')}, {
                         "$push": {"user": request.form.get('user_id'),
                                   "text": request.form.get('text'),
                                   "created_at": datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
                                   "images":[],
                                   "videos":[]
                                   }})
    return {"200": f"message was inserted into space"}, 200



@Spaces_APP.route("/list", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def create_space(current_user):
    if request.form != None:
        return {"400":"Invalid empty parameters"},400
    status = " "
    if status.lower != "public" and status.lower != "private" or request.form.get("title") == None:
        return {"400":"invalid status modifier or title"},400   
    if status == "public":
        x = col_of_lists.insert({
            "title": request.form.get("title"),
            "listowner":str(current_user["_id"]),
            "status": request.form.get("status"),
            "users_in_list":[]       
        })
    else:
        x = col_of_lists.insert({
            "title": request.form.get("title"),
            "listowner": str(current_user["_id"]),
            "status": request.form.get("status"),
            "users_in_list": [],
        })
    return {"200":f"space was created with space id:{x.inserted_id}"},200


@Spaces_APP.route("/enlist", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def add_user_to_list(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_lists.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "list doesn't exist in database'"}, 403
    if col_of_lists.find_one({"_id": ObjectId(request.form.get('Id')), "listowner": current_user["_id"]}) == None:
        return {"401":"user is not list owner"},401
    if col_of_users.find_one({"_id":ObjectId(request.form.get('user_id'))}) ==None:
        return {"402":"user doesn't exist in database"},402
    col_of_lists.update({"_id":ObjectId(request.form.get('Id'))},{"$push":{"users_in_list":request.form.get('user_id')}})
    return {"200": f"user was inserted into list"}, 200


@Spaces_APP.route("/delist", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def eject_user_from_list(current_user):
    if request.form != None:
        return {"400": "Invalid empty parameters"}, 400
    if col_of_lists.find_one({"_id": ObjectId(request.form.get('Id'))}) == None:
        return {"403": "list doesn't exist in database'"}, 403
    if col_of_lists.find_one({"_id": ObjectId(request.form.get('Id')), "listowner": current_user["_id"]}) == None:
        return {"401": "user is not list owner"}, 401
    if col_of_users.find_one({"_id": ObjectId(request.form.get('user_id'))}) == None:
        return {"402": "user doesn't exist in database'"}, 402
    col_of_lists.update({"_id": ObjectId(request.form.get('Id'))}, {
                         "$pull": {"users_in_list": request.form.get('user_id')}})
    return {"200": f"user was thrown out of  list into space"}, 200


@Spaces_APP.route("/mylists", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_user_lists(current_user):
    # number of tweets to return
    Id = str(current_user["_id"])
    if col_of_lists.find_one({"listowner": Id}) == None:
        return {"404": "user ahs no lists"},404
    lists =list(col_of_lists.find({"listowner":Id}))
    for l in lists:
        l["_id"] = str(l["_id"])
    if lists == []:
       return {"404":"user ahs no lists"},404
    return {"lists": lists}, 200

@Spaces_APP.route("/mylist", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_user_tweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    all_lists = []
    users = col_of_lists.find_one({"_id": ObjectId(Id)})
    tweets = collectionoftweets()
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
        retweets.retweets = []
    for user in users["users_in_lists"]:
        t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(user))
        t1 = retweets.get_from_user_tweets_database(int(pag_token), ObjectId(user))
        all_lists += tweets.Tweets
        all_lists += retweets.retweets 
        tweets.Tweets = []
        retweets.retweets = []
    if t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    all_lists.sort(key=operator.itemgetter("created_at"), reverse=True)
    return {"all_list_tweets_retweets": all_lists}, 200
