import unittest
from retweets_count import app


class TestRetweetCounts(unittest.TestCase):

    #check for response 200, List of users returned successfully
    def test_success(self):
        tester = app.test_client(self)
        response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18")
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test_invalid_input(self):
        tester = app.test_client(self)
        response= tester.get("admin/statistics/retweet_count?start_date=20220415&end_date=20220417")
        statuscode = response.status_code
        self.assertEqual(statuscode , 400)

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18")
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")

    #check if returned users are right
    def test_data(self):
        tester = app.test_client(self)
        response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18")
        data_returned = response.get_json()
        print("******************************")
        print(data_returned)
        self.assertEqual(data_returned,{"Number of retweets": 2})

if __name__ == "__main__":
    unittest.main()