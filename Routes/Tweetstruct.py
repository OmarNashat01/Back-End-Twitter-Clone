from Database.Database import Database as Client
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from functools import wraps
from jwt import decode
import re

app = Flask(__name__)
x = Api(app)

client = MongoClient(
    "mongodb+srv://karimhafez:KojGCyxxTJXTYKYV@cluster0.buuqk.mongodb.net/twitter?retryWrites=true&w=majority")

objectid_of_like_dates = "625ad8751b0d674357495ccd"

path = "C: \\Users\\LEGION\\Downloads\\photos"

db = client["Twitter_new"]
col_of_tweets = db["tweets"]
col_of_retweets = db["tweets"]
col_of_stats = db["stats"]
col_of_users = db["User"]
col_of_blocked = db["blocked_users"]
col_of_images = db["images"]
col_of_spaces =db["Spaces"]
col_of_trends = db["Hashtags"]
col_of_lists = db["lists"]


def saveimages(files):
    arr = []
    c = 0
    for x in enumerate(files):
       c += 1    
    for x in range(0,c):
        z = files[x]
        z.save(f"storage//{z.filename}")
        arr.append(f"http://45.79.245.94:5000/storage/{z.filename}")
    return arr

def gethashes(para: str,tweetid):
    words  =None
    if para.contains('#'):
        para = para.partition
        para = para[2]
        words = para.split('#')
        for word in range(1,words.length):
           if col_of_trends.find({"wordid":word}) is None:
               col_of_trends.insert({"wordid":word,"related_tweets_ids":[tweetid]})
           else:
               col_of_trends.update({"wordid":word},{"$push":{"related_tweets_ids":tweetid}})
        return True
    else:
        return False




def check_block(current_user):

    user_id = str(current_user['_id'])
    db_response = col_of_blocked.find_one({'_id': user_id})

    if db_response == None:
        return jsonify("not_banned")
    else:
        try:
            decode(db_response['token'], "SecretKey1911", "HS256")
        except:
            col_of_blocked.delete_one({'_id': user_id})
            return 'not_banned'

    return 'banned'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = decode(token, "SecretKey1911", "HS256")
            user_id = ObjectId(data["_id"])
            current_user = col_of_users.find_one({'_id': user_id})
            print(user_id)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        if current_user == None:
            return {"message":"no such user exists in the database"},405

        return f(current_user, *args, **kwargs)

    return decorated

# days between two given dates

# A date has day 'd', month 'm' and year 'y'


class Date:
    def __init__(self, d, m, y):
        self.d = d
        self.m = m
        self.y = y


# To store number of days in all months from
# January to Dec.
monthDays = [31, 28, 31, 30, 31, 30,
             31, 31, 30, 31, 30, 31]

# This function counts number of leap years
# before the given date


def countLeapYears(d):

    years = d.y

    # Check if the current year needs to be considered
    # for the count of leap years or not
    if (d.m <= 2):
        years -= 1

    # An year is a leap year if it is a multiple of 4,
    # multiple of 400 and not a multiple of 100.
    return int(years / 4) - int(years / 100) + int(years / 400)


# This function returns number of days between two
# given dates
def getDifference(dt1, dt2):

    # COUNT TOTAL NUMBER OF DAYS BEFORE FIRST DATE 'dt1'

    # initialize count using years and day
    n1 = dt1.y * 365 + dt1.d

    # Add days for months in given date
    for i in range(0, dt1.m - 1):
        n1 += monthDays[i]

    # Since every leap year is of 366 days,
    # Add a day for every leap year
    n1 += countLeapYears(dt1)

    # SIMILARLY, COUNT TOTAL NUMBER OF DAYS BEFORE 'dt2'

    n2 = dt2.y * 365 + dt2.d
    for i in range(0, dt2.m - 1):
        n2 += monthDays[i]
    n2 += countLeapYears(dt2)

    # return difference between two counts
    return (n2 - n1)





class comment(Resource):
    prof_pic_url: str
    username: str
    _id: str
    user_id: str
    Text: str
    videos_urls: str = []
    images_urls: str = []
    like_count: int
    retweet_count: int
    reply_count: int
    Liked_by: str = []
    replies = []
    created_at: datetime
    needed: str

    def __init__(self, username: str = None, user_id: str = None,
                 text: str = None, videos_url: str = [],
                 images_url: str = [], likes: int = 0, liked_by: str = [], comment_count: int = 0,
                 retweet_count: int = 0,
                 comments=[]):
        self._id = str(len(list(col_of_tweets.find({})))+1)
        self.username = username
        self.user_id = user_id
        self.Text = text
        self.videos_urls = videos_url
        self.images_urls = images_url
        self.like_count = likes
        self.Liked_by = liked_by
        self.retweet_count = retweet_count
        self.reply_count = comment_count
        self.replies = comments
        self.created_at = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    

    def set_pic(self, pic):
        self.prof_pic_url = pic

    def partial_tweet_json(self):
        return {
            "tweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "text": {{self.text}},
            "videos": {{self.videos_urls}},
            "images": {{self.images_urls}},
            "like_count": {{self.like_count}},
            "Retweet_count": {{self.retweet_count}},
            "comment_count": {{self.comment_count}},
        }

    def full_tweet_json(self):
        if self.comments.count() > 0:
            return {
                "comment_id": {{self._id}},
                "user_id": {{self.user_id}},
                "text": {{self.text}},
                "videos": {{self.videos_urls}},
                "images": {{self.images_urls}},
                "like_count": {{self.like_count}},
                "Retweet_count": {{self.retweet_count}},
                "comment_count": {{self.comment_count}},
                "comments": [self.comments]
            }
        else:
            print("tweet doesn't have any comments yet")
            return self.partial_tweet_json()

    def __repr__(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"

    def get(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"


    def set_creation_date(self, date: datetime):
        self.creation_at = date
        
    def set_name(self, name: str):
        self.username = name

    def save_to_database(self):
        x = col_of_tweets.insert_one({
            "type": "comment",
            "tweet_id": self._id,
            "prof_pic_url": self.prof_pic_url,
            "user_id": self.user_id,
            "username": self.username,
            "created_at": self.created_at,
            "text": self.Text,
            "images": self.images_urls,
            "videos": self.videos_urls,
            "like_count": int(self.like_count),
            "retweet_count": int(self.retweet_count),
            "comment_count": int(self.reply_count),
            "Liker_ids": self.Liked_by,
            "comments": self.replies, })
        self.needed = x
        return x

    def get_from_database(self, id):
        tweeter = col_of_tweets.find_one({"_id": ObjectId(id)})
        if col_of_tweets.find_one({"_id": ObjectId(id)}) != None:
            self._id = str(tweeter["_id"])
            self.user_id = tweeter["user_id"]
            self.Text = tweeter["text"]
            self.created_at = tweeter["created_at"]
            self.videos_urls = tweeter["videos"]
            self.images_urls = tweeter["images"]
            self.like_count = tweeter["like_count"]
            self.Liked_by = tweeter["Liker_ids"]
            self.retweet_count = tweeter["retweet_count"]
            self.comment_count = tweeter["comment_count"]
            self.replies = tweeter["comments"]
            self.prof_pic_url = tweeter["prof_pic_url"]
            self.username = tweeter["username"]
        return tweeter

    @staticmethod
    def get_from_database_json(_id):
        return col_of_tweets.find_one({"_id": _id})

    @staticmethod
    def delete_from_database(_id):
       col_of_tweets.delete_one({"_id": _id})


class Tweet(Resource):
    prof_pic_url: str
    username: str
    _id: str
    user_id: str
    Text: str
    videos_urls: str = []
    images_urls: str = []
    like_count: int
    retweet_count: int
    comment_count: int
    Liked_by: str = []
    comments = []
    created_at: datetime
    needed_by: str 

    def __init__(self, username: str = None, user_id: str = None,
                 text: str = None, videos_url: str = [],
                 images_url: str = [], likes: int = 0, liked_by: str = [], comment_count: int = 0,
                 retweet_count: int = 0,
                 comments=[]):
        self._id = str(len(list(col_of_tweets.find({})))+1)
        self.username = username
        self.user_id = user_id
        self.Text = text
        self.videos_urls = videos_url
        self.images_urls = images_url
        self.like_count = likes
        self.Liked_by = liked_by
        self.retweet_count = retweet_count
        self.comment_count = comment_count
        self.comments = comments
        self.created_at = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        

    def add_comment(self, newcomment):
        self.comments.append(newcomment)

    def set_likes(self, likes):
        self.like_count = likes

    def like(self, user_id):
        self.like_count += 1
        self.Liked_by.append(user_id)

    def set_name(self, username):
        self.username = username

    def unlike(self, user_id):
        if self.like_count > 1:
            self.like_count -= 1
            self.Liked_by.append(user_id)

    def retweet_it(self):
        self.retweet_count += 1
        return self._id

    def un_retweet(self):
        if self.retweet_count > 0:
            self.retweet_count -= 1

    def comment_tweet(self, new_comment):
        self.comments.append(new_comment)
        self.comment_count += 1

    def uncomment_tweet(self):
        if self.comment_count > 0:
            self.comment_count -= 1

    def set_pic(self, pic):
        self.prof_pic_url = pic

    def partial_tweet_json(self):
        return {
            "tweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "text": {{self.text}},
            "videos": {{self.videos_urls}},
            "images": {{self.images_urls}},
            "like_count": {{self.like_count}},
            "Retweet_count": {{self.retweet_count}},
            "comment_count": {{self.comment_count}},
        }

    def full_tweet_json(self):
        if self.comments.count() > 0:
            return {
                "comment_id": {{self._id}},
                "user_id": {{self.user_id}},
                "text": {{self.text}},
                "videos": {{self.videos_urls}},
                "images": {{self.images_urls}},
                "like_count": {{self.like_count}},
                "Retweet_count": {{self.retweet_count}},
                "comment_count": {{self.comment_count}},
                "comments": [self.comments]
            }
        else:
            print("tweet doesn't have any comments yet")
            return self.partial_tweet_json()

    def __repr__(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"

    def get(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"

    def get_id(self):
        return self._id

    def get_user_id(self):
        return self.user_id

    def get_text(self):
        return self.Text

    def get_liked_by(self):
        return self.Liked_by

    def get_videos_urls(self):
        return self.videos_urls

    def get_images_urls(self):
        return self.images_urls

    def get_like_count(self):
        return self.like_count

    def get_retweet(self):
        return self.retweet_count

    def get_comments(self):
        return self.comments

    def set_creation_date(self, date: datetime):
        self.creation_at = date

    def save_to_database(self):
        print(self.creation_at)
        self.needed = col_of_tweets.insert_one({
            "type": "tweet",
            "tweet_id": self._id,
            "prof_pic_url": self.prof_pic_url,
            "user_id": self.user_id,
            "username": self.username,
            "created_at": self.created_at,
            "text": self.Text,
            "images": self.images_urls,
            "videos": self.videos_urls,
            "like_count": int(self.like_count),
            "retweet_count": int(self.retweet_count),
            "comment_count": int(self.comment_count),
            "Liker_ids": self.Liked_by,
            "comments": self.comments, })
        return self.get_from_database_json(self._id) == {}

    def get_from_database(self, id):
        tweeter = col_of_tweets.find_one({"_id": ObjectId(id)})
        if col_of_tweets.find_one({"_id": ObjectId(id)}) != None:
            self._id = str(tweeter["_id"])
            self.user_id = tweeter["user_id"]
            self.Text = tweeter["text"]
            self.created_at = tweeter["created_at"]
            self.videos_urls = tweeter["videos"]
            self.images_urls = tweeter["images"]
            self.like_count = tweeter["like_count"]
            self.Liked_by = tweeter["Liker_ids"]
            self.retweet_count = tweeter["retweet_count"]
            self.comment_count = tweeter["comment_count"]
            self.comments = tweeter["comments"]
            self.prof_pic_url = tweeter["prof_pic_url"]
            self.username = tweeter["username"]
        return tweeter

    @staticmethod
    def get_from_database_json(_id):
        return col_of_tweets.find_one({"_id": _id})

    @staticmethod
    def delete_from_database(_id):
       col_of_tweets.delete_one({"_id": _id})
       print(Tweet.get_from_database_json(_id))


class collectionoftweets:
    Tweets: list = []

    def __innit__(self, tweets: list = []):
        self.Tweets = tweets

    def ___repr__(self):
        return f"collection of tweets for easier retrieval"

    def get_from_database(self, pagtoken: int):
        tweets = list(col_of_tweets.find({"type": "tweet"}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "type":tweets[x]["type"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.Tweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.Tweets == []

    def get_random_from_database(self, pagtoken: int,current):
        tweets = list(col_of_tweets.find({"type": "tweet"}))
        blockers = list(col_of_blocked.find({"source_user_id":current},{"_id":0,"source_user_id":0}))
        start = (pagtoken-1)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                if blockers.count({"target_user_id":user["_id"]}) == 0:
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
                else:
                    pass
        elif x1 <= 0:
            return self.Tweets == []

        elif x1 >= 25:
            for x in range(start, end):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                if blockers.count({"target_user_id": user["_id"]}) == 0:
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
                else:
                    pass
        return self.Tweets == []

    def get_from_user_tweets_database(self, pagtoken: int, _id):
        tweets = list(col_of_tweets.find({"type": "tweet", "user_id": _id}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.Tweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.Tweets == []


    def json(self):
        return jsonify({"Tweets": self.Tweets})

    def get_from_liked_tweets_database(self, pagtoken: int, _id):
            tweets = list(col_of_tweets.find({},{"Liker_ids":1}))
            likedtweets = []
            for tweet in tweets:
                for liked in tweet["Liker_ids"]:
                    print(liked)
                    if liked["liker"] == str(_id):
                        likedtweets.append(tweet["_id"])
            print(likedtweets)
            start = (0)*25
            end = pagtoken*25
            x1 = 0
            tweets = list(col_of_tweets.find({"_id":{"$in":likedtweets}}))
            for tweet in list(tweets):
                x1 += 1
            if pagtoken < 1:
                return self.Tweets == []
            if x1 < pagtoken*25:
                for x in range(start, x1):
                    user = col_of_users.find_one(
                        {"_id": ObjectId(tweets[x]["user_id"])})
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
            elif x1 <= 0:
                return self.Tweets == []

            elif x1 >= 25:
                for x in range(start, x1):
                    user = col_of_users.find_one(
                        {"_id": ObjectId(tweets[x]["user_id"])})
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
            return self.Tweets == []

    def get_from_followings_tweets_database(self, pagtoken: int, _id):
        user = col_of_users.find_one({"_id":_id},{"following":1})
        users = []
        for follow in list(user["following"]):
            users.append(ObjectId(follow["user_id"]))
        if users != []:
           tweets = list(col_of_tweets.find(
              {"type": "tweet","user_id":{"$in":users}}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
                x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
                for x in range(start, x1):
                    user = col_of_users.find_one(
                        {"_id": ObjectId(tweets[x]["_id"])})
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
        elif x1 <= 0:
                return self.Tweets == []

        elif x1 >= 25:
                for x in range(start, x1):
                    user = col_of_users.find_one(
                        {"_id": ObjectId(tweets[x]["user_id"])})
                    self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
        return self.Tweets == []

    def get_query_from_database(self, pagtoken:int,string:str):
        regex = re.compile(f"^{string}",re.IGNORECASE)
        tweets = list(col_of_tweets.find({"type": "tweet","text":regex}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.Tweets == []

        elif x1 >= 25:
            for x in range(start, end):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.Tweets == []



class retweet(Resource):
    prof_pic_url: str
    username: str
    _id: str
    user_id: str
    Text: str
    videos_urls: str = []
    images_urls: str = []
    like_count: int
    retweet_count: int
    comment_count: int
    Liked_by: str = []
    comments = []
    created_at: datetime
    refrenced_tweet_id:str
    Quoted: bool
    needed:str

    def __init__(self, username: str = None, user_id: str = None,
                 text: str = None, videos_url: str = [],
                 images_url: str = [],refrenced_tweet_id:str = None, likes: int = 0, liked_by: str = [], comment_count: int = 0,
                 retweet_count: int = 0,
                 comments=[]):
        self._id = str(len(list(col_of_tweets.find({})))+1)
        self.username = username
        self.user_id = user_id
        self.Text = text
        self.videos_urls = videos_url
        self.images_urls = images_url
        self.like_count = likes
        self.Liked_by = liked_by
        self.retweet_count = retweet_count
        self.comment_count = comment_count
        self.comments = comments
        self.created_at = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.refrenced_tweet_id = refrenced_tweet_id

    def add_comment(self, newcomment):
        self.comments.append(newcomment)

    def set_likes(self, likes):
        self.like_count = likes

    def like(self, user_id):
        self.like_count += 1
        self.Liked_by.append(user_id)

    def set_name(self, username):
        self.username = username
        
    def setbool(self, key):
        self.Quoted = key


    def unlike(self, user_id):
        if self.like_count > 1:
            self.like_count -= 1
            self.Liked_by.append(user_id)

    def retweet_it(self):
        self.retweet_count += 1
        return self._id

    def un_retweet(self):
        if self.retweet_count > 0:
            self.retweet_count -= 1

    def comment_tweet(self, new_comment):
        self.comments.append(new_comment)
        self.comment_count += 1

    def uncomment_tweet(self):
        if self.comment_count > 0:
            self.comment_count -= 1

    def set_pic(self, pic):
        self.prof_pic_url = pic

    def partial_tweet_json(self):
        return {
            "retweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "text": {{self.text}},
            "videos": {{self.videos_urls}},
            "images": {{self.images_urls}},
            "like_count": {{self.like_count}},
            "Retweet_count": {{self.retweet_count}},
            "comment_count": {{self.comment_count}},
        }

    def full_tweet_json(self):
        if self.comments.count() > 0:
            return {
                "comment_id": {{self._id}},
                "user_id": {{self.user_id}},
                "text": {{self.text}},
                "videos": {{self.videos_urls}},
                "images": {{self.images_urls}},
                "like_count": {{self.like_count}},
                "Retweet_count": {{self.retweet_count}},
                "comment_count": {{self.comment_count}},
                "comments": [self.comments]
            }
        else:
            print("tweet doesn't have any comments yet")
            return self.partial_tweet_json()

    def __repr__(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"

    def get(self):
        return f"tweet_id: {self._id},user_id: {self.user_id},Text: {self.Text},videos: {self.videos_urls},images: {self.images_urls},like_count: {self.like_count},Retweet_count: {self.retweet_count},comment_count: {self.comment_count},comments: {self.comments}"

    def get_id(self):
        return self._id

    def get_user_id(self):
        return self.user_id

    def get_text(self):
        return self.Text

    def get_liked_by(self):
        return self.Liked_by

    def get_videos_urls(self):
        return self.videos_urls

    def get_images_urls(self):
        return self.images_urls

    def get_like_count(self):
        return self.like_count

    def get_retweet(self):
        return self.retweet_count

    def get_comments(self):
        return self.comments

    def set_creation_date(self, date: datetime):
        self.creation_at = date

    def save_to_database(self):
        self.needed = col_of_tweets.insert_one({
                                                "type": "retweet",
                                                "tweet_id": self._id,
                                                "quoted":self.Quoted,
                                                "prof_pic_url": self.prof_pic_url,
                                                "user_id": self.user_id,
                                                "username": self.username,
                                                "refrenced_tweet_id":self.refrenced_tweet_id,
                                                "created_at": self.created_at,
                                                "text": self.Text,
                                                "images": self.images_urls,
                                                "videos": self.videos_urls,
                                                "like_count": int(self.like_count),
                                                "retweet_count": int(self.retweet_count),
                                                "comment_count": int(self.comment_count),
                                                "Liker_ids": self.Liked_by,
                                                "comments": self.comments, })
        return self.get_from_database_json(self._id) == {}

    def get_from_database(self, id):
        tweeter = col_of_tweets.find_one({"_id": ObjectId(id)})
        tweet_refrenced = col_of_tweets.find_one(
            {"_id": ObjectId(tweeter["refrenced_tweet_id"])})
        if col_of_tweets.find_one({"_id": ObjectId(id)}) != None:
            self._id = str(tweeter["_id"])
            self.user_id = tweeter["user_id"]
            self.refrenced_tweet_id = str(tweeter["refrenced_tweet_id"])
            self.Text = tweeter["text"]
            self.Quoted = tweeter["quoted"]
            self.created_at = tweeter["created_at"]
            self.videos_urls = tweeter["videos"]
            self.images_urls = tweeter["images"]
            self.like_count = tweeter["like_count"]
            self.Liked_by = tweeter["Liker_ids"]
            self.retweet_count = tweeter["retweet_count"]
            self.comment_count = tweeter["comment_count"]
            self.comments = tweeter["comments"]
            self.prof_pic_url = tweeter["prof_pic_url"]
            self.username = tweeter["username"]
        return tweeter

    @staticmethod
    def get_from_database_json(_id):
        return col_of_tweets.find_one({"_id": _id})

    @staticmethod
    def delete_from_database(_id):
       col_of_tweets.delete_one({"_id": _id})
       print(Tweet.get_from_database_json(_id))


class collectionofretweets:
    retweets: list = []

    def __innit__(self, retweets: list = []):
        self.retweets = retweets

    def ___repr__(self):
        return f"collection of retweets for easier retrieval"

    def get_from_database(self, pagtoken: int):
        tweets = list(col_of_tweets.find({"type": "retweet"}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.retweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                tweet = col_of_tweets.find_one({"_id":ObjectId(ID["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images":tweet["images"],
                        "videos":tweet["videos"],
                        "like_count":tweet["like_count"],
                        "retweet_count":tweet["retweet_count"],
                        "comment_count":tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced":new_tweet,
                                    "text": tweets[x]["text"],
                                    "quoted":tweets[x]["quoted"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced": new_tweet,
                                    "text": tweets[x]["text"],
                                    "quoted": tweets[x]["quoted"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.retweets == []

    def get_random_from_database(self, pagtoken: int,current):
        tweets = list(col_of_tweets.find({"type": "retweet"}))
        blockers = list(col_of_blocked.find(
            {"source_user_id": current}, {"_id": 0, "source_user_id": 0}))
        start = (pagtoken-1)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.retweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(ID["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                if blockers.count({"target_user_id": user["_id"]}) == 0:
                    self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "quoted":tweets[x]["quoted"],
                                        "tweet_refrenced": new_tweet,
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
            else:
                pass
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, end):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                if blockers.count({"target_user_id": user["_id"]}) == 0:
                    self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                        "user_id": str(tweets[x]["user_id"]),
                                        "username": tweets[x]["username"],
                                        "name": user["name"],
                                        "bio": user["bio"],
                                        "followers_count": user["followers_count"],
                                        "following_count": user["followers_count"],
                                        "prof_pic_url": tweets[x]["prof_pic_url"],
                                        "quoted": tweets[x]["quoted"],
                                        "tweet_refrenced": new_tweet,
                                        "text": tweets[x]["text"],
                                        "created_at": tweets[x]["created_at"],
                                        "videos": tweets[x]["videos"],
                                        "images": tweets[x]["images"],
                                        "type": tweets[x]["type"],
                                        "like_count": tweets[x]["like_count"],
                                        "liked_by_ids": tweets[x]["Liker_ids"],
                                        "retweet_count": tweets[x]["retweet_count"],
                                        "comment_count": tweets[x]["comment_count"],
                                        "comments": tweets[x]["comments"]})
                else:
                    pass
        return self.retweets == []
    
    def get_from_liked_tweets_database(self, pagtoken: int, _id):
        tweets = list(col_of_tweets.find({}, {"Liker_ids": 1}))
        likedtweets = []
        for tweet in tweets:
            for liked in tweet["Liker_ids"]:
                print(liked)
                if liked["liker"] == str(_id):
                    likedtweets.append(tweet["_id"])
        print(likedtweets)
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        tweets = list(col_of_tweets.find({"_id": {"$in": likedtweets}}))
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.retweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                      "user_id": str(tweets[x]["user_id"]),
                                      "username": tweets[x]["username"],
                                      "name": user["name"],
                                      "bio": user["bio"],
                                      "followers_count": user["followers_count"],
                                      "following_count": user["followers_count"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "tweet_refrenced": new_tweet,
                                      "text": tweets[x]["text"],
                                      "quoted": tweets[x]["quoted"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "type": tweets[x]["type"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                      "user_id": str(tweets[x]["user_id"]),
                                      "username": tweets[x]["username"],
                                      "name": user["name"],
                                      "bio": user["bio"],
                                      "followers_count": user["followers_count"],
                                      "following_count": user["followers_count"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "tweet_refrenced": new_tweet,
                                      "text": tweets[x]["text"],
                                      "quoted": tweets[x]["quoted"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "type": tweets[x]["type"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        return self.retweets == []
            

    def get_from_user_tweets_database(self, pagtoken: int, _id):
        tweets = list(col_of_tweets.find({"type": "retweet", "user_id": _id}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.retweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                tweet = col_of_tweets.find_one({"_id":ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced": new_tweet,
                                    "text": tweets[x]["text"],
                                    "quoted": tweets[x]["quoted"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                tweet = col_of_tweets.find_one({"_id":ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced": new_tweet,
                                    "text": tweets[x]["text"],
                                    "quoted": tweets[x]["quoted"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.retweets == []
    
    def get_query_from_database(self, pagtoken: int, string: str):
        regex = re.compile(f"^{string}",re.IGNORECASE)
        tweets = list(col_of_tweets.find(
            {"type": "retweet", "text":regex}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(ID["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced": new_tweet,
                                    "text": tweets[x]["text"],
                                    "quoted":tweets[x]["quoted"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, end):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "tweet_refrenced": new_tweet,
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "quoted": tweets[x]["quoted"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.retweets == []
    
    def get_from_followings_tweets_database(self, pagtoken: int, _id):
        user = col_of_users.find_one({"_id": _id}, {"following": 1})
        users = []
        for follow in list(user["following"]):
            users.append(ObjectId(follow["user_id"]))
        if users != []:
           tweets = list(col_of_tweets.find(
               {"type": "retweet", "user_id": {"$in": users}}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.retweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                ID = tweets[x]
                user = col_of_users.find_one({"_id": ObjectId(ID["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(ID["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                      "user_id": str(tweets[x]["user_id"]),
                                      "username": tweets[x]["username"],
                                      "name": user["name"],
                                      "bio": user["bio"],
                                      "followers_count": user["followers_count"],
                                      "following_count": user["followers_count"],
                                      "quoted": tweets[x]["quoted"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "tweet_refrenced": new_tweet,
                                      "text": tweets[x]["text"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "type": tweets[x]["type"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.retweets == []

        elif x1 >= 25:
            for x in range(start, end):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                tweet = col_of_tweets.find_one(
                    {"_id": ObjectId(tweets[x]["refrenced_tweet_id"])})
                if tweet == None:
                    new_tweet = "None"
                else:
                    new_tweet = {
                        "tweet_id": str(tweet["_id"]),
                        "user_id": str(tweet["user_id"]),
                        "username": str(tweet["username"]),
                        "prof_pic_url": str(tweet["prof_pic_url"]),
                        "text": tweet["text"],
                        "images": tweet["images"],
                        "videos": tweet["videos"],
                        "like_count": tweet["like_count"],
                        "retweet_count": tweet["retweet_count"],
                        "comment_count": tweet["comment_count"]
                    }
                self.retweets.append({"tweet_id": str(tweets[x]["_id"]),
                                      "user_id": str(tweets[x]["user_id"]),
                                      "username": tweets[x]["username"],
                                      "name": user["name"],
                                      "bio": user["bio"],
                                      "followers_count": user["followers_count"],
                                      "following_count": user["followers_count"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "tweet_refrenced": new_tweet,
                                      "text": tweets[x]["text"],
                                      "quoted": tweets[x]["quoted"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "type": tweets[x]["type"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        return self.retweets == []

    def json(self):
        return jsonify({"retweets": self.retweets})

class collectionofcomments:
    Tweets: list = []

    def __innit__(self, tweets: list = []):
        self.Tweets = tweets

    def ___repr__(self):
        return f"collection of tweets for easier retrieval"

    def get_from_tweet_comments_database(self, pagtoken: int, _id):
        tweet = col_of_tweets.find_one({"_id":_id})
        comment_ids = []
        if tweet["comments"] == []:
            return []
        for com in list(tweet["comments"]):
            comment_ids.append(ObjectId(com))
        tweets = list(col_of_tweets.find({"type": "comment","_id":{"$in":comment_ids}}))
        start = (0)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if pagtoken < 1:
            return self.Tweets == []
        if x1 < pagtoken*25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(tweets[x]["user_id"])})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif x1 <= 0:
            return self.Tweets == []

        elif x1 >= 25:
            for x in range(start, x1):
                user = col_of_users.find_one(
                    {"_id": ObjectId(_id)})
                self.Tweets.append({"tweet_id": str(tweets[x]["_id"]),
                                    "user_id": str(tweets[x]["user_id"]),
                                    "username": tweets[x]["username"],
                                    "name": user["name"],
                                    "bio": user["bio"],
                                    "followers_count": user["followers_count"],
                                    "following_count": user["followers_count"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "type": tweets[x]["type"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.Tweets == []


    def json(self):
        return jsonify({"Tweets": self.Tweets})

        



