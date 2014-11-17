from webtest import TestApp
from main import application

app = TestApp(application)

# Expect 404 template page as appropriate
def test_404():
    response = app.get('/ifthisiseverathingtherewillbetrouble', status=404)
    assert str(404) in response.status

# Expect 500 template page as appropriate
def test_500():
    response = app.get('/fivehundred', status=500)
    assert str(500) in response.status
