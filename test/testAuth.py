from webtest import TestApp
from auth import application

import os

app = TestApp(application)

# It should return 401 on unauthenticated token request
def test_unauth_token():
    response = app.get('/auth/token', expect_errors=True)
    assert str(401) in response.status

# It should return a token on authenticated token request
def test_auth_token():
    os.environ['USER_EMAIL'] = 'info@example.com'
    os.environ['AUTH_DOMAIN'] = 'example.com'
    os.environ['USER_ID'] = 'NOFUCKSGIVEN'
    response = app.get('/auth/token')
    assert str(200) in response.status
    assert response.content_type == 'application/json'
    assert '' in response.json['token']

