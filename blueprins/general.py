from flask import Blueprint

app = Blueprint('general',__name__)

@app.route('/')
def main():
    return 'main page'

@app.route('/about')
def about():
    return 'about us'