from flask import Blueprint

app = Blueprint('general',__name__)

@app.route('/')
def main():
    return 'main page'