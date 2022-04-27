import unittest
from app import app

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTIyNzRkNTc4NmY0MzdjYmIyNWMiLCJhZG1pbiI6dHJ1ZSwiZXhwIjoxNjgyMzQzOTExfQ.b6-oq0j_Uto5NGvyobu4y2BVRjmM_6cUT9zQJ1I9FP8"
header = {"x-access-token":token}

class TestNewAccounts(unittest.TestCase):
    def test_success(self):
        tester = app.test_client(self)
        response= tester.get("admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17",headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test_invalid_input(self):
        tester = app.test_client(self)
        response= tester.get("admin/statistics/new_account_count?start_date=20220415&end_date=20220417",headers = header)
        statuscode = response.status_code
        self.assertEqual(statuscode , 400)

    def test_response_content_type(self):
        tester = app.test_client(self)
        response= tester.get("admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17",headers = header)
        cont_type = response.content_type
        self.assertEqual(cont_type , "application/json")

    #check if returned users are right
    # def test_data(self):
    #     tester = app.test_client(self)
    #     response= tester.get("/admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17",headers = header)
    #     data_returned = response.get_json()
    #     print("******************************")
    #     print(data_returned)
    #     self.assertEqual(data_returned,{"Number of created Users": 3})
if __name__ == "__main__":
    unittest.main()