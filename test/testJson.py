from webtest import TestApp
from main import application

app = TestApp(application)

# This is a test of the JSON responses from the server
def test_index():
    response = app.get('/test/json')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert 'success' in str(response.json['test'])
