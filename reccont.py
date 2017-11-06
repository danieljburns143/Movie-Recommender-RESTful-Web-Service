import cherrypy
import re, json

class RecommendationController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def FULL_DELETE(self):
		output = {'result': 'success'}
		try:
			self.mdb.delete_all_ratings()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not clear votes database'
		return json.dumps(output)

	def GET(self, user_id):
		output = {'result': 'success'}
		user_id = int(user_id)
		try:
			output['movie_id'] = self.mdb.get_highest_rated_unvoted_movie(user_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not retrieve movie recommendation for user'
		return json.dumps(output)

	def PUT(self, user_id):
		output = {'result': 'success'}
		user_id = int(user_id)
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			self.mdb.set_user_movie_rating(user_id, int(the_body['movie_id']), \
				int(the_body['rating']))
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not add a new vote for given movie'
		return json.dumps(output)
