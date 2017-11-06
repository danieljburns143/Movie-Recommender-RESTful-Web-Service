import cherrypy
import re, json

class RatingController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def GET(self, movie_id):
		output = {'result': 'success'}
		movie_id = int(movie_id)
		try:
			output['rating'] = self.mdb.get_rating(movie_id)
			output['movie_id'] = movie_id
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not retrieve the average rating for a movie'
		return json.dumps(output)
