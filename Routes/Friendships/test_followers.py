import unittest
from followers import app


karim_user = {"followers":[{"name":"Karim","user_name":"Karim5213","email":"Karim@gmail.com"}]}

class TestFollowersList(unittest.TestCase):

    #check for response 200, List of users returned successfully
    def test_success(self):
        tester = app.test_client(self)
        response= tester.get("/users/followers?user_id=625560f7e10c0b48c19d2cb6")
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test_not_found(self):
        tester = app.test_client(self)
        response= tester.get("/users/followers?user_id=625560f7e10c0b48c19d2cb0")
        statuscode = response.status_code
        self.assertEqual(statuscode , 404)

    def test_no_followers(self):
        tester = app.test_client(self)
        response= tester.get("/users/followers?user_id=625560c0e10c0b48c19d2cb5")
        statuscode = response.status_code
        self.assertEqual(statuscode , 204)   

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("/users/followers?user_id=625560f7e10c0b48c19d2cb6")
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")

    #check if returned users are right
    def test_data(self):
        tester = app.test_client(self)
        response= tester.get("/users/followers?user_id=625560f7e10c0b48c19d2cb6")
        data_returned = response.get_json()
        print("******************************")
        print(data_returned)
        self.assertEqual(data_returned,karim_user)

if __name__ == "__main__":
    unittest.main()