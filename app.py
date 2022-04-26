from flask import Flask
from flask_cors import CORS

#Importing all Routes

from Routes.Friendships.followers import followers
from Routes.Friendships.following import following
from Routes.Statistics.new_accounts import new_accounts_count
from Routes.Statistics.retweets_count import retweets_count
from Routes.Tweet_Statistics.tweet_stats import Tweet_stats
from Routes.Tweets.Tweets import Tweet_app
from Routes.Login.Login import Login
from Routes.GetAllUsers.GetAll import GetAll
from Routes.Signup.signup import signup, mail
from Routes.get_me.get_me import get_me
from Routes.get_user.get_user import get_user
from Routes.update_user.update_user import update_user



# Creating flask application
app = Flask(__name__, template_folder='Templates')
app.config.from_pyfile('config.cfg')
mail.init_app(app)
CORS(app, resources=r'/*')

# Registering all the blue prints created in other files
app.register_blueprint(Login, url_prefix='/Login')
app.register_blueprint(GetAll, url_prefix='/users')
app.register_blueprint(signup, url_prefix='/signup')
app.register_blueprint(followers, url_prefix='/users/followers')
app.register_blueprint(following, url_prefix='/users/following"')
app.register_blueprint(new_accounts_count, url_prefix='/admin/statistics/new_account_count')
app.register_blueprint(retweets_count, url_prefix='/admin/statistics/retweet_count')
app.register_blueprint(Tweet_app,url_prefix='/tweets')
app.register_blueprint(Tweet_stats,url_prefix='/admin/statistics/')
app.register_blueprint(get_me, url_prefix='/users')
app.register_blueprint(get_user, url_prefix='/users')
app.register_blueprint(update_user, url_prefix='/users')


# Running the application
if __name__ == '__main__':
    app.run(host='0.0.0.0')
