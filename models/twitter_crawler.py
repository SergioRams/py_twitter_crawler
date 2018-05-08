import twitter
from db import db

api = twitter.Api(consumer_key='Ez7sZdUmLcOFe0mBWkMEahuX6',
                  consumer_secret='duYR0I84UY0wZ0PqJfiz0ez3F4tupcP15JANu4PZKu69XI02mo',
                  access_token_key='243951999-jA71XWRYW1Qw83kIdXfpLdeQoON8qSSbQ0qCVEeQ',
                  access_token_secret='f2ODvlmoGAGgGFGis68TOy9wx3c7g5WuSZ7vhFatVV8Bl')


class TwitterPage(db.Document):

    page_name = db.StringField()

    def save_to_db(self):
        self.save()

    @classmethod
    def find_by_name(cls, page_name):
        return cls.query.filter(cls.page_name == page_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {'page_name': self.page_name}


class TwitterPost(db.Document):
    id_str = db.StringField()
    page_name = db.DocumentField(TwitterPage)
    text = db.StringField()
    source = db.StringField()
    likes = db.IntField()
    created_at = db.StringField()

    def save_to_db(self):
        self.save()

    @classmethod
    def find_by_page(cls, page_name):
        return cls.query.filter(cls.page_name == page_name)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {'id_str': self.id_str,
                'text': self.text,
                'source': self.source,
                'likes': self.likes,
                'created_at': self.created_at}
