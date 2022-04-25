import json
import unittest
from following import app

data =  {"source_user_id": "62556148e10c0b48c19d2cb9","target_user_id":"62556130e10c0b48c19d2cb8"}
karim_user = {"following":[{"name":"Karim","user_name":"Karim5213","email":"Karim@gmail.com"}]}

class TestFollowUser(unittest.TestCase):
    def test_success(self):
        tester = app.test_client(self)
        response= tester.post("/users/following",json = data)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

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
        response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb6")
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test_not_found(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb0")
        statuscode = response.status_code
        self.assertEqual(statuscode , 404)

    def test_no_following(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=625560c0e10c0b48c19d2cb5")
        statuscode = response.status_code
        self.assertEqual(statuscode , 204)   

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb6")
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")

    #check if returned users are right
    def test_data(self):
        tester = app.test_client(self)
        response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb6")
        data_returned = response.get_json()
        print("******************************")
        print(data_returned)
        self.assertEqual(data_returned,karim_user)

if __name__ == "__main__":
    unittest.main()