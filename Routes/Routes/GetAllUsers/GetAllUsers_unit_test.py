import sys
from wsgiref import headers
sys.path.append("..")
from json import dumps
from GetAll import app 
import sys
from Login.Login import app
from flask import json

def test_admin(): #admin using the command GETALL
    
    response = app.test_client().post(
      '/Login',
      data = json.dumps({"email": "fbimoaadahammead@yahoo.com",
      "password": "yahoome.com"}),
      content_type = 'application/json')

    data = json.loads(response.get_data(as_text=True))
    token = data['token']
    headers = {'x-access-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjI1YjQyNTY4MDA0MGFmNjgwNDlmNmNhIiwiQWRtaW4iOnRydWUsImV4cCI6MTY1MDMwOTIwNn0.JiIXTuhKmIzoFLIP5ON4MEAt6WeueyPVGf3yamLMiXg'}

    response2 = app.test_client().get(
      f'/users/all?offset={0}&limit={10}',
      headers = headers)

    assert response2.status_code == 200




     
