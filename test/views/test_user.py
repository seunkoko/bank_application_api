import json
import pytest

try:
    from test.base import create_flask_app
    from api.models import db, User
except ImportError:
    from bank_application_api.test.base import BaseTestCase
    from bank_application_api.api.models import db, User


class UserSignupTestCase(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

    def test_request_is_valid_json(self):
        response = self.client.post('/signup/', content_type='text/plain')
        response_data = json.loads(response.data)

        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['data']['message'], 'Request must be a valid JSON')
        self.assert400(response)

    def test_signup_with_no_firstname(self):
        new_user = {
            'firstname': '',
            'lastname': 'test',
            'middlename': 'a',
            'email': 'test',
            'password': 'password',
            'account_amount': 1000.01
        }
        fields = '(account_amount, firstname, lastname, middlename, email and password)'
        response = self.client.post('/signup', data=json.dumps(new_user),
                    content_type='application/json')
        response_data = json.loads(response.data)
        self.assert400(response)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['data']['message'], 
          'None of these fields {0} are allowed to be empty or of invalid type'.format(fields))

    def test_empty_signup_fields(self):
        new_user = {
            'lastname': 'test',
            'middlename': 'a',
            'username': 'test',
            'email': 'test',
        }
        fields = '(account_amount, firstname, lastname, middlename, email and password)'
        response = self.client.post('/signup', data=json.dumps(new_user),
                    content_type='application/json')
        response_data = json.loads(response.data)
        self.assert400(response)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['data']['message'], 
          'These fields are required on signup {0}'.format(fields))

    def test_user_account_created_successfully(self):
        new_user = {
            'firstname': 'Tami',
            'lastname': 'Lister',
            'middlename': 'Middle',
            'email': 'tami@lister.com',
            'password': 'password1234',
            'account_amount': 6000
        }
        response = self.client.post('/signup', data=json.dumps(new_user),
                    content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['message'], "User created succesfully")
