import bcrypt
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
db = client["twitter"]
user_time_line_obj = db["user_timeline"]


@app.route("/signup", metods=["POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        if user_time_line_obj.find_one({'email': email}) != None:
            password = request.form.get("password")
            password_byte = bytes(password, "ascii")
            hashed_pw = bcrypt.hashpw(password_byte, bcrypt.gensalt())
            app.db.user_timeline.insert_one({"email": email, "password": hashed_pw})


