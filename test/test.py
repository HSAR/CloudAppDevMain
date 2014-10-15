from webtest import TestApp
from main import application

app = TestApp(application)

# This is a test of the hello world default application
def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)