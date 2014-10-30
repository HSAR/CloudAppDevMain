from webtest import TestApp
from main import application

app = TestApp(application)

# This is a test of the JSON responses from the server
def test_json():
    response = app.get('/test/json')
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert 'success' in str(response.json['test'])

# This is a test of requests with URI arguments and parameters.
def test_json_path():
    key = 'test1'
    value = 'test2'
    response = app.get('/test/json/' + key + '?value=' + value)
    assert response.status == '200 OK'
    assert response.content_type == 'application/json'
    assert value in str(response.json[key])
