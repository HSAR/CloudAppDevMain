from webtest import TestApp
from main import application

app = TestApp(application)

# This is a test of the hello world default application
def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)
	
# This is a test of the editor handler response
def test_editor_handler():
	response = app.get('/editor')
	assert '<div class="canvas col-md-10">' in str(response)
	