from webtest import TestApp
from main import application

app = TestApp(application)

# Expect 404 template page as appropriate
def test_index():
    response = app.get('/ifthisiseverathingtherewillbetrouble')
    assert 'Error 404' in str(response)

# Expect 500 template page as appropriate
    response = app.get('/timeout')
    assert 'Error 500' in str(response)
