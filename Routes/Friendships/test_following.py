import json
import unittest
from wsgiref import headers
from app import app

data =  {"source_user_id": "626551f44d5786f437cbb25b","target_user_id":"626552274d5786f437cbb25c"}
#karim_user = {"following":[{"name":"Karim","user_name":"Karim5213","email":"Karim@gmail.com"}]}
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTFmNDRkNTc4NmY0MzdjYmIyNWIiLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTY4MjM0MzQ5MX0.8xbJXtfITqlxM1YwdaRV1kr1qXRtvQJ3glhjxNdOPD4"
header = {"x-access-token":token}

class TestFollowUser(unittest.TestCase):
    def test_success(self):
        tester = app.test_client(self)
        response= tester.post("/users/following",json = data,headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)
        print("_________________________________________________")
        print("Successful request")
## Uncomment to try to follow once otherwise it will return used followed

    # def test_response_data(self):
    #     tester = app.test_client(self)
    #     response= tester.post("/users/following",json = data)
    #     data_returned = response.get_json()
    #     print("******************************")
    #     print(data_returned)
    #     self.assertEqual(data_returned,{"Message": "Sucessfully followed the user"})

class TestFollowingList(unittest.TestCase):
    def test_success(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=626551f44d5786f437cbb25b",headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)
        print("_________________________________________________")
        print("Successful request")

    def test_not_found(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb0",headers=header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 404)
        print("_________________________________________________")
        print("User Not Found")

    # def test_no_following(self):
    #     tester = app.test_client(self)
    #     response= tester.get("/users/following?user_id=625560c0e10c0b48c19d2cb5")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode , 204)   
    #     print("_________________________________________________")
    #     print("User have no followers")

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=626551f44d5786f437cbb25b",headers=header)
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")
        print("_________________________________________________")
        print("Valid data returned")

    #check if returned users are right
    # def test_data(self):
    #     tester = app.test_client(self)
    #     response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb6")
    #     data_returned = response.get_json()
    #     self.assertEqual(data_returned,karim_user)
    #     print("******************************")
    #     print(data_returned)

if __name__ == "__main__":
    unittest.main()