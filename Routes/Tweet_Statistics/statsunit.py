import unittest
from app import app


#sub class from testcase class


class TestTweets(unittest.TestCase):

    #check for response 200, tweet returned successfully
    def test_success(self):
        tester = app.test_client(self)
        response = tester.get(
            "/admin/statistics/like_count?start_date=2022-4-20&end_date=2021-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid tweetID
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.get("/admin/statistics/like_count?start_date=2020-4-20&end_date=2021-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, tweet Doesnt Exist
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.get(
            "/admin/statistics/like_count?start_date=2025-4-20&end_date=2023-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    #check for response 200, List of tweets returned successfully

    def test_success(self):
        tester = app.test_client(self)
        response = tester.get(
            "/admin/statistics/tweet_count?start_date=2022-4-20&end_date=2021-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #check for response 400, User entered Invalid page number
    def test_invalid_input(self):
        tester = app.test_client(self)
        response = tester.get("/admin/statistics/tweet_count?start_date=2021-4-20&end_date=2023-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    #check for response 404, page number doesnt hold anything
    def test_not_found(self):
        tester = app.test_client(self)
        response = tester.get(
            "/admin/statistics/tweet_count?start_date=2026-4-20&end_date=2025-01-01")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    

   


if __name__ == "__main__":
    unittest.main()
