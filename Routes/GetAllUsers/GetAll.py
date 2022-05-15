from urllib import response
from flask import Blueprint, request, Response, jsonify, render_template
from pymongo import MongoClient
from flask_cors import cross_origin
import jwt
from bson import ObjectId
from functools import wraps
from Database.Database import Database
import re




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
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def GET_ALL(current_user):
    if current_user['admin'] == True:
        count = Database.User.count_documents({})
        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))
        empty_array = []
        empty_document = {}
        empty_array.append(empty_document)
        if (offset > count - 1):
            return jsonify({"users": empty_array}), 204

        starting_id = Database.User.find().sort('_id')
        last_id = starting_id[int(offset)]['_id']
        isfound = Database.User.find({'_id': {'$gte': last_id}}).sort('_id').limit(limit)
        output = []

    

        for i in isfound:
            i["_id"] = str(i["_id"])
            i["creation_date"] = i["creation_date"].date()
            i["creation_date"] = i["creation_date"].strftime("%Y-%m-%d")
            if "password" in i:
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

        print(output)

        
        return jsonify({"users": output}), 200
           
    else: 
        return jsonify({"Message": "user is not admin"}), 403

   



@GetAll.route("/search", methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'x-access-token', 'Authorization'])
@token_required
def search_user(current_user):
    paginated_list = []
    empty_array = []
    users = []
    limit = int(request.args.get('limit'))
    offset = int(request.args.get('offset'))
    keyword = request.args.get('keyword')
    if current_user['admin'] == True:
        db_response = Database.User.find({
        'username': {
            '$regex': re.compile(rf"{keyword}(?i)")
        }
    })

        for i in db_response:
            i["_id"] = str(i["_id"])
            i["creation_date"] = i["creation_date"].date()
            i["creation_date"] = i["creation_date"].strftime("%Y-%m-%d")
            del i['password']
            users.append(i)

        count = len(users)

        if (offset > count - 1):
            return jsonify({"users": empty_array}), 204

        

        for i in range(len(users)):
            paginated_list.append(users[i+offset])
            if i+1== limit:
                break
 
        return jsonify({"users": paginated_list}), 200

    
    else:
        return jsonify({"message":"user is not admin"})