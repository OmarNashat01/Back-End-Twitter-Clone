from Routes.Tweetstruct import Tweet, collectionoftweets, token_required, col_of_users, retweet, col_of_tweets, objectid_of_like_dates,col_of_stats,comment,collectionofcomments,Client,collectionofretweets,saveimages,check_block
from flask import Blueprint, request, jsonify,send_file
from flask_cors import cross_origin
from datetime import datetime, timedelta
from bson import ObjectId
import operator
import pymongo
import numpy

Tweet_app = Blueprint("Tweet_app", __name__)
path = "C:\\Users\\LEGION\\Downloads\\photos"



def findrecursive(ID, deletedids: list):
    x = comment.get_from_database_json(ObjectId(ID))
    if x is None:
       return
    for comments in list(x["comments"]):
        findrecursive(comments, deletedids)
    deletedids.append(ID)



@Tweet_app.route("", methods=["POST"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def create_tweet(current_user):
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
       urls = saveimages(images)
    else:
       videos = []
       print(json)
       urls = []
    tweet = None
    tweet = Tweet(None, current_user["_id"],
                    json["text"],videos , urls)
    print(current_user["_id"])
    tweet.set_pic(current_user["prof_pic_url"])
    tweet.set_name(current_user["username"])
    tweet.set_creation_date(datetime.now().strftime("%Y-%m-%d"))
    if json == None or json == {} or str(tweet.username) is False or str(tweet.user_id) is False or str(tweet.Text) is False or tweet.username is None or (tweet.Text == None and tweet.videos_urls == [] and tweet.images_urls == []):
        return {"400", "Invalid parameters"}, 400
    if tweet.save_to_database() is False:
        return {"200": "successfull tweet creation"}, 200
    else:
        return {"404": "operation failed"}, 404

    
@Tweet_app.route("", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
    # ID of tweet to delete
def delete_one_tweet(current_user):
    Id = request.args.get("Id", default=None, type=str)
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    # condtions to make sure the Id entered is in the database and atomicaly can be a valid number or string
    if Id == None:
        return {"400": "Invalid input,Id cannot be empty"}, 400
    x = Tweet.get_from_database_json(ObjectId(Id))
    ids = []
    if Tweet.get_from_database_json(ObjectId(Id)) == {}:
        return {"404": "operation failed,tweet doesn't exist in database"}, 404
    findrecursive(Id, ids)
    commentstobedeleted = 0
    datestobedeleted = []
    tweetid = None
    print(ids)
    for id in ids:
        x = Tweet.get_from_database_json(ObjectId(Id))
        commentstobedeleted += 1
        if x["Liker_ids"] != []:
           for dates in x["Liker_ids"]:
               datestobedeleted.append(x["date"])
        comment.delete_from_database(ObjectId(id))
    if datestobedeleted != []:
        for date in datestobedeleted:
            col_of_stats.update_one({"_id": ObjectId(objectid_of_like_dates)}, {
                                    "$pull": {"likes": date}})

    return jsonify({"200": "successfull operation,tweet was deleted and all replies to this tweet"}), 200


@Tweet_app.route("/tweet_id", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_tweet(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = Tweet()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    comments = collectionofcomments()
    comments.get_from_tweet_comments_database(1,ObjectId(Id))
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    return jsonify({"tweet":{"tweet_id": str(t1._id),
                    "user_id": str(t1.user_id),
                    "username": t1.username,
                    "name": user["name"],
                    "bio": user["bio"],
                    "followers_count": user["followers_count"],
                    "following_count": user["followers_count"],
                    "prof_pic_url": t1.prof_pic_url,
                    "created_at": t1.created_at,
                    "text": t1.Text,
                    "videos": t1.videos_urls,
                    "images": t1.images_urls,
                    "like_count": t1.like_count,
                    "liked_by_ids": t1.Liked_by,
                    "retweet_count": t1.retweet_count,
                    "comment_count": t1.comment_count,
                    "comments": comments.Tweets}}), 200


@Tweet_app.route("/random", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_tweets(current_user):
    # number of tweets to return
    pag_token = request.args.get("page", default=1, type=int)
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_random_from_database(int(pag_token),ObjectId(current_user["_id"]))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201
    return {"tweets": tweets.Tweets}, 200


@Tweet_app.route("/all/me", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_user_tweets_tweets(current_user):
    # number of tweets to return
    pag_token = 1
    _id = current_user["_id"]
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"tweets": tweets.Tweets}, 200


@Tweet_app.route("/all", methods=["GET"])
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
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"tweets": tweets.Tweets}, 200



@Tweet_app.route("/retweeting_users", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_tweet_retweeters(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    x = list(col_of_tweets.find({"refrenced_tweet_id":_id},{"user_id":1,"_id":0}))
    users = []
    if x == []:
        return {"404":"tweet has no retweets"},404
    for n in x:
        user = col_of_users.find_one({"_id":n["user_id"]})
        del user['password']
        user["_id"] = str(user["_id"])
        users.append(user)
        
    return {"retweeting_users":users},200




@Tweet_app.route("/liking_users", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_tweet_likers(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))

    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    x = col_of_tweets.find_one(
        {"_id": _id}, {"Liker_ids": 1, "_id": 1})
    users_ids = x["Liker_ids"]
    users = []
    if users_ids == []:
        return {"404": "tweet has no likers"}, 404
    for n in users_ids:
        user = col_of_users.find_one({"_id": n["liker"]})
        del user['password']
        user["_id"] = str(user["_id"])
        users.append(user)

    return {"liking_users": users}, 200


@Tweet_app.route("/all/followings", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_followings_tweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_followings_tweets_database(int(pag_token), _id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "liked tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"tweets": tweets.Tweets}, 200


@Tweet_app.route("/comments/comment_id", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_comment(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = comment()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    comments = collectionofcomments()
    comments.get_from_tweet_comments_database(1,ObjectId()) 
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    return jsonify({"tweet": {"tweet_id": str(t1._id),
                    "user_id": str(t1.user_id),
                              "username": t1.username,
                              "name": user["name"],
                              "bio": user["bio"],
                              "followers_count": user["followers_count"],
                              "following_count": user["followers_count"],
                              "prof_pic_url": t1.prof_pic_url,
                              "created_at": t1.created_at,
                              "text": t1.Text,
                              "videos": t1.videos_urls,
                              "images": t1.images_urls,
                              "like_count": t1.like_count,
                              "liked_by_ids": t1.Liked_by,
                              "retweet_count": t1.retweet_count,
                              "comment_count": t1.comment_count,
                              "comments": comments.Tweets}}), 200
    

@Tweet_app.route("/count/recent", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_tweet_count_using_a_string_query_recent(current_user):
    if current_user["admin"] == False:
        return {"501": "permission not granted"}, 501
    q = request.args.get("q",default=None,type = str)
    end_datetime = (datetime.strptime(
        (datetime.now()).strftime("%Y-%m-%d"), '%Y-%m-%d'))
    start_datetime = (datetime.strptime(
        (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), '%Y-%m-%d'))

    if start_datetime > end_datetime:
        return jsonify({"message": "Start date cannot be larger than end date"}), 400

    all_tweets = collectionoftweets()
    all_tweets.get_query_from_database(1, q)
    #####################
    list_of_days_inbetween = [(start_datetime + timedelta(days=x)).strftime("%Y-%m-%d")
                              for x in range((end_datetime-start_datetime).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = 0
        for tweets in all_tweets.Tweets:
            if tweets["created_at"] == day:
                count_for_day += 1
        list_of_counts_per_day.append({day: count_for_day})
    if list_of_counts_per_day == []:
        return {"404": "operation failed,no tweet relates to the query"}, 404
    return {"Number_of_tweets": list_of_counts_per_day}, 200


@Tweet_app.route("/count/all", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_tweet_count_using_a_string_query_ALL(current_user):
    if current_user["admin"] == False:
        return {"501": "permission not granted"}, 501
    q = request.args.get("q", default=None, type=str)
    v = list(col_of_tweets.find({}, {"created_at": 1, "_id": 0}))
    v.sort(
        key=operator.itemgetter("created_at"), reverse=True)
    v1 = list(col_of_tweets.find({}, {"created_at": 1, "_id": 0})
              )
    v1.sort(key=operator.itemgetter("created_at"))
    start_datetime = (datetime.strptime(
        (v1[0]["created_at"]), '%Y-%m-%d'))
    
    end_datetime = (datetime.strptime(
        (v[0]["created_at"]), '%Y-%m-%d'))

    if start_datetime > end_datetime:
        return jsonify({"message": "Start date cannot be larger than end date"}), 400
    all_tweets = collectionoftweets()
    all_tweets.get_query_from_database(1,q)
    #####################
    list_of_days_inbetween = [(start_datetime + timedelta(days=x)).strftime("%Y-%m-%d")
                              for x in range((end_datetime-start_datetime).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = 0
        for tweets in all_tweets.Tweets:
            if tweets["created_at"] == day:
                count_for_day +=1
        list_of_counts_per_day.append({day: count_for_day})
    if list_of_counts_per_day == []:
        return {"404":"operation failed,no tweet relates to the query"},404
    return {"Number_of_tweets": list_of_counts_per_day}, 200


@Tweet_app.route("/search/all", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_query_tweets(current_user):
    # number of tweets to return

    pag_token = 1
    try:
        string = str(request.args.get("q", default=None, type=str))
        q = string.lower()
    except:
        return {"400": "Invalid query"}, 400
    tweets = collectionoftweets()
    print(str(q))
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_query_from_database(1, q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"all_tweets": tweets.Tweets}, 200


@Tweet_app.route("/search/recent", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_query_recent_tweets(current_user):
    # number of tweets to return

    pag_token = 1
    try:
        string = str(request.args.get("q", default=None, type=str))
        q = string.lower()
    except:
        return {"400": "Invalid query"}, 400
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_query_from_database(1, q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    today = (datetime.strptime(
        (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), '%Y-%m-%d'))
    for tweet1 in list(tweets.Tweets):
        if datetime.strptime(tweet1["created_at"], '%Y-%m-%d') > today:
            print(tweet1["created_at"])
        else:
            tweets.Tweets.remove(tweet1)
    if tweets.Tweets == []:
        return {"404": "tweets are unavailable"}, 404
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"recent_tweets": tweets.Tweets}, 200


@Tweet_app.route("/retweets/random", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_retweets(current_user):
    # number of tweets to return
    pag_token = request.args.get("page", default=1, type=int)
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_random_from_database(int(pag_token), ObjectId(current_user["_id"]))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"retweets": tweets.retweets}, 201
    return {"retweets": tweets.retweets}, 200


@Tweet_app.route("/retweets/all/me", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_my_retweets(current_user):
    # number of tweets to return
    pag_token = 1
    _id = current_user["_id"]
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"retweets": tweets.retweets}, 201

    return {"retweets": tweets.retweets}, 200


@Tweet_app.route("/retweets/all", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_user_retweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"retweets": tweets.retweets}, 201

    return {"retweets": tweets.retweets}, 200


@Tweet_app.route("/retweets/retweet_id", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_retweet(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = retweet()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    comments = collectionofcomments()
    comments.get_from_tweet_comments_database(1, ObjectId(Id))
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    tweet = col_of_tweets.find_one(
        {"_id": ObjectId(t1.refrenced_tweet_id)})
    if tweet == None:
        new_tweet = {"tweet_refrenced": "None"}
    else:
        user = col_of_users.find_one({"_id": ObjectId(tweet["user_id"])})
        comments = collectionofcomments()
        comments.get_from_tweet_comments_database(1, ObjectId(tweet["_id"]))
        new_tweet = {
                    "tweet_id": str(tweet["_id"]),
                    "user_id": str(tweet["user_id"]),
                    "username": str(tweet["username"]),
                    "bio":user["bio"],
                    "prof_pic_url": str(tweet["prof_pic_url"]),
                    "text": tweet["text"],
                    "images": tweet["images"],
                    "videos": tweet["videos"],
                    "like_count": tweet["like_count"],
                    "retweet_count": tweet["retweet_count"],
                    "comment_count": tweet["comment_count"],
                    "liker_by_ids":tweet["liked_by_ids"],
                    "created_at":tweet["created_at"],
                    "comments": comments.Tweets
                    }
    return jsonify({"tweet": {"tweet_id": str(t1._id),
                              "user_id": str(t1.user_id),
                              "username": t1.username,
                              "quoted":t1.Quoted,
                              "name": user["name"],
                              "bio": user["bio"],
                              "followers_count": user["followers_count"],
                              "following_count": user["followers_count"],
                              "tweet_refrenced":new_tweet,
                              "prof_pic_url": t1.prof_pic_url,
                              "created_at": t1.created_at,
                              "text": t1.Text,
                              "videos": t1.videos_urls,
                              "images": t1.images_urls,
                              "like_count": t1.like_count,
                              "liked_by_ids": t1.Liked_by,
                              "retweet_count": t1.retweet_count,
                              "comment_count": t1.comment_count,
                              "comments": comments.Tweets}}), 200


@Tweet_app.route("/retweets/count/recent", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_retweet_count_using_a_string_query_recent(current_user):
   # if current_user["admin"] == False:
    #    return {"501": "permission not granted"}, 501
    q = request.args.get("q", default=None, type=str)
    end_datetime = (datetime.strptime(
        (datetime.now()).strftime("%Y-%m-%d"), '%Y-%m-%d'))
    start_datetime = (datetime.strptime(
        (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), '%Y-%m-%d'))

    if start_datetime > end_datetime:
        return jsonify({"message": "Start date cannot be larger than end date"}), 400

    all_tweets = collectionofretweets()
    all_tweets.get_query_from_database(1, q)
    #####################
    list_of_days_inbetween = [(start_datetime + timedelta(days=x)).strftime("%Y-%m-%d")
                              for x in range((end_datetime-start_datetime).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = 0
        for tweets in all_tweets.retweets:
            if tweets["created_at"] == day:
                count_for_day += 1
        list_of_counts_per_day.append({day: count_for_day})
    if list_of_counts_per_day == []:
        return {"404": "operation failed,no tweet relates to the query"}, 404
    return {"Number_of_tweets": list_of_counts_per_day}, 200


@Tweet_app.route("/retweets/count/all", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_retweet_count_using_a_string_query_ALL(current_user):
    #if current_user["admin"] == False:
    #   return {"501": "permission not granted"}, 501
    q = request.args.get("q", default=None, type=str)
    v = list(col_of_tweets.find({}, {"created_at": 1, "_id": 0}))
    v.sort(
        key=operator.itemgetter("created_at"), reverse=True)
    v1 = list(col_of_tweets.find({}, {"created_at": 1, "_id": 0})
              )
    v1.sort(key=operator.itemgetter("created_at"))
    start_datetime = (datetime.strptime(
        (v1[0]["created_at"]), '%Y-%m-%d'))

    end_datetime = (datetime.strptime(
        (v[0]["created_at"]), '%Y-%m-%d'))

    if start_datetime > end_datetime:
        return jsonify({"message": "Start date cannot be larger than end date"}), 400
    all_tweets = collectionofretweets()
    all_tweets.get_query_from_database(1, q)
    #####################
    list_of_days_inbetween = [(start_datetime + timedelta(days=x)).strftime("%Y-%m-%d")
                              for x in range((end_datetime-start_datetime).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = 0
        for tweets in all_tweets.retweets:
            if tweets["created_at"] == day:
                count_for_day += 1
        list_of_counts_per_day.append({day: count_for_day})
    if list_of_counts_per_day == []:
        return {"404": "operation failed,no tweet relates to the query"}, 404
    return {"Number_of_tweets": list_of_counts_per_day}, 200


@Tweet_app.route("/retweets/search/all", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_query_retweets(current_user):
    # number of tweets to return

    pag_token = 1
    try:
        string = str(request.args.get("q", default=None, type=str))
        q = string.lower()
    except:
        return {"400": "Invalid query"}, 400
    tweets = collectionofretweets()
    print(str(q))
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_query_from_database(1, q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"tweets": tweets.retweets}, 201

    return {"all_tweets": tweets.retweets}, 200


@Tweet_app.route("/retweets/search/recent", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_query_recent_retweets(current_user):
    # number of tweets to return

    pag_token = 1
    try:
        string = str(request.args.get("q", default=None, type=str))
        q = string.lower()
    except:
        return {"400": "Invalid query"}, 400
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_query_from_database(1, q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    today = (datetime.strptime(
        (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), '%Y-%m-%d'))
    for tweet1 in list(tweets.retweets):
        if datetime.strptime(tweet1["created_at"], '%Y-%m-%d') > today:
            print(tweet1["created_at"])
        else:
            tweets.retweets.remove(tweet1)
    if tweets.retweets == []:
        return {"404": "tweets are unavailable"}, 404
    if pag_token > len(list(tweets.retweets)):
        return {"tweets": tweets.retweets}, 201

    return {"recent_tweets": tweets.retweets}, 200
    

@Tweet_app.route("/media", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def retrieve_images(current_user):
    url = request.args.get("url", default=None, type = str)
    try:
       return send_file(url),200
    except:
        return {"404":"no such image in repository"},404


@Tweet_app.route("/retweets/retweeting_users", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_retweet_retweeters(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))

    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    x = list(col_of_tweets.find(
        {"refrenced_tweet_id": _id}, {"user_id": 1, "_id": 0}))
    users = []
    if x == []:
        return {"404": "tweet has no retweets"}, 404
    for n in x:
        user = col_of_users.find_one({"_id": n["user_id"]})
        del user['password']
        user["_id"] = str(user["_id"])
        users.append(user)

    return {"retweeting_users": users}, 200


@Tweet_app.route("/retweets/liking_users", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_retweet_likers(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))

    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    x = col_of_tweets.find_one(
        {"_id": _id}, {"Liker_ids": 1, "_id": 1})
    users_ids = x["Liker_ids"]
    users = []
    if users_ids == []:
        return {"404": "tweet has no likers"}, 404
    for n in users_ids:
        user = col_of_users.find_one({"_id": n["liker"]})
        del user['password']
        user["_id"] = str(user["_id"])
        users.append(user)

    return {"liking_users": users}, 200


@Tweet_app.route("/retweets/all/followings", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_followings_retweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_from_followings_tweets_database(int(pag_token),_id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "liked tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"))
    if pag_token > len(list(tweets.retweets)):
        return {"retweets": tweets.retweets}, 201

    return {"retweets": tweets.retweets}, 200


@Tweet_app.route("/tweet", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_tweet_cross(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = Tweet()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    return jsonify({"tweet": {"tweet_id": str(t1._id),
                    "user_id": str(t1.user_id),
                              "username": t1.username,
                              "name": user["name"],
                              "bio": user["bio"],
                              "followers_count": user["followers_count"],
                              "following_count": user["followers_count"],
                              "prof_pic_url": t1.prof_pic_url,
                              "created_at": t1.created_at,
                              "text": t1.Text,
                              "videos": t1.videos_urls,
                              "images": t1.images_urls,
                              "like_count": t1.like_count,
                              "liked_by_ids": t1.Liked_by,
                              "retweet_count": t1.retweet_count,
                              "comment_count": t1.comment_count,
                              "comments": t1.comments}}), 200
    

@Tweet_app.route("/retweets/retweet", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_retweet_cross(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = retweet()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    tweet = col_of_tweets.find_one(
        {"_id": ObjectId(t1.refrenced_tweet_id)})
    if tweet == None:
        new_tweet = {"tweet_refrenced": "None"}
    else:
        user = col_of_users.find_one({"_id": ObjectId(tweet["user_id"])})
        new_tweet = {
            "tweet_id": str(tweet["_id"]),
            "user_id": str(tweet["user_id"]),
            "username": str(tweet["username"]),
            "bio": user["bio"],
            "prof_pic_url": str(tweet["prof_pic_url"]),
            "text": tweet["text"],
            "images": tweet["images"],
            "videos": tweet["videos"],
            "like_count": tweet["like_count"],
            "retweet_count": tweet["retweet_count"],
            "comment_count": tweet["comment_count"],
            "liker_by_ids": tweet["liked_by_ids"],
            "created_at": tweet["created_at"],
            "comments": tweet["comments"]
        }
    return jsonify({"tweet": {"tweet_id": str(t1._id),
                              "user_id": str(t1.user_id),
                              "username": t1.username,
                              "quoted": t1.Quoted,
                              "name": user["name"],
                              "bio": user["bio"],
                              "followers_count": user["followers_count"],
                              "following_count": user["followers_count"],
                              "tweet_refrenced": new_tweet,
                              "prof_pic_url": t1.prof_pic_url,
                              "created_at": t1.created_at,
                              "text": t1.Text,
                              "videos": t1.videos_urls,
                              "images": t1.images_urls,
                              "like_count": t1.like_count,
                              "liked_by_ids": t1.Liked_by,
                              "retweet_count": t1.retweet_count,
                              "comment_count": t1.comment_count,
                              "comments": t1.comments}}), 200

@Tweet_app.route("/comments/comment", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_one_comment_cross(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = comment()
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    ID = t1.user_id
    user = col_of_users.find_one({"_id": ObjectId(ID)})
    if t is None:
        return {"404": "tweet is unavailable"}, 404
    return jsonify({"tweet": {"tweet_id": str(t1._id),
                    "user_id": str(t1.user_id),
                              "username": t1.username,
                              "name": user["name"],
                              "bio": user["bio"],
                              "followers_count": user["followers_count"],
                              "following_count": user["followers_count"],
                              "prof_pic_url": t1.prof_pic_url,
                              "created_at": t1.created_at,
                              "text": t1.Text,
                              "videos": t1.videos_urls,
                              "images": t1.images_urls,
                              "like_count": t1.like_count,
                              "liked_by_ids": t1.Liked_by,
                              "retweet_count": t1.retweet_count,
                              "comment_count": t1.comment_count,
                              "comments": t1.replies}}), 200
    

@Tweet_app.route("/all/liked", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_liked_tweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_liked_tweets_database(1,_id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "liked tweets are unavailable"}, 404
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"tweets": tweets.Tweets}, 201

    return {"tweets": tweets.Tweets}, 200


@Tweet_app.route("/retweets/all/liked", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_liked_retweets(current_user):
    # number of tweets to return
    Id = str(request.args.get("Id", default=None, type=str))
    pag_token = 1
    try:
        _id = ObjectId(Id)
    except:
        return {"400": "Invalid ID"}, 400
    tweets = collectionofretweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_from_liked_tweets_database(1, _id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "liked retweets are unavailable"}, 404
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"retweets": tweets.retweets}, 201

    return {"retweets": tweets.retweets}, 200
