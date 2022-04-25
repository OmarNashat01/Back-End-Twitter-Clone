from json import dumps
from re import X
from app import app 
from flask import json

wrongotp = -1
def test_verify_valid_email(): #Sending an OTP for an Email
    response = app.test_client().get(
        '/verify',
        data = json.dumps({"email": "fbimohammed@yahoo.com"}),
        content_type = 'application/json')

    data = json.loads(response.get_data(as_text=True))
    global x 
    x = data["OTP"]
    assert response.status_code == 200
def test_verify_already_registered_email(): #Email already exist on DB, No OTP
    response = app.test_client().get(
        '/verify',
        data = json.dumps({"email": "mariannaderrr@gmail.com"}),
        content_type = 'application/json')
    assert response.status_code == 400

def test_confirm_email_successufl():
        response = app.test_client().get(
            f"/confirm_email?OTP={str(x)}&email=fbimohammed@yahoo.com"
            )

        assert response.status_code == 200

def test_confirm_email_wrongOTP(): #WrongOTP and correct email address
        response = app.test_client().get(
            f"/confirm_email?OTP={str(wrongotp)}&email=fbimohammed@yahoo.com"
            )

        assert response.status_code == 404

def test_confirm_wrong_email_wrongOTP(): #WrongOTP and wrong email address
        response = app.test_client().get(
            f"/confirm_email?OTP={str(wrongotp)}&email=wrongemail@yahoo.com"
            )

        assert response.status_code == 404

def test_confirm_wrong_email_correctOTP(): #WrongOTP and wrong email address
        test_verify_valid_email()  
        response = app.test_client().get(
            f"/confirm_email?OTP={str(X)}&email=fbimohammed90@yahoo.com"
            )

        assert response.status_code == 404

def test_signup(): #inserting a verfied user in the database  
        response = app.test_client().post(
            "/signup",
            data = json.dumps({
            "email": "mohamedkhaled@yahoo.com",
            "username": "momo",
            "password": "test11111",
            "date_of_birth": "26/08/2001",
            "name": "mohamed"}),
            content_type = 'application/json')

        data = json.loads(response.get_data(as_text=True))





        assert response.status_code == 200

    
def test_signup_failure(): #existing username
        response = app.test_client().post(
            "/signup",
            data = json.dumps({
            "email": "mohamedkhaled@yahoo.com",
            "username": "GakOelGen",
            "password": "test11111",
            "date_of_birth": "26/08/2001",
            "name": "mohamed"}),
            content_type = 'application/json')

        data = json.loads(response.get_data(as_text=True))





        assert response.status_code == 400



    
    