#Tutorial: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html#tutorial-setup
#TODO: decouple this
import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import api

from mymodel import Base,db
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

class DocClassifier(Base):

    __tablename__ = 'document_classifier'
    id = db.Column(db.Integer, primary_key = True)

    def __init__(self, *args, **kwargs):
        super(DocClassifier, self).__init__(*args, **kwargs)

        self.classifier_path = 'classifier/classifier.pkl'
        #TODO: pass by params
        self.training_data_path = '/home/felipe/Projs/python/classydoc/api/training_data'
        self.categories = []
        self.classifier = None
        self.dataset = None

    def generate_classifier(self):

        self.dataset = datasets.load_files(self.training_data_path, encoding="unicode_escape")

        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
        ])

        text_clf.fit(self.dataset.data, self.dataset.target)

        self.categories = self.dataset.target_names

        self.classifier = text_clf

        return self.classifier

    def store_classifier(self):
         joblib.dump(self.classifier, self.classifier_path)

    def load_classifier(self):
        self.classifier = joblib.load(self.classifier_path)

        return self.classifier

    #TODO: understand -> fix
    def predict(self, fd):
        fd.seek(0)

        predicted = self.classifier.predict([fd.read()])

        return predicted[0]

    def category(self, category_number):
        return self.categories[category_number]
