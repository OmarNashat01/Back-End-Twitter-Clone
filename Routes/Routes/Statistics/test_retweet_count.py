import unittest
from app import app

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTIyNzRkNTc4NmY0MzdjYmIyNWMiLCJhZG1pbiI6dHJ1ZSwiZXhwIjoxNjgyMzQzOTExfQ.b6-oq0j_Uto5NGvyobu4y2BVRjmM_6cUT9zQJ1I9FP8"
header = {"x-access-token":token}

class TestRetweetCounts(unittest.TestCase):

    #check for response 200, List of users returned successfully
    def test_success(self):
        tester = app.test_client(self)
        response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18",headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test_invalid_input(self):
        tester = app.test_client(self)
        response= tester.get("admin/statistics/retweet_count?start_date=20220415&end_date=20220417",headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 400)

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18",headers = header)
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")

    #check if returned users are right
    # def test_data(self):
    #     tester = app.test_client(self)
    #     response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18")
    #     data_returned = response.get_json()
    #     print("******************************")
    #     print(data_returned)
    #     self.assertEqual(data_returned,{"Number of retweets": 2})

if __name__ == "__main__":
    unittest.main()