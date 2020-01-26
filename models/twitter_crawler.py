import twitter
from db import db

api = twitter.Api(consumer_key='Ez7sZdUmLcOFe0mBWkMEahuX6',
                  consumer_secret='duYR0I84UY0wZ0PqJfiz0ez3F4tupcP15JANu4PZKu69XI02mo',
                  access_token_key='243951999-jA71XWRYW1Qw83kIdXfpLdeQoON8qSSbQ0qCVEeQ',
                  access_token_secret='f2ODvlmoGAGgGFGis68TOy9wx3c7g5WuSZ7vhFatVV8Bl')


class TwitterPageModel(db.Model):
    """
    Model for a twitter page, this model contains just the name of the twitter profile
    """

    # CREATE TABLE twitter_page
    __tablename__ = 'twitter_page'
    # create columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # back reference
    posts = db.relationship('TwitterPostModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """
        :return: returns a dictionary representation of this object
        """
        return {'page_name': self.name, 'posts': [post.json() for post in self.posts.all()]}

    def save_to_db(self):
        """
        INSERT INTO twitter_page ...
        UPDATE twitter_page SET ...
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        DELETE FROM twitter_page WHERE ...
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        """
        SELECT * FROM twitter_page WHERE name = (param: name) LIMIT 1
        :param name of the twitter page(profile)
        :return: TwitterPage model object
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        """
        SELECT * FROM twitter_page
        :return: TwitterPage model objects
        """
        return cls.query.all()


class TwitterPostModel(db.Model):

    # CREATE TABLE posts_page
    __tablename__ = 'posts_page'
    # create columns
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    source = db.Column(db.String(500))
    likes = db.Column(db.Integer)
    sentiment = db.Column(db.String(10))
    positive_proba = db.Column(db.Float(precision=2))
    created_at = db.Column(db.String(20))

    # Foreign key relationship to page parent table
    page_id = db.Column(db.Integer, db.ForeignKey('twitter_page.id'))
    name = db.relationship('TwitterPageModel')

    def __init__(self, text, source, likes, sentiment, positive_proba, created_at, page_id):
        self.text = text
        self.source = source
        self.likes = likes
        self.sentiment = sentiment
        self.positive_proba = positive_proba
        self.created_at = created_at
        self.page_id = page_id

    def json(self):
        """
        :return: returns a dictionary representation of this object
        """
        return {'text': self.text,
                'source': self.source,
                'likes': self.likes,
                'sentiment': self.sentiment,
                'positive_proba': self.positive_proba,
                'created_at': self.created_at,
                'page_id': self.page_id}

    def save_to_db(self):
        """
        INSERT INTO posts_page ...
        UPDATE posts_page SET ...
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        DELETE FROM posts_page WHERE ...
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_posts_by_page(cls, page_name):
        """
        SELECT * FROM posts_page WHERE page_name == (param: page_name)
        :return: posts_page model objects
        """
        return cls.query.filter_by(name=page_name)

    @classmethod
    def find_all(cls):
        """
        SELECT * FROM posts_page
        :return: posts_page model objects
        """
        return cls.query.all()
