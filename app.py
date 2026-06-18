from flask import Flask,redirect,url_for,flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from blueprins.general import app as general
from blueprins.admin import app as admin
from blueprins.user import app as user
from models.user import User
from extentions import db
import config

app = Flask(__name__)

app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY   
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash('وارد حساب کاربریتان شوید')
    return redirect(url_for('user.login'))

db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)