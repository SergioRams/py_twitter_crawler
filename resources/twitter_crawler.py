from flask_restful import Resource, reqparse
from models.twitter_crawler import TwitterPage, TwitterPost, api


class Tweets(Resource):

    def get(self, page_name):
        page = TwitterPage.find_by_name(page_name)

        if page:
            return {'tweets': [page.json() for page in TwitterPost.find_by_page(page)]}, 200

        return {'message': 'Page not found.'}, 404

    def post(self, page_name):
        if TwitterPage.find_by_name(page_name):
            return {"message": "This page has already been stalked!."}, 400  # user error

        # call Twitter API
        t = api.GetUserTimeline(screen_name=page_name, count=50)
        tweets = [i.AsDict() for i in t]

        # for t in tweets:
        #    print(t)

        # saves tweets and page
        if tweets:
            twitter_page = TwitterPage(page_name=page_name)
            twitter_page.save_to_db()

            for t in tweets:
                post = TwitterPost(id_str=t['id_str'],
                                   page_name=twitter_page,
                                   text=t['text'],
                                   source=t['source'],
                                   likes=t['user']['favourites_count'],
                                   created_at=t['created_at'])
                try:
                    post.save_to_db()
                except:
                    return {'message': 'An error occurred inserting Posts into database.'}, 500  # internal server error

        page = TwitterPage.find_by_name(page_name)
        return {'tweets': [page.json() for page in TwitterPost.find_by_page(page)]}, 201


