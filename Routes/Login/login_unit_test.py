from json import dumps
from Login import app 
from flask import json



def test_correct_email_password():

   response = app.test_client().post(
      '/Login',
      data = json.dumps({"email": "galalaksamps@gmail.com",
      "password": "yahoome.com"}),
      content_type = 'application/json')

   data = json.loads(response.get_data(as_text=True))
   assert response.status_code == 200
   assert 'token' in data

def test_correct_email_wrong_password():

   response = app.test_client().post(
      '/Login',
      data = json.dumps({"email": "galalaksamps@gmail.com",
      "password": "yahoome2.com"}),
      content_type = 'application/json')

   data = json.loads(response.get_data(as_text=True))
   assert response.status_code == 400



def test_wrong_email_wrong_password():

   response = app.test_client().post(
      '/Login',
      data = json.dumps({"email": "wrongemail@gmail.com",
      "password": "yahoome2.com"}),
      content_type = 'application/json')

   data = json.loads(response.get_data(as_text=True))
   assert response.status_code == 400


   
    
