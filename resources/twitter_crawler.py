from flask_restful import Resource, reqparse
from models.twitter_crawler import TwitterPageModel, TwitterPostModel, api
from ml_model.machine_learning import MachineLearning


class Tweets(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('count',
                        type=int,
                        required=True,
                        help="Specify how many tweets to get."
                        )

    def get(self, twitter_page):
        page = TwitterPageModel.find_by_name(twitter_page)

        if page:
            return {'tweets': [post.json() for post in TwitterPostModel.find_posts_by_page(page)]}, 200

        return {'message': 'There are no posts for this page yet.'}, 404

    def post(self, twitter_page):
        # retrieve data from parser
        data = self.parser.parse_args()
        # Create Machine Learning Model Object
        ml_model = MachineLearning()

        # call Twitter API to look for page and number of tweets on the given page
        list_of_tweets = api.GetUserTimeline(screen_name=twitter_page, count=data['count'])

        # if API found list of tweets, save page to database
        if list_of_tweets:
            list_of_tweets = [i.AsDict() for i in list_of_tweets]
            # check if page already exists in database
            page = TwitterPageModel.find_by_name(name=twitter_page)
            if not page:
                page = TwitterPageModel(name=twitter_page)
                page.save_to_db()

            # save each one to database
            for tweet in list_of_tweets:
                if 'favorite_count' not in tweet:  # not all tweets have the likes field apparently
                    tweet['favorite_count'] = 0

                # Machine Learning, send text to transform and make a prediction
                prediction, probs = ml_model.make_prediction(tweet['text'])

                post = TwitterPostModel(text=tweet['text'],
                                        source=tweet['source'],
                                        likes=tweet['favorite_count'],
                                        created_at=tweet['created_at'],
                                        sentiment=prediction,
                                        positive_proba=probs[0, 1],  # positive proba
                                        page_id=page.id,)
                try:
                    post.save_to_db()
                except:
                    # internal server error
                    return {'message': 'An error occurred inserting Posts into database.'}, 500

            return {'tweets': [post.json() for post in TwitterPostModel.find_posts_by_page(page)]}, 201

        else:
            return {'message': 'This page does not exists or has no public tweets.'}, 404
