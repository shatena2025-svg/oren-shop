from flask import Blueprint

app = Blueprint('user',__name__)

@app.route('/user')
def admin():
    return 'user page'
