from flask import Flask
from views import views


app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret_key_1234567890'  # Set a strong secret key in production
app.register_blueprint(views, url_prefix='/views')

if __name__ == '__main__':
    app.run(debug=True, port=8000)