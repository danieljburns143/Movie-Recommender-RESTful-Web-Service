import cherrypy
import re, json

class MovieController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def FULL_GET(self):
		output = {'result': 'success'}
		output['movies'] = []
		try:
			for key_value in self.mdb.movies.items():
				JSONString = self.GET(key_value[0])
				JSONString = json.loads(JSONString)
				output['movies'].append(JSONString)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not list all available movies'
		return json.dumps(output)
	
	def FULL_POST(self):
		output = {'result': 'success'}
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			new_movie_id = max(self.mdb.get_movies()) + 1
			listParameter = [the_body['title'], the_body['genres']]
			self.mdb.set_movie(new_movie_id, listParameter)
			output['id'] = new_movie_id
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not add a new movie'
		return json.dumps(output)

	def FULL_DELETE(self):
		output = {'result': 'success'}
		try:
			self.mdb.movies.clear()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not clear movies database'
		return json.dumps(output)

	def GET(self, movie_id):
		output = {'result': 'success'}
		movie_id = int(movie_id)
		try:
			output['title'] = self.mdb.get_movie(movie_id)[0]
			output['genres'] = self.mdb.get_movie(movie_id)[1]
			output['id'] = movie_id
			if movie_id in self.mdb.images:
				output['img'] = self.mdb.images[movie_id][1]
				if output['img'] == '':
					output['img'] = '/no_img_path.jpg'
			else:
				output['img'] = '/no_img_path.jpg'
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not retrieve movie title and description'
		return json.dumps(output)
	
	def PUT(self, movie_id):
		output = {'result': 'success'}
		movie_id = int(movie_id)
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			listParameter = [the_body['title'], the_body['genres']]
			self.mdb.set_movie(movie_id, listParameter)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not replace (or create) movie'
		return json.dumps(output)

	def DELETE(self, movie_id):
		output = {'result': 'success'}
		movie_id = int(movie_id)
		try:
			self.mdb.delete_movie(movie_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'delete the movie'
		return json.dumps(output)
