from Routes.Tweetstruct import col_of_stats,Client,objectid_of_like_dates,col_of_tweets,token_required,Date,getDifference
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime,timedelta
from bson import ObjectId

Tweet_stats = Blueprint("Tweet_stats", __name__)


@Tweet_stats.route("/like_count", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_like_count_using_a_query(current_user):
    if current_user["admin"] == False:
        return {"501": "permission not granted"}, 501
    start_date = request.args.get(
        "start_date", default=str(datetime.now()), type=str)
    end_date = request.args.get(
        "end_date", default=str(datetime.now()), type=str)
    try:
       start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except:
        return {"401": "Invalid start_date format"}, 401
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return {"402": "Invalid start_date format"}, 402
    if end_date < start_date:
        return jsonify({"400": "start date cannot be larger than end date"}), 400
    likes = col_of_stats.find_one({"_id": ObjectId(objectid_of_like_dates)})
    likes_n_dates = likes["likes"]
    print(likes_n_dates)
    if likes_n_dates == [] or likes_n_dates is None:
        return jsonify({"404": "likes are unavailable"}), 404
    else:
        d1 = start_date.day
        d2 = end_date.day
        m1 = start_date.month
        m2 = end_date.month
        y1 = start_date.year
        y2 = end_date.year
        std = Date(d1, m1, y1)
        etd = Date(d2, m2, y2)

        countsarray = []
        for z in range(0, getDifference(std, etd)):
            x = 0
            start_date += timedelta(days=1)
            for v in range(0, len(list(likes_n_dates))):
                if datetime.strptime(likes_n_dates[v], '%Y-%m-%d') == start_date:
                    x += 1
                else:
                    pass
            countsarray.append({f"{start_date.strftime('%Y-%m-%d')}": x})
        return {"Number_of_likes": countsarray}, 200


@Tweet_stats.route("/tweet_count", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def get_tweet_count_using_a_query(current_user):
    if current_user["admin"] == False:
        return {"501": "permission not granted"}, 501
    start_datetime = request.args.get('start_date')
    end_datetime = request.args.get('end_date')
    try:
         start_date = datetime.strptime(start_datetime, '%Y-%m-%d').date()
         end_date = datetime.strptime(end_datetime, '%Y-%m-%d').date()
    except:
        return jsonify({"message": "Enter valid date like this: 2022-4-11"}), 400

    if start_date > end_date:
        return jsonify({"message": "Start date cannot be larger than end date"}), 400

    counter = 0
    my_collection = Client["tweets"]
    query = {"type": {"$eq": 'tweet'} }
    all_retweets = list(col_of_tweets.find(query, {"_id":0,"created_at":1}))
    #####################
    list_of_days_inbetween = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d")
                                for x in range((end_date-start_date).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = all_retweets.count({'created_at': day})
        list_of_counts_per_day.append({day: count_for_day})
    return {"Number_of_tweets": list_of_counts_per_day},200
