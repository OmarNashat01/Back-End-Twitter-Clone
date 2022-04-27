from posixpath import split
from tracemalloc import start
from flask import Flask,request,Response,jsonify,Blueprint
from flask_cors import cross_origin
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
import datetime
from Database.Database import Database as mydb
from datetime import date, timedelta
import jwt
from functools import wraps

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)
retweets_count = Blueprint('retweets_count', __name__)
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
@retweets_count.route("/retweet_count")
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def number_of_retweets(current_user):
    start_datetime = request.args.get('start_date')
    end_datetime = request.args.get('end_date') 
    try:
        start_date = datetime.datetime.strptime(start_datetime,'%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_datetime,'%Y-%m-%d').date()
    except:
        return jsonify({"message": "Enter valid date like this: 2022-4-11"}),400
        
    if start_date > end_date:
        return jsonify({"message": "Start date cannot be larger than end date"}),400

    counter = 0
    my_collection = mydb["tweets"]
    query = {"type": {"$eq":'retweet'} }
    all_retweets = list(my_collection.find(query,{"_id":0,"created_at":1}))
#####################    
    list_of_days_inbetween = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((end_date-start_date).days + 1)]
    number_of_days = len(list_of_days_inbetween)
    counts_for_each_day = [0]*number_of_days
    list_of_counts_per_day = []
    for day in list_of_days_inbetween:
        count_for_day = all_retweets.count({'created_at':day})
        list_of_counts_per_day.append({day: count_for_day})    
    # for tweet in all_retweets:
    #     created_date = datetime.datetime.strptime(tweet['created_at'],'%Y-%m-%d').date()
    #     if created_date >= start_date and created_date <= end_date:
    #         counter = counter+1

    return jsonify({"Number of retweets":list_of_counts_per_day})
