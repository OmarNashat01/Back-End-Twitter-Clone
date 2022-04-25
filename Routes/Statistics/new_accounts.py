from posixpath import split
from tracemalloc import start
from flask import Flask,request,Response,jsonify,Blueprint
import pymongo
from bson.objectid import ObjectId
import bson.json_util as json_util
import datetime
from Database.Database import Database as mydb
from datetime import date, timedelta

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)
new_accounts_count = Blueprint('new_accounts_count', __name__)

@new_accounts_count.route("/admin/statistics/new_account_count")
def number_of_newaccounts():
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
    my_collection = mydb["User"]
    all_users = list(my_collection.find({},{"_id":0,"creation_date": 1}))
    ##########################################################
    list_of_users_string_date =[]
    for user in all_users:
        date_per_user_as_string = user['creation_date'].strftime("%Y-%m-%d")
        list_of_users_string_date.append({'creation_date': date_per_user_as_string})
        
    list_of_days_inbetween = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((end_date-start_date).days + 1)]
    count_of_users_per_day = []

    for day in list_of_days_inbetween:
        count_for_day = list_of_users_string_date.count({'creation_date':day})
        count_of_users_per_day.append({day: count_for_day})

    # for date in all_users:
    #     create_date=date['creation_date'].date()
    #     if create_date >= start_date and create_date <= end_date:
    #         counter = counter+1

    return jsonify({"Number of created Users":count_of_users_per_day})

