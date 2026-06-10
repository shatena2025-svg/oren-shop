from flask import Flask
from blueprins.general import app as general
from blueprins.admin import app as admin

app = Flask(__name__)

app.register_blueprint(general)
app.register_blueprint(admin)


if __name__ == '__main__':
    app.run(debug=True)