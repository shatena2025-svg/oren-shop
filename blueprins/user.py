from flask import Blueprint
from models.user import User

app = Blueprint('user',__name__)

@app.route('/user')
def admin():
    return 'user page'
