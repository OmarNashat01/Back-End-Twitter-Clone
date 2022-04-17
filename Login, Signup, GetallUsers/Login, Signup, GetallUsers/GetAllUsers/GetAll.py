from unicodedata import name
import bcrypt
from flask import Flask, request, Response, jsonify, render_template
from pymongo import MongoClient
import jwt
import datetime
from bson import ObjectId
from functools import wraps




try:
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
    app.db = client.Twitter_new
except: 
    print("can't connect")


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
            user_id = ObjectId(data['user_id'])
            current_user = app.db.User.find_one({'_id': user_id})
        except:
            return jsonify({'message': 'Token expired!'}), 401


        return f(current_user, *args, **kwargs)
       
    return decorated


        



@app.route("/users/all", methods=['GET'])
@token_required
def GET_ALL(current_user):
    if request.method == "GET":
        if current_user['admin'] == True:
            limit = int(request.args.get('limit'))
            offset = int(request.args.get('offset'))
            starting_id = app.db.User.find().sort('_id')
            last_id = starting_id[int(offset)]['_id']
            isfound = app.db.User.find({'_id': {'$gte': last_id}}).sort('_id').limit(limit)
            output = []

            for i in isfound:
                del i['_id']
                del i['password']
                output.append(i)


            #next_page = '/users/all?limit=' + str(limit) + '&offset=' + str(offset + limit)


           # if offset == 1:
                #prev_page = '/users/all?limit=' + str(limit) + '&offset=' + str(0)
            #elif offset == 0:
                #prev_page = 'No previous page'
            #else:

               # if limit > offset:
                #    prev_page = offset - 1
                #else:
                  #  prev_page = '/users/all?limit=' + str(limit) + '&offset=' + str(offset - limit)

            
            return jsonify({"users": output}), 200
            
            

        else: 
            return jsonify({"Message": "user is not admin"}), 400
