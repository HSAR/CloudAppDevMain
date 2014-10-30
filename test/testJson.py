from webtest import TestApp
from main import application

import json

app = TestApp(application)

# This is a test of the JSON library
def test_index():
    response = app.get('/test/json')
    jsonData = json.load(response)
    assert 'success' in str(jsonData[test])
