from flask_app import app
from flask_app.controllers import controllers_users
from flask_app.controllers import controllers_shows



if __name__=="__main__":
    app.run(debug=True)