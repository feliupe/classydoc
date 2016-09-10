#Tutorial: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html#tutorial-setup
#TODO: decouple this
import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import api

from mymodel import Base,db
import os
import pickle as pkl

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn import metrics

class DocClassifier(Base):
    __tablename__ = 'document_classifier'
    id = db.Column(db.Integer, primary_key = True)

    def __init__(self, *args, **kwargs):
        super(DocClassifier, self).__init__(*args, **kwargs)

        self.categories_path = '/home/felipe/Projs/python/classydoc/mymodel/classifier/categories.pkl'
        self.classifier_path = '/home/felipe/Projs/python/classydoc/mymodel/classifier/classifier.pkl'
        self.metrics_path = '/home/felipe/Projs/python/classydoc/mymodel/classifier/metrics.pkl'
        #TODO: pass by params
        self.training_data_path = '/home/felipe/Projs/python/classydoc/api/training_data'
        self.test_data_path = '/home/felipe/Projs/python/classydoc/api/test_data'
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

        self.output_metrics = self._metrics()

        return self.classifier

    def store_classifier(self):
         DocClassifier._store(self.categories, self.categories_path)
         DocClassifier._store(self.output_metrics, self.metrics_path)

         joblib.dump(self.classifier, self.classifier_path)

    def load_classifier(self):
        self.categories = DocClassifier._load(self.categories_path)
        self.output_metrics = DocClassifier._load(self.metrics_path)

        self.classifier = joblib.load(self.classifier_path)

        return self.classifier

    def predict(self, fd=None, text=None, arr=None):
        if fd:
            fd.seek(0)
            txt = [fd.read()]
        elif text:
            txt = [text]
        elif arr:
            txt = arr

        predicted = self.classifier.predict(txt)

        return predicted if arr else predicted[0]

    def category(self, category_number):
        return self.categories[category_number]

    def _store(obj, path):
        with open(path,'bw') as fd:
            fd.write(pkl.dumps(obj))

    def _load(path):
        with open(path,'br') as fd:
            return pkl.loads(fd.read())

    def _metrics(self):
        test_dataset = datasets.load_files(self.test_data_path, encoding="unicode_escape")

        predicted = self.predict(arr=test_dataset.data)

        result = metrics.precision_recall_fscore_support(test_dataset.target, predicted, average=None)
        result = dict(zip(['precision','recall','f1','support'],result))

        return result
