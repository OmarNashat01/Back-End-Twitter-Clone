from Database import Client
from flask import Flask, request, jsonify
from flask_restx import Resource
import pymongo
from datetime import datetime
from bson import ObjectId
from functools import wraps
from jwt import encode, decode
#from setuptools import setup
#from multiprocessing import Process,Manager


objectid_of_like_dates = "625ad8751b0d674357495ccd"

db = Client["Twitter_new"]
col_of_tweets = db["tweets"]
col_of_retweets = db["tweets"]
col_of_stats = db["stats"]
col_of_users = db["User"]



class Reply(Resource):
    _id: str
    user_id: str
    Text: str

    def __innit__(self, _id: str = None, user_id: str = None, text: str = None):
        self._id = _id
        self.user_id = user_id
        self.Text = text

    def set_id(self, _id: str):
        self._id = _id

    def set_user_id(self, user_id: str):
        self.user_id = user_id

    def set_text(self, text: str):
        self.Text = text

    def json(self):
        return {
            "_id": {{self._id}},
            "user_id": {{self.user_id}},
            "Text": {{self.Text}}
        }


class comment(Resource):
    _id: str
    user_id: str
    Text: str
    videos_urls: str = []
    images_urls: str = []
    like_count: int
    reply_count: int
    replies: Reply = []

    def __init__(self, _id: str, user_id: str, text: str, videos_urls: str, images_urls: str, like_count: int,
                 reply_count: int):
        self._id = _id
        self.user_id = user_id
        self.Text = text
        self.video_urls = videos_urls
        self.image_urls = images_urls
        self.like_count = like_count
        self.reply_count = reply_count

    def add_reply(self, new_reply: Reply):
        self.replies.append(new_reply)

    def set_likes(self, likes):
        self.like_count = likes

    def like(self, user_id):
        self.like_count += 1
        self.Liked_by.append(user_id)

    def unlike(self, user_id):
        if self.like_count > 1:
            self.like_count -= 1
            self.liked_by.append(user_id)

    def reply_comment(self, new_reply: Reply):
        self.replies.append(new_reply)
        self.reply_count += 1

    def unreply_comment(self):
        if self.reply_count > 0:
            self.reply_count -= 1

    def json(self):
        return {
            "tweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "Text": {{self.text}},
            "videos": {{self.videos_urls}},
            "images": {{self.images_urls}},
            "like_count": {{self.like_count}},
            "replies_count": {{self.reply_count}}
        }

    def full_comment_json(self):
        if self.replies.count() > 0:
            return {
                "tweet_id": {{self._id}},
                "user_id": {{self.user_id}},
                "Text": {{self.text}},
                "videos": {{self.videos_urls}},
                "images": {{self.images_urls}},
                "like_count": {{self.like_count}},
                "replies_count": {{self.reply_count}},
                "Replies": {{comment.replies.json()}}}

        else:
            print("tweet doesn't have any comments yet")
            return self.json()


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
        self.created_at = datetime.now().strftime("%d-%m-%Y")

    def add_comment(self, newcomment):
        self.comments.append(newcomment)

    def set_likes(self, likes):
        self.like_count = likes

    def like(self, user_id):
        self.like_count += 1
        self.Liked_by.append(user_id)

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

    def partial_tweet_json(self):
        return {
            "tweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "Text": {{self.text}},
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
                "Text": {{self.text}},
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
        col_of_tweets.insert_one({
            "Type": "tweet",
            "tweet_id": self._id,
            "prof_pic_url": "string",
            "user_id": self.user_id,
            "username": self.username,
            "created_at": self.created_at,
            "Text": self.Text,
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
        print(tweeter)
        if col_of_tweets.find_one({"_id": ObjectId(id)}) != None:
            self._id = str(tweeter["_id"])
            self.user_id = tweeter["user_id"]
            self.Text = tweeter["Text"]
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
        start = (pagtoken-1)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if x1 < pagtoken*25:
            for x in range(start, x1):
                self.Tweets.append({"tweet_id": tweets[x]["tweet_id"],
                                    "user_id": tweets[x]["user_id"],
                                    "username": tweets[x]["username"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["Text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        elif  x1 <= 1:
            return self.Tweets == []

        elif pagtoken >= 1:
            for x in range(start, end):
                self.Tweets.append({"tweet_id": tweets[x]["tweet_id"],
                                    "user_id": tweets[x]["user_id"],
                                    "username": tweets[x]["username"],
                                    "prof_pic_url": tweets[x]["prof_pic_url"],
                                    "text": tweets[x]["Text"],
                                    "created_at": tweets[x]["created_at"],
                                    "videos": tweets[x]["videos"],
                                    "images": tweets[x]["images"],
                                    "like_count": tweets[x]["like_count"],
                                    "liked_by_ids": tweets[x]["Liker_ids"],
                                    "retweet_count": tweets[x]["retweet_count"],
                                    "comment_count": tweets[x]["comment_count"],
                                    "comments": tweets[x]["comments"]})
        return self.Tweets == []

    def json(self):
        return jsonify({"Tweets": self.Tweets})


class retweet(Resource):
    _id: str
    username: str
    user_id: str
    Refrenced_Tweet_Id: str
    Text: str
    videos_urls: str
    images_urls: str
    like_count: int
    retweet_count: int
    comment_count: int
    Liked_by: str
    comments: comment = []
    refrenced_tweet: Tweet

    def __init__(self, _id: str = None, username: str = None, user_id: str = None, refrenced_tweet_id: str = None,
                 text: str = None,
                 videos_url: str = None, images_url: str = None, likes: int = 0, comment_count: int = 0,
                 retweet_count: int = 0, commented: comment = []):
        self._id = _id
        self.user_id = user_id
        self.username = username
        self.Refrenced_Tweet_Id = refrenced_tweet_id
        self.Text = text
        self.videos_urls.append(videos_url)
        self.images_urls.append(images_url)
        self.like_count = likes
        self.retweet_count = retweet_count
        self.comment_count = comment_count
        self.comments = commented
        self.get_refrenced_tweet(refrenced_tweet_id)

    def __repr__(self):
        return f"'tweet_id': {self._id},'user_id': {self.user_id},'Text': {self.Text},'videos': {self.videos_urls},'images': {self.images_urls},'like_count': {self.like_count},'Retweet_count': {self.retweet_count},'comment_count': {self.comment_count},'Liked_by':{self.liked_by},'comments': {self.comments}"

    def get(self):
        return f"'tweet_id': {self._id},'user_id': {self.user_id},'Text': {self.Text},'videos': {self.videos_urls},'images': {self.images_urls},'like_count': {self.like_count},'Retweet_count': {self.retweet_count},'comment_count': {self.comment_count},'Liked_by':{self.liked_by},'comments': {self.comments}"

    def get_refrenced_tweet(self):
        self.tweet = Tweet()
        self.tweet.get_from_database(self.Refrenced_Tweet_Id)

    def add_comment(self, newcomment: comment):
        self.comments.append(newcomment)

    def set_likes(self, likes):
        self.like_count = likes

    def like(self, user_id):
        self.like_count += 1
        self.Liked_by.append(user_id)

    def unlike(self, user_id):
        if self.like_count > 1:
            self.like_count -= 1
            self.Liked_by.append(user_id)

    def retweet_it(self):
        self.retweet_count += 1
        return self._id

    def unretweet_it(self):
        if self.retweet_count > 0:
            self.retweet_count -= 1

    def comment_tweet(self, new_comment: comment):
        self.comments.append(new_comment)
        self.comment_count += 1

    def uncomment_tweet(self, comment_id: str):
        if self.comment_count > 0:
            self.comment_count -= 1
            self.comments[comment_id]

    def partial_tweet_json(self):
        return {
            "tweet_id": {{self._id}},
            "user_id": {{self.user_id}},
            "Refrenced_Tweet_id": {{self.Refrenced_Tweet_Id}},
            "Text": {{self.text}},
            "videos": {{self.videos_urls}},
            "images": {{self.images_urls}},
            "like_count": {{self.like_count}},
            "Retweet_count": {{self.retweet_count}},
            "comment_count": {{self.comment_count}},
            "comments": []
        }

    def full_tweet_json(self):
        if self.comments.count() > 0:
            return {
                "tweet_id": {{self._id}},
                "user_id": {{self.user_id}},
                "Refrenced_Tweet_id": {{self.Refrenced_Tweet_Id}},
                "Text": {{self.text}},
                "videos": {{self.videos_urls}},
                "images": {{self.images_urls}},
                "like_count": {{self.like_count}},
                "Retweet_count": {{self.retweet_count}},
                "comment_count": {{self.comment_count}},
                "comments": [self.comments.json()]
            }
        else:
            print("tweet doesn't have any comments yet")
            return self.partial_tweet_json()

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

    def save_to_database(self):
        col_of_retweets.insert_one(self.full_tweet_json())

    @staticmethod
    def get_from_database(_id):
        return col_of_retweets.find({"_id": _id})


class collectionofretweets:
    retweets: list = []

    def __innit__(self, retweets: list = []):
        self.retweets = retweets

    def ___repr__(self):
        return f"collection of tweets for easier retrieval"

    def get_from_database(self, pagtoken: int):
        tweets = list(col_of_tweets.find({"type": "retweet"}))
        start = (pagtoken-1)*25
        end = pagtoken*25
        x1 = 0
        for tweet in list(tweets):
            x1 += 1
        if x1 < pagtoken*25:
            for x in range(start, x1):
                self.retweets.append({"tweet_id": tweets[x]["tweet_id"],
                                      "user_id": tweets[x]["user_id"],
                                      "username": tweets[x]["username"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "text": tweets[x]["Text"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        elif x1 <= 1:
            return self.retweets == []

        elif pagtoken >= 1:
            for x in range(start, end):
                self.retweets.append({"tweet_id": tweets[x]["tweet_id"],
                                      "user_id": tweets[x]["user_id"],
                                      "username": tweets[x]["username"],
                                      "prof_pic_url": tweets[x]["prof_pic_url"],
                                      "text": tweets[x]["Text"],
                                      "created_at": tweets[x]["created_at"],
                                      "videos": tweets[x]["videos"],
                                      "images": tweets[x]["images"],
                                      "like_count": tweets[x]["like_count"],
                                      "liked_by_ids": tweets[x]["Liker_ids"],
                                      "retweet_count": tweets[x]["retweet_count"],
                                      "comment_count": tweets[x]["comment_count"],
                                      "comments": tweets[x]["comments"]})
        return self.Tweets == []

    def json(self):
        return jsonify({"retweets": self.retweets})
