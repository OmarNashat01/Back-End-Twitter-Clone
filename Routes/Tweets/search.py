from Routes.Tweetstruct import Tweet, collectionoftweets, token_required, col_of_users, retweet, col_of_tweets, objectid_of_like_dates, col_of_stats, comment, collectionofcomments, Client, collectionofretweets, saveimages
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
from datetime import datetime, timedelta
from bson import ObjectId
import operator
import pymongo
import numpy


Home_app = Blueprint("Home_app", __name__)


@Home_app.route("/random", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_tweets(current_user):
    # number of tweets to return
    pag_token = request.args.get("page", default=1, type=int)
    tweets = collectionoftweets()
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_random_from_database(int(pag_token), ObjectId(current_user["_id"]))
    t1 = retweets.get_random_from_database(int(pag_token),ObjectId(current_user["_id"]))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    tweets.Tweets += retweets.retweets
    tweets.Tweets.sort(key=operator.itemgetter("created_at"),reverse = True)
    if pag_token > len(list(tweets.Tweets)):
        return {"all_tweets_retweets": tweets.Tweets}, 201
    return {"all_tweets_retweets": tweets.Tweets}, 200


@Home_app.route("/all/me", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_all_user_tweets_tweets(current_user):
    # number of tweets to return
    pag_token = 1
    _id = current_user["_id"]
    tweets = collectionoftweets()
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    t1 = retweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    tweets.Tweets += retweets.retweets
    tweets.Tweets.sort(key=operator.itemgetter("created_at"),reverse = True)
    if pag_token > len(list(tweets.Tweets)):
        return {"all_tweets_retweets": tweets.Tweets}, 201

    return {"all_tweets_retweets": tweets.Tweets}, 200


@Home_app.route("/all", methods=["GET"])
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
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
        retweets.retweets = [] 
    t = tweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    t1 = retweets.get_from_user_tweets_database(int(pag_token), ObjectId(_id))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    tweets.Tweets += retweets.retweets
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"all_tweets_retweets": tweets.Tweets}, 201

    return {"all_tweets_retweets": tweets.Tweets}, 200


@Home_app.route("/all/followings", methods=["GET"])
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
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_followings_tweets_database(int(pag_token), _id)
    t1 = tweets.get_from_followings_tweets_database(int(pag_token),_id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "liked tweets are unavailable"}, 404
    tweets.Tweets += retweets.retweets
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"all_tweets_retweets": tweets.Tweets}, 201

    return {"all_tweets_retweets": tweets.Tweets}, 200


@Home_app.route("/search/all", methods=["GET"])
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
    retweets = collectionoftweets()
    print(str(q))
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_query_from_database(1, q)
    t1 = retweets.get_query_from_database(1,q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    tweets.retweets += retweets.Tweets
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.retweets)):
        return {"all_tweets_retweets": tweets.retweets}, 201

    return {"all_tweets_retweets": tweets.retweets}, 200


@Home_app.route("/search/recent", methods=["GET"])
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
    retweets = collectionoftweets()
    if tweets.retweets != []:
        tweets.retweets = []
    t = tweets.get_query_from_database(1, q)
    t1 = retweets.get_query_from_database(1, q)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "tweets and retweets are unavailable"}, 404
    tweets.retweets += retweets.Tweets
    tweets.retweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    today = (datetime.strptime(
        (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), '%Y-%m-%d'))
    for tweet1 in list(tweets.retweets):
        if datetime.strptime(tweet1["created_at"], '%Y-%m-%d') > today:
            print(tweet1["created_at"])
        else:
            tweets.retweets.remove(tweet1)
    if tweets.retweets == []:
        return {"404": "tweets and retweets are unavailable"}, 404
    if pag_token > len(list(tweets.retweets)):
        return {"recent_tweets_retweets": tweets.retweets}, 201

    return {"recent_tweets_retweets": tweets.retweets}, 200


@Home_app.route("/all/liked", methods=["GET"])
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
    retweets = collectionofretweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_liked_tweets_database(1, _id)
    t1 = retweets.get_from_liked_tweets_database(1, _id)
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True and t1 is True:
        return {"404": "liked tweets and retweets are unavailable"}, 404
    tweets.Tweets += retweets.retweets
    tweets.Tweets.sort(key=operator.itemgetter("created_at"), reverse=True)
    if pag_token > len(list(tweets.Tweets)):
        return {"liked_tweets_retweets": tweets.Tweets}, 201

    return {"liked_tweets_retweets": tweets.Tweets}, 200
