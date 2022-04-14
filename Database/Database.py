from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/admin")
    Database = client.Twitter_new
except: 
    print("can't connect")

