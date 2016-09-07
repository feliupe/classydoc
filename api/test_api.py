import unittest
import base64
import os
import api

import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import mymodel
from mymodel.user import User
import mymodel.config as dbconfig

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        api.create_app('config.Test')
        dbconfig.create_tables(api.engine)
        self.app = api.app.test_client()

    def tearDown(self):
        pass

    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes(username + \
                ":" + password, 'ascii')).decode('ascii')
            }
        )

    def test_login(self):
        res = self.open_with_auth('/user/login', 'POST', 'admin',
                                  'secret')

    def test_register_user(self):

        res = self.app.post('/user/register', data=dict(user='felipe',password="secret"))

        self.assertEqual('felipe',  res.headers['user'])
        
        user = api.session.query(User).filter(User.username == 'felipe').first()
        self.assertEqual('secret', user.password_hash)

if __name__ == '__main__':
    unittest.main()
