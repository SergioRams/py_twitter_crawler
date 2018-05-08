from flask import Flask
from flask_restful import Api
from resources.twitter_crawler import Tweets


app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'pyt_crawl_db'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://admin:pass123@ds217310.mlab.com:17310/pyt_crawl_db'
app.secret_key = 'Secret_very_secret'
api = Api(app)


# endpoints
api.add_resource(Tweets, '/page_name/<string:page_name>')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

