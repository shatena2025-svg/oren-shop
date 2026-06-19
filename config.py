SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:1234@localhost/oren_shop"

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'

SECRET_KEY = 'sghhlbnkjgffjgfgh456789ihgdfghjkln45tdfghjkfcvbgjhhgh'

PAYMENT_MERCHANT = "sandbox"
PAYMENT_CALLBACK = "http://127.0.0.1:5000/verify"

PAYMENT_FIRST_REQUEST = 'https://sandbox.shepa.com/api/v1/token'
PAYMENT_VERIFY_REQUEST = 'https://sandbox.shepa.com/api/v1/verify'