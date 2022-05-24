#import imp
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
from Routes.Tweets.extra import Tweet_app1
from Routes.Tweets.search import Home_app
from Routes.user_block_user.user_block_user import user_block_user
from Routes.user_unblock_user.user_unblock_user import user_unblock_user
from Routes.get_blocked_user.get_blocked_users import get_blocked_users
from Routes.forgot_password.forgot_password import forgot_password
from Routes.change_password.change_password import change_password
from Routes.block_user.post_block import block
from Routes.block_user.get_blocked import getblock
#### notifications ###
from Routes.notifications.get_all_notifications_of_user import all_notifications
from Routes.notifications.get_by_notification_id import notification_by_id
from Routes.notifications.get_specific_notification_type_for_auser import notification_by_type
# Creating flask application
app = Flask(__name__, template_folder='Templates')
app.config.from_pyfile('config.cfg')
mail.init_app(app)

app.secret_key = "MakO"





# Registering all the blue prints created in other files

# Notifications
app.register_blueprint(all_notifications, url_prefix = '/users/notifications')
app.register_blueprint(notification_by_id, url_prefix = '/users')
app.register_blueprint(notification_by_type, url_prefix = '/users/notifications')
# Notifications

app.register_blueprint(Login, url_prefix='/Login')
app.register_blueprint(GetAll, url_prefix='/users')
app.register_blueprint(signup, url_prefix='/signup')
app.register_blueprint(block, url_prefix='/admin')
app.register_blueprint(getblock, url_prefix='/admin')
app.register_blueprint(Home_app,url_prefix='/home')
app.register_blueprint(followers, url_prefix='/users')
app.register_blueprint(following, url_prefix='/users')
app.register_blueprint(new_accounts_count, url_prefix='/admin/statistics')
app.register_blueprint(retweets_count, url_prefix='/admin/statistics')
app.register_blueprint(Tweet_app, url_prefix='/tweets')
app.register_blueprint(Tweet_app1, url_prefix='/users')
app.register_blueprint(Tweet_stats, url_prefix='/admin/statistics')

app.register_blueprint(get_me, url_prefix='/users')
app.register_blueprint(get_user, url_prefix='/users')
app.register_blueprint(update_user, url_prefix='/users')

app.register_blueprint(user_block_user, url_prefix='/users')
app.register_blueprint(user_unblock_user, url_prefix='/users')
app.register_blueprint(get_blocked_users, url_prefix='/users')
app.register_blueprint(forgot_password, url_prefix='/users')
app.register_blueprint(change_password, url_prefix='/users')


CORS(app)


# Running the application
if __name__ == '__main__':
    app.run(host='0.0.0.0')
