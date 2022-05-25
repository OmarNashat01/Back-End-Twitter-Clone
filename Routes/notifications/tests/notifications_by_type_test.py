import unittest
from wsgiref import headers
from app import app
import json
from Routes.Tweetstruct import col_of_tweets,col_of_users
import pymongo 
from bson import ObjectId
from Database.Database import Database

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTFmNDRkNTc4NmY0MzdjYmIyNWIiLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTY4MjM0MzQ5MX0.8xbJXtfITqlxM1YwdaRV1kr1qXRtvQJ3glhjxNdOPD4"
header = {"x-access-token":token}
data =  {"source_user_id": "626551f44d5786f437cbb25b","target_user_id":"626552274d5786f437cbb25c"}

class TestNotificationsType(unittest.TestCase):
    user_id = '6278fe20281eab1464e4cf2a'
    notif_type = 'tweet_liked_event'
    invalid_user_id = 'dsdsds'
    not_existing_user_id = '699899f9e99c9b99o19o9oo9'
    data = {}

    def test_sucessful_response(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications/type?user_id={}&notification_type={}".format(self.user_id,self.notif_type),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)
        print(response)
        print("_________________________________________________")
        print("Notifications of the user returned successfully")

    def test_user_not_found(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications/type?user_id={}&notification_type={}".format(self.not_existing_user_id,self.notif_type),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 404)
        print(response)
        print("_________________________________________________")
        print("User Doesnt Exist")    

    def test_invalid_input(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications/type?user_id={}&notification_type={}".format(self.invalid_user_id,self.notif_type),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 400)
        print(response)
        print("_________________________________________________")
        print("Invalid user id entered")    

    def test_response_content_type(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications/type?user_id={}&notification_type={}".format(self.user_id,self.notif_type),headers = header)
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")
        print(response)
        print("_________________________________________________")
        print("Correct Json data returned")        