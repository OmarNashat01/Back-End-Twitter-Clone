from Routes.Tweetstruct import Tweet, collectionoftweets, token_required, col_of_users, retweet, col_of_tweets, objectid_of_like_dates, col_of_stats, comment, collectionofcomments,saveimages,check_block
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime, timedelta
from bson import ObjectId
import operator
import pymongo
import numpy

Tweet_app1 = Blueprint("Tweet_app1",__name__)


@Tweet_app1.route("/retweets", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def create_retweet(current_user):
    check = check_block(current_user)
    if check == 'banned':
        return jsonify({"message": 'user is banned'}), 403
    json1 = request.files
    json = request.form
    if request.files == None and request.form == None:
        return {"400":"Invalid empty parameteres"},400
    text = None
    videos = []
    images = []
    urls = []
    if json1 != None and bool(json["quoted"]) is True:
       images = json1.getlist('img')
       videos = json1.getlist('vid')
       print(json)
       urls = saveimages(images)
       text = json["text"]
    elif bool(json["quoted"]) is False:
       videos = []
       print(json)
       urls = []
       text = None
    try:
        ObjectId(json["tweet_id"])
    except:
        return {"400":"invalid tweet id"},400
    if Tweet.get_from_database_json(ObjectId(json["tweet_id"])) is None:
        return {"405": "refrenced tweet does not exist in the database"}, 405
    tweet = retweet(None, current_user["_id"],
                    text, videos, urls, ObjectId(json["tweet_id"]))
    tweet.set_pic(current_user["prof_pic_url"])
    tweet.set_name(current_user["username"])
    tweet.set_creation_date(datetime.now().strftime("%Y-%m-%d"))
    tweet.setbool(bool(json["quoted"]))
    col_of_tweets.update_one({"_id": ObjectId(json["tweet_id"])}, {
                             "$inc": {"retweet_count": 1}})
    if json["tweet_id"] is None or json == None or json == {} or str(tweet.username) is False or str(tweet.user_id) is False or str(tweet.Text) is False or tweet.username is None or (tweet.Text is "" and tweet.videos_urls is [] and tweet.images_urls is []):
        return {"400":"Invalid parameters"}, 400
    if tweet.save_to_database() is False:
        return {"200": "successfull retweet creation"}, 200
    else:
        return {"404": "operation failed"}, 404


@Tweet_app1.route("/retweets", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
# ID of tweet to delete
def delete_one_retweet(current_user):
    Id = request.args.get("Id", default=None, type=str)
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    # condtions to make sure the Id entered is in the database and atomicaly can be a valid number or string
    if Id == None:
        return {"400": "Invalid Id"}, 400
    if retweet.get_from_database_json(ObjectId(Id)) == None:
        return {"404": "operation failed,tweet doesn't exist in database"}, 404
    retweeter = retweet.get_from_database_json(ObjectId(Id))
    tweetid = retweeter["refrenced_tweet_id"]
    col_of_tweets.update_one({"_id": ObjectId(tweetid)}, {
                             "$inc": {"retweet_count": -1}})
    retweet.delete_from_database(ObjectId(Id))
    if retweet.get_from_database_json(ObjectId(Id)) != None:
        return jsonify({"404": "delete operation is unavailable"}), 404
    return jsonify({"200": "successfull operation,tweet was deleted"}), 200


@Tweet_app1.route("/likes", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def like_an_object(current_user):
    check = check_block(current_user)
    if check == 'banned':
        return jsonify({"message": 'user is banned'}), 403
    json = request.json
    tweet = None
    try:
        ObjectId(json["tweet_id"])
        ObjectId(current_user["_id"])
    except:
        {"405": "invalid tweet id or invalid user id does not exist in the database"}, 405
    if list(col_of_tweets.find({"_id": ObjectId(json["tweet_id"])})) == []:
        return {"404": "liked tweet  does not exist in the database"}, 404
    if list(col_of_users.find({"_id": ObjectId(current_user["_id"])})) == []:
        return {"404": "user  does not exist in the database"}, 404
    if list(col_of_tweets.find({"_id": ObjectId(json["tweet_id"]), "Liker_ids.liker": {
            "$nin": [str(current_user["_id"])]}})) == []:
        return {"406": "operation failed as user has already liked the tweet"}, 406
    col_of_tweets.update_one({"_id": ObjectId(json["tweet_id"])}, {"$push": {"Liker_ids": {"liker":
                                                                                           str(current_user["_id"]), "date": datetime.now().strftime("%Y-%m-%d")}}, "$inc": {"like_count": 1}})
    col_of_stats.update_one({"_id": ObjectId(objectid_of_like_dates)}, {"$push": {
                            "likes": datetime.now().strftime("%Y-%m-%d")}})
    return {"200": "tweet successfully liked"}, 200


@Tweet_app1.route("/likes", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def unlike_an_object(current_user):
    Id = request.args.get("Id", default=None, type=str)
    try:
        ObjectId(Id)
        ObjectId(current_user["_id"])
    except:
        {"405": "invalid tweet id or invalid user id does not exist in the database"}, 405
    if list(col_of_tweets.find({"_id": ObjectId(Id)})) == []:
        return {"404": "liked tweet  does not exist in the database"}, 404
    if list(col_of_users.find({"_id": ObjectId(current_user["_id"])})) == []:
        return {"404": "user  does not exist in the database"}, 404
    if list(col_of_tweets.find({"_id": ObjectId(Id), "Liker_ids.liker": {
            "$in": [str(current_user["_id"])]}})) == []:
        return {"406": "operation failed as user does not like the tweet"}, 406
    dateoflike = col_of_tweets.find_one(
        {"_id": ObjectId(Id), "Liker_ids.Liker": Id}, {"Liker_ids.date": 1})
    col_of_tweets.update_one({"_id": ObjectId(Id)}, {"$pull": {"Liker_ids": {"liker":
                                                                             str(current_user["_id"]), "date": datetime.now().strftime("%Y-%m-%d")}}, "$inc": {"like_count": -1}})
    col_of_stats.update_one({"_id": ObjectId(objectid_of_like_dates)}, {"$pull": {
                            "likes": dateoflike}})
    return {"200": "tweet successfully unliked"}, 200


@Tweet_app1.route("/comments", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def create_comment(current_user):
    check = check_block(current_user)
    if check == 'banned':
        return jsonify({"message": 'user is banned'}), 403
    json1 = request.files
    json = request.form
    images = []
    videos = []
    urls = []
    if json1 != None:
       images = json1.getlist('img')
       videos = json1.getlist('vid')
       print(json)
       #urls = saveimages(images)
    else:
       videos = []
       print(json)
       urls = []
    comments = None
    print("yes-------------------")
    comments = comment(None, current_user["_id"],
                       json["text"],videos , urls)
    comments.set_pic(current_user["prof_pic_url"])
    comments.set_name(current_user["username"])
    comments.set_creation_date(datetime.now().strftime("%Y-%m-%d"))
    print("yes-------------------")
    try:
        ObjectId(json["tweet_id"])
        ObjectId(current_user["_id"])
    except:
        {"405": "invalid tweet id or invalid user id does not exist in the database"}, 405
    print("yes-------------------")
    if json == None or json == {} or str(comments.username) is False or str(comments.user_id) is False or str(comments.Text) is False or comments.username is None or (comments.Text is "" and comments.videos_urls is [] and comments.images_urls is []):
        return {"400", "Invalid parameters"}, 400
    print("yes-------------------")
    x = comments.save_to_database()
    print("yes-------------------")
    col_of_tweets.update_one({"_id": ObjectId(json["tweet_id"])}, {
                             "$push": {"comments": str(x.inserted_id)}, "$inc": {"comment_count": 1}})
    
    if col_of_tweets.find({"_id": ObjectId(str(x.inserted_id))}) != []:
        return {"200": "successfull comment creation"}, 200
    else:
        return {"404": "operation failed"}, 404


def findrecursive(ID, deletedids: list):
    x = comment.get_from_database_json(ObjectId(ID))
    if x is None:
       return
    for comments in list(x["comments"]):
        findrecursive(comments, deletedids)
    deletedids.append(ID)


@Tweet_app1.route("/comments", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
# ID of tweet to delete
def delete_one_comment(current_user):
    Id = request.args.get("Id", default=None, type=str)
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    # condtions to make sure the Id entered is in the database and atomicaly can be a valid number or string
    if Id == None:
        return {"400": "Invalid input,Id cannot be empty"}, 400
    x = comment.get_from_database_json(ObjectId(Id))
    ids = []
    if comment.get_from_database_json(ObjectId(Id)) == {}:
        return {"404": "operation failed,reply doesn't exist in database"}, 404
    findrecursive(Id, ids)
    commentstobedeleted = 0
    datestobedeleted = []
    tweetid = col_of_tweets.find_one({"comments":Id})
    print(ids)
    for id in ids:
        x = comment.get_from_database_json(ObjectId(Id))
        commentstobedeleted += 1
        if x["Liker_ids"] != []:
           for dates in x["Liker_ids"]:
               datestobedeleted.append(x["date"])
        comment.delete_from_database(ObjectId(id))
    print(tweetid["_id"])
    if datestobedeleted != []:
        for dates in datestobedeleted:
            col_of_stats.update_one({"_id": ObjectId(objectid_of_like_dates)}, {
                                    "$pull": {"likes": dates}})
    for id in ids:    
        col_of_tweets.update_one({"_id": ObjectId(tweetid["_id"])}, {
                                "$pull": {"comments": str(ids)}})
    col_of_tweets.update_one({"_id": ObjectId(tweetid["_id"])}, {
                             "$inc": {"comment_count": -commentstobedeleted}})

    return jsonify({"200": "successfull operation,comment was deleted and all replies to this reply"}), 200
