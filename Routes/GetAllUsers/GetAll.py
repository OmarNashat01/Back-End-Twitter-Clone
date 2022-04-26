from flask import Blueprint, request, Response, jsonify, render_template
from pymongo import MongoClient
from flask_cors import cross_origin
import jwt
from bson import ObjectId
from functools import wraps
from Database.Database import Database




GetAll = Blueprint("GetAll" ,__name__)
    


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
            current_user = Database.User.find_one({'_id': user_id})

        except:
            return jsonify({'message': 'Token is invalid!'}), 401


        return f(current_user, *args, **kwargs)
       
    return decorated


        



@GetAll.route("/all", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
@token_required
def GET_ALL(current_user):
    if current_user['admin'] == True:
        if request.args.get('keyword') == None:
            limit = int(request.args.get('limit'))
            offset = int(request.args.get('offset'))
            starting_id = Database.User.find().sort('_id')
            last_id = starting_id[int(offset)]['_id']
            isfound = Database.User.find({'_id': {'$gte': last_id}}).sort('_id').limit(limit)
            output = []

            for i in isfound:
                i["_id"] = str(i["_id"])
                i["creation_date"] = i["creation_date"].date()
                i["creation_date"] = i["creation_date"].strftime("%Y-%m-%d")
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
        return jsonify({"Message": "user is not admin"}), 403

   

