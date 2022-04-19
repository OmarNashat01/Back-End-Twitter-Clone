from posixpath import split
from tracemalloc import start
from flask import Flask,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
import datetime
from Database.Database import Database as mydb


# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)
retweets_count = Blueprint('retweets_count', __name__)

@retweets_count.route("/admin/statistics/retweet_count")
def number_of_retweets():
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
    
    for tweet in all_retweets:
        created_date = datetime.datetime.strptime(tweet['created_at'],'%Y-%m-%d').date()
        if created_date >= start_date and created_date <= end_date:
            counter = counter+1

    return jsonify({"Number of retweets":counter})
