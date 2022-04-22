from Routes.Tweetstruct import col_of_stats,objectid_of_like_dates,col_of_tweets,wraps,encode,decode
from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

Tweet_stats = Blueprint("Tweet_stats", __name__)

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
                current_user = Tweet_stats.db.User.find_one({'_id': user_id})
            except:
               return jsonify({'message': 'Token expired!'}), 401

            return f(current_user, *args, **kwargs)

    return decorated


@Tweet_stats.route("/like_count", methods=["GET"])
@token_required
def get_like_count_using_a_query(current_user):
    start_date = request.args.get(
        "start_date", default=str(datetime.now()), type=str)
    end_date = request.args.get(
        "end_date", default=str(datetime.now()), type=str)
    if current_user["Admin"] != True:
        return {"403": "Unauthorized acccess"}, 403
    try:
       start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        return {"401": "Invalid start_date format"}, 401
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return {"402": "Invalid start_date format"}, 402
    if end_date > start_date:
        return jsonify({"400": "invalid end date"}), 400
    likes = col_of_stats.find_one({"_id": ObjectId(objectid_of_like_dates)})
    likes_n_dates = likes["likes"]
    print(likes_n_dates)
    if likes_n_dates == [] or likes_n_dates is None:
        return jsonify({"404": "likes are unavailable"}), 404
    else:
        x = 0
        for v in range(0, len(list(likes_n_dates))):
          if datetime.strptime(likes_n_dates[v], '%Y-%m-%d') >= end_date and datetime.strptime(likes_n_dates[v], '%Y-%m-%d') <= start_date:
             x += 1
          else:
              pass
        return {"count": x}, 200


@Tweet_stats.route("/tweet_count", methods=["GET"])
@token_required
def get_tweet_count_using_a_query(current_user):
    start_date = request.args.get(
        "start_date", default=str(datetime.now()), type=str)
    end_date = request.args.get(
        "end_date", default=str(datetime.now()), type=str)
    if current_user["Admin"] != True:
        return {"403": "Unauthorized acccess"}, 403
    try:
       start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        return {"401": "Invalid start_date format"}, 401
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return {"402": "Invalid start_date format"}, 402
    if end_date > start_date:
        return jsonify({"400": "invalid end date"}), 400
    if tweets != None:
        tweets = None
    tweets = col_of_tweets.find({"type": "tweet"}, {"created_at": 1, "_id": 0})
    x = 0
    for v in list(tweets):
        if datetime.strptime(v["created_at"], '%Y-%m-%d') >= end_date and datetime.strptime(v["created_at"], '%Y-%m-%d') <= start_date:
           x += 1
    if x == 0:
        return {"404": "tweet count is unavialable"}, 404
    return {"count": x}, 200
