from flask_app import app
from flask_app.controllers import controllers_users
from flask_app.controllers import controllers_games



if __name__=="__main__":
    app.run(debug=True)