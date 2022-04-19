from flask import Flask


# Importing all Routes
from Routes.Login import Login
from Routes.Friendships.followers import followers
from Routes.Friendships.following import following
from Routes.Statistics.new_accounts import new_accounts_count
from Routes.Statistics.retweets_count import retweets_count


# Creating flask application
app = Flask(__name__)


# Registering all the blue prints created in other files
app.register_blueprint(Login, url_prefix='/Login')
app.register_blueprint(followers, url_prefix='/users/followers')
app.register_blueprint(following, url_prefix='/users/following"')
app.register_blueprint(new_accounts_count, url_prefix='/admin/statistics/new_account_count')
app.register_blueprint(retweets_count, url_prefix='/admin/statistics/retweet_count')


# Running the application
if __name__ == '__main__':
    app.run()
