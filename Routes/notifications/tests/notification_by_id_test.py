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

class TestNotificationsID(unittest.TestCase):
    user_id = '626551f44d5786f437cbb25b'
    notif_id= '628d51f59db90f732a5293bb'
    invalid_user_id = 'dsdsds'
    not_existing_user_id = '699899f9e99c9b99o19o9oo9'
    data = {}

    def test_sucessful_response(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications?user_id={}&notification_id={}".format(self.user_id,self.notif_id),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)
        print(response)
        print("_________________________________________________")
        print("Notification returned successfully")

    def test_user_not_found(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications?user_id={}&notification_id={}".format(self.not_existing_user_id,self.notif_id),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 404)
        print(response)
        print("_________________________________________________")
        print("User Doesnt Exist")    

    def test_invalid_input(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications?user_id={}&notification_id={}".format(self.invalid_user_id,self.notif_id),headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 400)
        print(response)
        print("_________________________________________________")
        print("Invalid user id entered")    

    def test_response_content_type(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response= tester.get("/users/notifications?user_id={}&notification_id={}".format(self.user_id,self.notif_id),headers = header)
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")
        print(response)
        print("_________________________________________________")
        print("Correct Json data returned")        