# import unittest
# from wsgiref import headers
# from app import app
# import json
# from Routes.Tweetstruct import col_of_tweets,col_of_users
# import pymongo 
# from bson import ObjectId
# from Database.Database import Database
# # sub class from testcase class


# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTIyNzRkNTc4NmY0MzdjYmIyNWMiLCJhZG1pbiI6dHJ1ZSwiZXhwIjoxNjgyMzQzOTExfQ.b6-oq0j_Uto5NGvyobu4y2BVRjmM_6cUT9zQJ1I9FP8"
# header = {"x-access-token": token}
# user_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MjY1NTFmNDRkNTc4NmY0MzdjYmIyNWIiLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTY4MjM0MzQ5MX0.8xbJXtfITqlxM1YwdaRV1kr1qXRtvQJ3glhjxNdOPD4"
# header2 = {"x-access-token": user_token}

# tweet2 = col_of_tweets.find_one({"_id":{"$ne":ObjectId("6266b4bc234280718fc89ecf")}})
# tweettobedeleted = tweet2["_id"]
# user1 = col_of_users.find_one({"_id":ObjectId("626551f44d5786f437cbb25b")},{"following.user_id":1,"_id":0})
# print(user1)
# user = col_of_users.find_one({"_id":{"$nin":list(user1["following"])}})
# header1 = {"x-access-token": token}
# data = {"source_user_id": "626551f44d5786f437cbb25b",
#         "target_user_id": "6265b8efc557bc4aa2f038ab"}
# codes = [200,400]
# OTP = 0



# class TestRetweetCounts(unittest.TestCase):
    
#     #check for response 200, List of users returned successfully
#     def test_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18",headers = header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode , 200)
#         print(response)
#         print("_________________________________________________")
#         print("retweet count success")

#     def test_invalid_input(self):
#         tester = app.test_client(self)
#         response= tester.get("admin/statistics/retweet_count?start_date=20220415&end_date=20220417",headers = header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode , 400)
#         print(response)
#         print("_________________________________________________")
#         print("retweet count failure due to invalid input")

#     def test_response_content_type(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18",headers = header)
#         cont_type = response.content_type
#         self.assertEqual(cont_type , "application/json")
#         print(response)
#         print("_________________________________________________")
#         print("retweet count returned  content type is valid")

#     # #check if returned users are right
#     # def test_data(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/admin/statistics/retweet_count?start_date=2022-04-15&end_date=2022-04-18", headers=header)
#     #     data_returned = response.get_json()
#     #     print("******************************")
#     #     print(data_returned)
#     #     self.assertEqual(data_returned,{"Number of retweets": 2})
# class TestNewAccounts(unittest.TestCase):
#     def test_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print(response)
#         print("_________________________________________________")
#         print("new account count returned successfully")

#     def test_invalid_input(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "admin/statistics/new_account_count?start_date=20220415&end_date=20220417", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
#         print(response)
#         print("new account invalid input test")

#     def test_response_content_type(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17", headers=header)
#         cont_type = response.content_type
#         self.assertEqual(cont_type, "application/json")
#         print("new account count returned content type is valid")

#     #check if returned users are right
#     # def test_data(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/admin/statistics/new_account_count?start_date=2022-04-15&end_date=2022-04-17",headers = header)
#     #     data_returned = response.get_json()
#     #     print("******************************")
#     #     print(data_returned)
#     #     self.assertEqual(data_returned,{"Number of created Users": 3})
# class TestFollowUser(unittest.TestCase):
#     def test_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.post("/users/following", json=data, headers=header)
#         statuscode = response.status_code
#         self.assertIn(statuscode,codes)
#         print("_________________________________________________")
#         print("user follow returned successfully")
#         print(response)
# ## Uncomment to try to follow once otherwise it will return used followed

#     # def test_response_data(self):
#     #     tester = app.test_client(self)
#     #     response= tester.post("/users/following",json = data)
#     #     data_returned = response.get_json()
#     #     print("******************************")
#     #     print(data_returned)
#     #     self.assertEqual(data_returned,{"Message": "Sucessfully followed the user"})


# class TestFollowingList(unittest.TestCase):
#     def test_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/users/following?user_id=626551f44d5786f437cbb25b", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("following returned successfully")
#         print("_________________________________________________")

#     def test_not_found(self):
#         tester = app.test_client(self)
#         response = tester.get(
#             "/users/following?user_id=625560f7e10c0b48c19d2cb0", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("user not found")
#         print("_________________________________________________")

#     # def test_no_following(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/users/following?user_id=625560c0e10c0b48c19d2cb5")
#     #     statuscode = response.status_code
#     #     self.assertEqual(statuscode , 204)
#     #     print("_________________________________________________")
#     #     print("User have no followers")

#     def test_response_content_type(self):
#         tester = app.test_client(self)
#         response = tester.get(
#             "/users/following?user_id=626551f44d5786f437cbb25b", headers=header)
#         cont_type = response.content_type
#         self.assertEqual(cont_type, "application/json")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("Valid data returned")
#         print("_________________________________________________")

#     #check if returned users are right
#     # def test_data(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/users/following?user_id=625560f7e10c0b48c19d2cb6")
#     #     data_returned = response.get_json()
#     #     self.assertEqual(data_returned,karim_user)
#     #     print("******************************")
#     #     print(data_returned)
# class TestFollowersList(unittest.TestCase):

#     # #check for response 200, List of users returned successfully
#     # def test_success(self):
#     #     tester = app.test_client(self)
#     #     print("_________________________________________________")
#     #     response = tester.get(
#     #         "/users/followers?user_id=626552274d5786f437cbb25c", headers=header)
#     #     statuscode = response.status_code
#     #     self.assertEqual(statuscode, 200)
#     #     print(response.status_code)
#     #     print(response)
#     #     print("followers retrieval of user followers success")
#     #     print("_________________________________________________")

#     def test_not_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/users/followers?user_id=625560f7e10c0b48c19d2cb0", headers=header1)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print(response.status_code)
#         print(response)
#         print("tests if user does not exist through followers retrieval")
#         print("_________________________________________________")

#     # def test_no_followers(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/users/followers?user_id=625560c0e10c0b48c19d2cb5")
#     #     statuscode = response.status_code
#     #     self.assertEqual(statuscode , 204)

#     def test_response_content_type(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/users/followers?user_id=626552274d5786f437cbb25c", headers=header1)
#         cont_type = response.content_type
#         self.assertEqual(cont_type, "application/json")
#         print(response.status_code)
#         print(response)
#         print("followers retrieval of user followers success")
        

#     #check if returned users are right
#     # def test_data(self):
#     #     tester = app.test_client(self)
#     #     response= tester.get("/users/followers?user_id=626552274d5786f437cbb25c")
#     #     data_returned = response.get_json()
#     #     print("******************************")
#     #     print(data_returned)
#     #     self.assertEqual(data_returned,karim_user)
# class TestTweets(unittest.TestCase):
#     # check for response 200, tweet returned successfully

#     def test_get_tweet_success(self):
#         print("_________________________________________________")
#         tester = app.test_client(self)
#         response = tester.get(
#             "/tweets/tweet_id?Id=6266b4bc234280718fc89ecf", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("tweet is returned")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_tweet_success")

#     # check for response 400, User entered Invalid tweetID
#     def test_invalid_ID_get_tweet_input(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get("/tweets/tweet_id?Id=", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
#         print("Invalid Id")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_invalid_ID_get_tweet_input")

#     # check for response 404, tweet Doesnt Exist
#     def test_tweet_not_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/tweets/tweet_id?Id=626446fa02862871daa00931", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print("tweet is not in the database")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_tweet_not_found")
        

#     # check for response 200, List of tweets returned successfully

#     def test_get_random_tweet_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get("/tweets/random?page=1", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("random tweets are returned")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_random_tweet_success")

#     # check for response 400, User entered Invalid tweetID

#     def test_get_user_tweet_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/tweets/all?Id=6265b8efc557bc4aa2f038ab", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("user tweets are returned")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_user_tweet_success")

#     # check for response 400, User entered Invalid tweetID
#     def test_invalid_ID_user_get_tweets_input(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get("/tweets/all?Id=", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
#         print("invalid user id")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_invalid_ID_user_get_tweets_input")

#     # check for response 404, tweet Doesnt Exist
#     def test_get_user_tweets_not_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/tweets/all?Id=626551f44d5226f437cbb25b", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print("user tweets are not found")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_user_tweets_not_found")

#     def test_get_my_tweets_success(self):
#         tester = app.test_client(self)
#         response = tester.get("/tweets/all/me", headers=header)
#         print("_________________________________________________")
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("my tweets are returned")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_my_tweets_success")

#     def test_post_tweet_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.post("/tweets", data=json.dumps({
#             "text": "i am new here",
#             "images": [],
#             "videos": []
#         }),
#             content_type='application/json', headers=header,follow_redirects=True)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_post_tweet_success")


#     def test_delete_tweet_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.delete(
#             f"/tweets?Id={tweettobedeleted}", headers=header, follow_redirects=True)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_delete_tweet_success")

#     # check for response 400, User entered Invalid tweetId
#     def test_delete_tweet_failure(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.delete(
#             "/tweets?Id=626446fa02862861daa00921", headers=header,follow_redirects=True)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_delete_tweet_failure")


# class TestUsers(unittest.TestCase):

#     # # check for response 200, user returned successfully
#     # def test_get_user_success(self):
#     #     print("_________________________________________________")
#     #     tester = app.test_client(self)
#     #     response = tester.get(
#     #         "/users/user_id?_id=626551f44d5786f437cbb25b", headers=header)
#     #     statuscode = response.status_code
#     #     self.assertEqual(statuscode, 200)
#     #     print("user is returned")
#     #     print("_________________________________________________")
#     #     print(response.status_code)
#     #     print(response)
#     #     print("test_get_user_success")

#     # check for response 404, User ID not found
#     def test_get_user_not_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/users/user_id?_id=626551f44d5786f437cbb259", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)
#         print("User ID not found")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_user_not_found")

#     # check for response 200, me returned successfully
#     def test_get_me_success(self):
#         print("_________________________________________________")
#         tester = app.test_client(self)
#         response = tester.get(
#             "/users/me", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("Me is returned")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_get_me_success")

#     # check for response 200, User updated successfully
#     def test_update_user_success(self):
#         print("_________________________________________________")
#         tester = app.test_client(self)
#         response = tester.put("/users/update_profile", data=json.dumps({
#             "name": "SHAHD",
#             "date_of_birth": "2002-04-25",
#             "bio": "i love painting",
#             "location": "cairo, egypt",
#             "website": "www.mywebsite.com",
#             "prof_pic_url": "https://pbs.twimg.com/media/EEI178KWsAEC79p.jpg",
#             "cover_pic_url": "https://i.pinimg.com/564x/a2/64/b4/a264b464b6fd6138d972448e19ba764d.jpg"
#         }),
#             content_type='application/json', headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("User has been updated")
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_update_user_success")


# class TestTweetsstats(unittest.TestCase):
#     def test_like_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/like_count?end_date=2022-4-20&start_date=2021-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_like_success")

#     #check for response 400, User entered Invalid tweetID
#     def test_invalid_like_count_input(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/like_count?start_date=2022-4-20&end_date=2021-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_invalid_like_count_input")

#     #check for response 404, tweet Doesnt Exist
#     def test_not_like_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/like_count?end_date=2025-4-20&start_date=2023-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_not_like_found")

#     #check for response 200, List of tweets returned successfully

#     def test_tweet_count_success(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/tweet_count?end_date=2022-4-20&start_date=2021-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_tweet_count_success")

#     #check for response 400, User entered Invalid page number
#     def test_invalid_tweet_count_input(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/tweet_count?start_date=2021-4-20&end_date=2020-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_invalid_tweet_count_input")

#     #check for response 404, page number doesnt hold anything
#     def test_tweet_count_not_found(self):
#         tester = app.test_client(self)
#         print("_________________________________________________")
#         response = tester.get(
#             "/admin/statistics/tweet_count?end_date=2026-4-20&start_date=2025-01-01", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print("_________________________________________________")
#         print(response.status_code)
#         print(response)
#         print("test_tweet_count_not_found")
# class test_Login(unittest.TestCase):
    
#     def test_correct_email_password(self):
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.post("/Login", data=json.dumps({
#             "email": "mohamedmohsen96661@gmail.com",
#             "password": "yahoome.com"
#         }),
#             content_type='application/json')
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 201)


#     def test_correct_email_wrong_password(self):
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.post("/Login", data=json.dumps({
#             "email": "mohamedmohsen96661@gmail.com",
#             "password": "yahoomae.com"
#         }),
#             content_type='application/json')
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)
    
#     def test_wrong_email_address(self):
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.post("/Login", data=json.dumps({
#             "email": "notemail@gmail.com",
#             "password": "yahoaomae.com"
#         }),
#             content_type='application/json', headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 404)

#     def test_signup_OTP(self): #inserting a verfied user in the database 

#         tester = app.test_client(self)
#         response = tester.post("/signup/verify", data=json.dumps({
#             "email": "mohamedmadboly@gmail.com"
#         }),
#             content_type='application/json', headers=header)
#         data = json.loads(response.get_data(as_text=True))
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)


    


#     def test_signup(self): #inserting a verfied user in the database  
        
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.post("/signup", data=json.dumps({
#             "email": "mohameaadmohsen@gmail.com",
#             "password": "yahoaomae.com",
#             "username": "never_inserted",
#             "date_of_birth": "26/08/2001",
#             "name": "mohamed",
#             "website": "facebook",
#             "location": "egpyt",
#             "gender": "M",

#         }),
#             content_type='application/json', headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         data = json.loads(response.get_data(as_text=True))
#         response = Database.User.delete_one({"username": "never_inserted"})
    
#     def test_signup_existing_username(self): #inserting a verfied user in the database  
        
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.post("/signup", data=json.dumps({
#             "email": "mohameaadmohsen@gmail.com",
#             "password": "yahoaomae.com",
#             "username": "MakOelGen",
#             "password": "test11111",
#             "date_of_birth": "26/08/2001",
#             "name": "mohamed",
#             "website": "facebook",
#             "bio": "hello",
#             "location": "egpyt",
#             "gender": "M",

#         }),
#             content_type='application/json', headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 400)




#     def test_get_all_admin(self): #admin using the command GETALL
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.get(f"/users/all?offset={0}&limit={10}", headers=header)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#         print(response.status_code)
#         print(response)

#     def test_get_all_non_admin(self): #admin using the command GETALL
#         print("_________________")
#         tester = app.test_client(self)
#         response = tester.get(f"/users/all?offset={0}&limit={10}", headers=header2)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 403)
#         print(response.status_code)
#         print(response) 

# if __name__ == "__main__":
#     unittest.main()
#     # if successful_tests != no_of_tests:
#     #     print(f"{(successful_tests/no_of_tests)*100}%")
