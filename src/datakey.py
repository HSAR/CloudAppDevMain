import webapp2

from google.appengine.ext import ndb


root_key = ndb.Key('Root', 'root')

class testModel(ndb.Model):
    user_id = ndb.StringProperty()

class KeyPutHandler(webapp2.RequestHandler):

    def get(self):
		for i in range(1000):
			tm = testModel(parent=root_key, id=str(i), user_id='Bob')
			tm.put()
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Put')

class KeyGetHandler(webapp2.RequestHandler):

	def get(self):
		for i in range(1000):
			tkey = ndb.Key('testModel', str(i), parent=root_key)
			tm = tkey.get()
			print tm
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(tm)
		
application = webapp2.WSGIApplication([
                                          webapp2.Route(r'/test/datakeyput', handler=KeyPutHandler, name='keyputhandler'),
										  webapp2.Route(r'/test/datakeyget', handler=KeyGetHandler, name='keygethandler'),
                                      ], debug=True)