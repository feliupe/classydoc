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

        #Text preprocessing, tokenizing and filtering of stopwords
        count_vect = CountVectorizer()
        dataset_counts = count_vect.fit_transform(self.dataset.data)

        #Transform
        tf_transformer = TfidfTransformer(use_idf=False)
        dataset_tf = tf_transformer.transform(dataset_counts)

        #Training
        self.classifier = MultinomialNB().fit(dataset_tf, self.dataset.target)

        self.categories = self.dataset.target_names

        return self.classifier

    def store_classifier(self):
         joblib.dump(self.classifier, self.classifier_path)

    def load_classifier(self):
        self.classifier = joblib.load(self.classifier_path)

        return self.classifier


    #TODO: understand -> fix
    def predict(self, fd):
        fd.seek(0)
        count_vect = CountVectorizer()
        count_vect.fit_transform(self.dataset.data)

        new_dataset_counts = count_vect.transform([fd.read()])
        tf_transformer = TfidfTransformer(use_idf=False)
        new_dataset_tf = tf_transformer.transform(new_dataset_counts)

        predicted = self.classifier.predict(new_dataset_counts)

        return predicted[0]

    def category(category_number):
        return categories[category_number]
