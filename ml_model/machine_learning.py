import pickle
import re
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


class TextStemming(BaseEstimator, TransformerMixin):
    """
    Text Stemming transformers: implements PorterStemmer()
    This class is used as a sklearn pipeline
    """

    def __init__(self):
        self.porter = PorterStemmer()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # custom transformer
        X = X.apply(self.stem_sentences)

        return X

    def stem_sentences(self, sentence):
        tokens = sentence.split()
        stemmed_tokens = [self.porter.stem(token) for token in tokens]

        return ' '.join(stemmed_tokens)


class TextCleanUp(BaseEstimator, TransformerMixin):
    """
    Custom Transformer Class that uses regex to cleanup tweets text
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        This method is meant to do some text cleaning:
        Removes left and right white spaces, HTML links, numbers, etc.
        """

        # trim/strip left and right whitespaces
        X = X.str.strip()
        # removes hyperlinks - I will assume that they don't add much value
        X = X.apply(lambda x: re.sub(r'https?:\/\/.*\/\w*', '', str(x)))
        # removes HTML special sintax such as &amp;
        X = X.apply(lambda x: re.sub(r'\&\w*;', '', str(x)))
        # Remove hashtags
        X = X.apply(lambda x: re.sub(r'#\w*', '', str(x)))
        # removes digits
        X = X.apply(lambda x: re.sub(r'\d+', '', str(x)))

        return X


class MachineLearning:
    """
    This class should receive a text input, transform it using sk-learn pipeline and output a prediction
    """

    ML_MODEL_PATH = 'ml_model/lrc_model.pkl'
    VOCABULARY_PATH = 'ml_model/vocab.pkl'
    TDIDF_MODEL_PATH = 'ml_model/tfidf_model.pkl'

    def __init__(self):
        # loads machine learning pre-trained model and extra tools from file
        self.ml_model = self._load_file(self.ML_MODEL_PATH)
        self.vocab = self._load_file(self.VOCABULARY_PATH)
        self.tfidf_vectorizer = self._load_file(self.TDIDF_MODEL_PATH)

    @staticmethod
    def _load_file(file):
        """ Loads model from file """
        with open(file, 'rb') as file:
            pickle_file = pickle.load(file)

        return pickle_file

    def pipeline(self, tweet, fit=False):
        """
        :param tweet: string input
        :param fit: fit_transform default True
        :return: sparse matrix TfidfVectorizer representation of the tweet
        """

        # stopwords to ignore based on personal bias (this is a subset of the NLTK full list of english words)
        forbidden_words = ['it', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                           'a', 'an', 'the', 'and', 'of', 'at', 'by', 'for', 'before', 'after', 'above', 'below',
                           'to', 'from', 'then', 'here', 'when', 'so', 'than', 'too', 'very', 's', 't', 'just',
                           'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'i', 'you', 'my', 'in', 'on', 'have', "i'm",
                           '-', 'its', 'im', 'u', 'what']

        pipeline = Pipeline([
            # text clean up transformer
            ('text_clean', TextCleanUp()),
            # Porter stemmer used
            ('text_stemming', TextStemming()),
            # tfidf transformer to create a sparse matrix of words
            ('tfidf', self.tfidf_vectorizer),
        ])

        if fit:
            transformed_tweet = pipeline.fit_transform(tweet)
        else:
            transformed_tweet = pipeline.transform(tweet)
        return transformed_tweet

    def make_prediction(self, tweet, fit=False):
        """
        :param tweet: string input
        :param fit: fit_transform default True
        :return: predicted class, prediction probability
        """

        # creating pandas type input to datapipeline transform on new data
        data = pd.DataFrame([tweet], columns=['tweets'])

        # apply transformation pipeline to tweet(s)
        transformed_tweet = self.pipeline(data['tweets'])

        # use model to get the predictions
        predictions = self.ml_model.predict(transformed_tweet)
        probs = self.ml_model.predict_proba(transformed_tweet)

        if predictions == 1:
            class_predictions = 'Positive'
        else:
            class_predictions = 'Negative'

        return class_predictions, probs
