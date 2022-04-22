import unittest
from app import app


#sub class from testcase class


class TestTweets(unittest.TestCase):

    #check for response 200, tweet returned successfully
    def test_success(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/tweet_id?Id=625c1825871ec7725260372c")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid tweetID
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/tweet_id?Id=")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, tweet Doesnt Exist
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/tweet_id?Id=1012001")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        
    #check for response 200, List of tweets returned successfully

    def test_success(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/all?page=1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid page number
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/all?page=-1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, page number doesnt hold anything
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.get("/tweets/all?page=50")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        
    #check for response 200, tweet deleted successfully
    def test_success(self):
        tester = app.test_client(self)
        response = tester.delete("/tweets?Id=625c1825871ec7725260372c")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid tweet id
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.delete("/tweets?Id=")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, tweet Doesnt Exist
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.delete("/tweets?Id=1012001")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        
    #check for response 200, tweet posted succefully

    def test_success(self):
        tester = app.test_client(self)
        response = tester.post("/tweets",{
            "user_id": "625560c0e10c0b48c19d2cb5",
            "username":"mohamed99883",
            "Text":"why are you running",
            "videos":[],
            "images":[]
        })
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid tweet structure
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.post("/tweets",{})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, User Doesnt Exist
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.post("/tweets",{"user_id":"sgsgrrsgr",
                                         "username":"",
                                         "Text":""})
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        
    #check for response 200, List of users returned successfully



if __name__ == "__main__":
    unittest.main()
