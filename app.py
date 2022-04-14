from flask import Flask


# Importing all Routes
from Routes.Login import Login



# Creating flask application
app = Flask(__name__)


# Registering all the blue prints created in other files
app.register_blueprint(Login, url_prefix='/Login')



# Running the application
if __name__ == '__main__':
    app.run()
