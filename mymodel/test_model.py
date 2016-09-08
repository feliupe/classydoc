import unittest, numpy as np
from doc_classifier import DocClassifier


class ApiTestCase(unittest.TestCase):

    def comp_np_dicts(self, d1,d2):

        _bool = True
        for k in set(d1.keys()) | set(d2.keys()):
            if type(d1[k]) == np.ndarray:
                _bool = _bool & np.all(d1[k] == d2[k])
            else:
                _bool = _bool & (d1[k] == d2[k])
            if not _bool:
                break

        return _bool

    def test_doc_classifier(self):
        dc = DocClassifier()

        clf = dc.generate_classifier()

        dc.store_classifier()

        #TODO: look for better test
        self.assertTrue(self.comp_np_dicts(dc.load_classifier().__dict__, clf.__dict__))

if __name__ == '__main__':
    unittest.main()
