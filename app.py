from flask import Flask
from blueprins.general import app as general
from blueprins.admin import app as admin
from blueprins.user import app as user
from extentions import db
import config

app = Flask(__name__)

app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY   


db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)