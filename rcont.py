import cherrypy
import re, json

class ResetController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def FULL_RESET(self):
		output = {'result': 'success'}
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			self.mdb.load_movies('ml-1m/movies.dat')
			self.mdb.load_users('ml-1m/users.dat')
			self.mdb.load_ratings('ml-1m/ratings.dat')
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not recreate database from .dat files'
		return json.dumps(output)
	
	def RESET(self, movie_id):
		output = {'result': 'success'}
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)		
			self.mdb.reset_one_movie('ml-1m/movies.dat', movie_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not reset one movie from .dat files'
		return json.dumps(output)
