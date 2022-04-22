from Tweetstruct import Tweet, retweet, collectionoftweets,wraps,encode,decode
from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from bson import ObjectId

Tweet_app = Blueprint(__name__, "Tweet_app")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
            token = None
            expiry_Date_token = encode(
                {'exp': datetime.datetime.utcnow()}, "1234")
            if 'x-access-token' in request.headers:
               token = request.headers['x-access-token']

            if not token:
               return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = decode(token, "SecretKey1911", "HS256")
                user_id = ObjectId(data['user_id'])
                current_user = Tweet_app.db.User.find_one({'_id': user_id})
            except:
               return jsonify({'message': 'Token expired!'}), 401

            return f(current_user, *args, **kwargs)

    return decorated

@Tweet_app.route("/", methods=["POST"])
@token_required
def create_tweet(current_user):
    json = request.json
    if tweet != None:
        tweet = None
    tweet = Tweet(json["username"], json["user_id"],
                  json["Text"], json["videos"], json["images"])
    tweet.set_creation_date(datetime.now().strftime("%Y-%m-%d"))
    if json == None or json == {} or str(tweet.username) is False or str(tweet.user_id) is False or str(tweet.Text) is False or tweet.username is None or (tweet.Text is None and tweet.videos_urls is [] and tweet.images_urls is []):
        return {"400", "Invalid parameters"}, 400
    if tweet.save_to_database() is False:
        return {"200": "successfull tweet creation"}, 200
    else:
        return {"404": "operation failed"}, 404


@Tweet_app.route("/tweet_id", methods=["GET"])
@token_required
def get_one_tweet(current_user):
    Id = str(request.args.get("Id", default=None, type=str))
    t1 = Tweet()
    #assert t1.get_from_database(
    #(Id)) == True, "Tweet database retieval is a failure"
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    if Id == None or str(Id) == "":
        return {"400": "Invalid Id"}, 400
    t = t1.get_from_database(Id)
    if t is None:
       # assert t1.get_from_database(
        #(Id)) == True, "Tweet database retieval needs work on the retrieved condition value"
        return {"404": "tweet is unavailable"}, 404
    #assert t1.get_from_database(
        #(Id)) == True, "Tweet database retieval is a failure function"
    return jsonify({"tweet_id": t1._id,
                    "user_id": t1.user_id,
                    "username": t1.username,
                    "prof_pic_url": t1.prof_pic_url,
                    "created_at": t1.created_at,
                    "text": t1.Text,
                    "videos": t1.videos_urls,
                    "images": t1.images_urls,
                    "like_count": t1.like_count,
                    "liked_by_ids": t1.Liked_by,
                    "retweet_count": t1.retweet_count,
                    "comment_count": t1.comment_count,
                    "comments": t1.comments}), 200


@Tweet_app.route("/all", methods=["GET"])
@token_required
def get_all_tweets(current_user):
    # number of tweets to return
    pag_token = request.args.get("page", default=1, type=int)
    tweets = collectionoftweets()
    if tweets.Tweets != []:
        tweets.Tweets = []
    t = tweets.get_from_database(int(pag_token))
    if pag_token <= 0 or int(pag_token) is False:
        return {"400": "invalid pagination token,please enter an integer number above 0"}, 400
    elif t is True:
        return {"404": "tweets are unavailable"}, 404
    elif pag_token > len(list(tweets.Tweets)):
        return {"Tweets": tweets.Tweets}, 201

    return {"Tweets": tweets.Tweets}, 200


@Tweet_app.route("/", methods=["DELETE"])
@token_required
def delete_one_tweet(current_user):
    #ID of tweet to delete
    Id = request.args.get("Id", default=None, type=str)
    try:
        ObjectId(Id)
    except:
        return {"400": "Invalid Id"}, 400
    #condtions to make sure the Id entered is in the database and atomicaly can be a valid number or string
    if Id == None:
        return {"400": "Invalid Id"}, 400
    if Tweet.get_from_database_json(ObjectId(Id)) == None:
        return {"404": "operation failed,tweet doesn't exist in database"}, 404
    Tweet.delete_from_database(ObjectId(Id))
    if Tweet.get_from_database_json(ObjectId(Id)) != None:
        return jsonify({"404": "delete operation is unavailable"}), 404
    return jsonify({"200": "successfull operation,tweet was deleted"}), 200
