from flask import Flask
from flask_restful import Api
from resources.twitter_crawler import Tweets

# App set up
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


# endpoints
api.add_resource(Tweets, '/twitter_page/<string:twitter_page>')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
