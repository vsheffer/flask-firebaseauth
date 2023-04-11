import os

import requests
from flask import json
import unittest

from flask import Flask
from flask_firebaseauth import FirebaseAuth
from firebase_admin import initialize_app, auth


def sign_in_with_email_and_password(email, password):
    request_ref = "http://localhost:9098/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-api-key"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    return request_object.json()


test_user_email: str = "jdoe@acme.com"
test_user_password: str = "3290423092340932"

os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9098"
initialize_app()
user = auth.create_user(email=test_user_email, password=test_user_password, email_verified=True)
authenticated_user = sign_in_with_email_and_password(email=test_user_email, password=test_user_password)
print(f"authenticated_user={authenticated_user}")
id_token = authenticated_user['idToken']


class FirebaseAuthTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)

        app.config['firebase_AUTH_USERNAME'] = 'john'
        app.config['firebase_AUTH_PASSWORD'] = 'matrix'

        firebase_auth = FirebaseAuth(auth=auth, app=app)

        @app.route('/')
        def normal_view():
            return 'This view does not normally require authentication.'

        @app.route('/protected')
        @firebase_auth.required
        def protected_view():
            return 'This view always requires authentication.'

        self.app = app
        self.firebase_auth = firebase_auth
        self.client = app.test_client()

    @staticmethod
    def make_header(token: str):
        return {'Authorization': f"Bearer {token}"}

    def test_views_without_firebase_auth_decorator_respond_with_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_responds_with_401_without_authorization(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

    def test_asks_for_authentication(self):
        response = self.client.get('/protected')
        self.assertIn('WWW-Authenticate', response.headers)
        self.assertEqual(
            response.headers['WWW-Authenticate'],
            'Bearer realm=""'
        )

    def test_asks_for_authentication_with_custom_realm(self):
        self.app.config['FIREBASE_AUTH_REALM'] = 'Secure Area'
        response = self.client.get('/protected')
        self.assertIn('WWW-Authenticate', response.headers)
        self.assertEqual(
            response.headers['WWW-Authenticate'],
            'Bearer realm="Secure Area"'
        )

    def test_responds_with_401_with_incorrect_credentials(self):
        response = self.client.get(
            '/protected',
            headers=self.make_header("invalid id token")
        )
        self.assertEqual(response.status_code, 401)

    def test_responds_with_200_with_correct_credentials(self):
        response = self.client.get(
            '/protected',
            headers=self.make_header(id_token)
        )
        self.assertEqual(response.status_code, 200)

    def test_runs_decorated_view_after_authentication(self):
        response = self.client.get(
            '/protected',
            headers=self.make_header(id_token)
        )
        self.assertEqual(
            response.data,
            b'This view always requires authentication.'
        )


def suite():
    return unittest.makeSuite(FirebaseAuthTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
