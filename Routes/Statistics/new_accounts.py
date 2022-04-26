from flask import request, jsonify,Blueprint
from flask_cors import cross_origin
from bson.objectid import ObjectId
import datetime
from Database.Database import Database as mydb
from datetime import timedelta
import jwt
from functools import wraps

# myclient = pymongo.MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority", connect=True)
# mydb = myclient["Twitter_new"]
# app = Flask(__name__)
new_accounts_count = Blueprint('new_accounts_count', __name__)
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
    
@new_accounts_count.route("/admin/statistics/new_account_count")
@cross_origin(allow_headers=['Content-Type'])
@token_required
def number_of_newaccounts(current_user):
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

