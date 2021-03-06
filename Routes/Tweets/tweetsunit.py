import unittest
from app import app
import json
from flask import jsonify
#sub class from testcase class


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTIyNzRkNTc4NmY0MzdjYmIyNWMiLCJhZG1pbiI6dHJ1ZSwiZXhwIjoxNjgyMzQzOTExfQ.b6-oq0j_Uto5NGvyobu4y2BVRjmM_6cUT9zQJ1I9FP8"
header = {"x-access-token":token}


class TestTweets(unittest.TestCase):
    #check for response 200, tweet returned successfully
    def test_get_tweet_success(self):
        print("_________________________________________________")
        tester = app.test_client(self)
        response = tester.get("/tweets/tweet_id?Id=6266b04ee31381f3ea46e4bc",headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("tweet is returned")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 400, User entered Invalid tweetID
    def test_invalid_ID_get_tweet_input(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get("/tweets/tweet_id?Id=", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        print("Invalid Id")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 404, tweet Doesnt Exist
    def test_tweet_not_found(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get(
            "/tweets/tweet_id?Id=626446fa02862871daa00931", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        print("tweet is not in the database")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 200, List of tweets returned successfully
    
    def test_get_random_tweet_success(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get("/tweets/random?page=1", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("random tweets are returned")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 400, User entered Invalid tweetID
    def test_invalid_page_number(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get("/tweets/random?page=-1", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        print("page  number invalid")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 404, tweet Doesnt Exist
    def test_tweet_page_not_found(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get("/tweets/random?page=50", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        print("page does not exist")
        print("_________________________________________________")
        print(response.status_code)
        print(response)
        
    def test_get_user_tweet_success(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get(
            "/tweets/all?Id=6265b8efc557bc4aa2f038ab", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("user tweets are returned")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 400, User entered Invalid tweetID
    def test_invalid_ID_user_get_tweets_input(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get("/tweets/all?Id=", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        print("invalid user id")
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 404, tweet Doesnt Exist
    def test_get_user_tweets_not_found(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.get(
            "/tweets/all?Id=626551f44d5226f437cbb25b", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        print("user tweets are not found")
        print("_________________________________________________")
        print(response.status_code)
        print(response)
        
        
    def test_get_user_tweet_success(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/all/me", headers=header)
        print("_________________________________________________")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("my tweets are returned")
        print("_________________________________________________")
        print(response.status_code)
        print(response)
        
    def test_post_tweet_success(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.post("/tweets", data = json.dumps({
            "text":"i am new here",
            "images":[],
            "videos":[]
            }),
            content_type='application/json', headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("_________________________________________________")
        print(response.status_code)
        print(response)
        
    def test_delete_tweet_success(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.delete(
            "/tweets?Id=6266b04ee31381f3ea46e4bc", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print("_________________________________________________")
        print(response.status_code)
        print(response)

    #check for response 400, User entered Invalid tweetId
    def test_delete_tweet_success(self):
        tester = app.test_client(self)
        print("_________________________________________________")
        response = tester.delete(
            "/tweets?Id=626446fa02862861daa00921", headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        print("_________________________________________________")
        print(response.status_code)
        print(response)

if __name__ == "__main__":
    unittest.main()
