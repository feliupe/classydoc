import unittest
import base64
import os
import api
import json
from io import BytesIO

import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import mymodel
from mymodel.user import User
import mymodel.config as dbconfig

class ApiTestCase(unittest.TestCase):

    def create_test_dir_tree(self):
        os.makedirs(os.path.join(self.test_root,'documents'), exist_ok=True)

    def remove_test_dir_tree(self):
        import shutil
        shutil.rmtree(self.test_root)

    def setUp(self):
        api.create_app('config.Test')
        dbconfig.create_tables(api.engine)
        self.app = api.app.test_client()
        self.test_root = api.app.config["APPLICATION_ROOT"]

        self.create_test_dir_tree()

        self.user = User(username="admin", password_hash="secret")
        api.session.add(self.user)
        api.session.commit()

        res = self.open_with_auth('/api/token', 'GET', self.user.username, self.user.password_hash)
        self.token = res.headers['token']

    def tearDown(self):
        #TODO: make it more secure
        if self.test_root.endswith('/api') or not self.test_root.endswith('/test'):
            raise Exception("Fail to clear /test directory. APPLICATION_ROOT ends with '/api' or not ends with '/test'")
        else:
            self.remove_test_dir_tree()

    def authorization_header(self,user,password):
        return {'Authorization': 'Basic ' + base64.b64encode(bytes(user + \
        ":" + password, 'ascii')).decode('ascii')}

    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
            method=method,
            headers=self.authorization_header(username,password)
        )

    def test_login(self):
        res = self.open_with_auth('/api/token', 'GET', self.user.username, self.user.password_hash)
        self.assertEqual(200, res.status_code)
        self.assertGreater(len(res.headers['token']), 1)

    def test_register_user(self):
        res = self.app.post('/user/register', data=dict(user='felipe',password="secret"))

        self.assertEqual('felipe',  res.headers['user'])

        user = api.session.query(User).filter(User.username == 'felipe').first()
        self.assertEqual('secret', user.password_hash)

    def test_get_document_list(self):
        res = self.app.get('user/documents',headers=self.authorization_header(self.token,'unused'))

        self.assertEqual(res.headers['Content-Type'], 'application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data.decode('ascii'))['documents'], api.documents)

    def test_upload_file(self):

        test_files = {
            'file1': (BytesIO(b'content1'), 'f1.txt'),
            'file2': (BytesIO(b'content2'), 'f2.txt')
        }

        resp = self.app.post(
            '/user/send',
            data = test_files,
            headers=self.authorization_header(self.token,'unused')
        )

        #TODO: check files and content
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
