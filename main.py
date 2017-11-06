import cherrypy
from rcont import ResetController
from mcont import MovieController
from ucont import UserController
from ratingcont import RatingController
from reccont import RecommendationController
from _movie_database import _movie_database

def start_service():
	# initialize mdb class
	mdb = _movie_database()
	mdb.load_movies('ml-1m/movies.dat')
	mdb.load_users('ml-1m/users.dat')
	mdb.load_ratings('ml-1m/ratings.dat')
	mdb.load_images('ml-1m/images.dat')

	# dispatcher
	dispatcher = cherrypy.dispatch.RoutesDispatcher()

	# controllers
	resetController = ResetController(mdb=mdb)
	movieController = MovieController(mdb=mdb)
	userController = UserController(mdb=mdb)
	ratingController = RatingController(mdb=mdb)
	recommendationController = RecommendationController(mdb=mdb)

	# for /ratings/:movie_id
	dispatcher.connect('ratings_get', '/ratings/:movie_id',
		controller = ratingController,
		action = 'GET', conditions = dict(method=['GET']))

	# for /recommendations/
	dispatcher.connect('full_recommendations_delete', '/recommendations/',
		controller = recommendationController,
		action = 'FULL_DELETE', conditions = dict(method=['DELETE']))

	# for /recommendations/:user_id
	dispatcher.connect('recommendations_get', '/recommendations/:user_id',
		controller = recommendationController,
		action = 'GET', conditions = dict(method=['GET']))

	dispatcher.connect('recommendations_put', '/recommendations/:user_id',
		controller = recommendationController,
		action = 'PUT', conditions = dict(method=['PUT']))

	# for /users/
	dispatcher.connect('full_users_get', '/users/',
		controller = userController,
		action = 'FULL_GET', conditions = dict(method=['GET']))

	dispatcher.connect('full_users_post', '/users/',
		controller = userController,
		action = 'FULL_POST', conditions = dict(method=['POST']))

	dispatcher.connect('full_users_delete', '/users/',
		controller = userController,
		action = 'FULL_DELETE', conditions = dict(method=['DELETE']))

	# for /users/:user_id
	dispatcher.connect('users_get', '/users/:user_id',
		controller = userController,
		action = 'GET', conditions = dict(method=['GET']))

	dispatcher.connect('users_put', '/users/:user_id',
		controller = userController,
		action = 'PUT', conditions = dict(method=['PUT']))

	dispatcher.connect('users_delete', '/users/:user_id',
		controller = userController,
		action = 'DELETE', conditions = dict(method=['DELETE']))

	# for /movies/
	dispatcher.connect('full_movies_get', '/movies/',
		controller = movieController,
		action = 'FULL_GET', conditions = dict(method=['GET']))

	dispatcher.connect('full_movies_post', '/movies/',
		controller = movieController,
		action = 'FULL_POST', conditions = dict(method=['POST']))

	dispatcher.connect('full_movies_delete', '/movies/',
		controller = movieController,
		action = 'FULL_DELETE', conditions = dict(method=['DELETE']))

	# for /movies/:movie_id
	dispatcher.connect('movies_get', '/movies/:movie_id',
		controller = movieController,
		action = 'GET', conditions = dict(method=['GET']))

	dispatcher.connect('movies_put', '/movies/:movie_id',
		controller = movieController,
		action = 'PUT', conditions = dict(method=['PUT']))

	dispatcher.connect('movies_delete', '/movies/:movie_id',
		controller = movieController,
		action = 'DELETE', conditions = dict(method=['DELETE']))

	# for /reset/
	dispatcher.connect('full_reset', '/reset/',
		controller  = resetController,
		action = 'FULL_RESET', conditions = dict(method=['PUT']))

	# for /reset/:movie_id
	dispatcher.connect('reset', '/reset/:movie_id',
		controller = resetController,
		action = 'RESET', conditions = dict(method=['PUT']))

	# configuration for server
	conf = {'global': {'server.socket_host': 'student04.cse.nd.edu',
				'server.socket_port': 51019},
		'/'	: {'request.dispatch': dispatcher}
		}
	
	# start server
	cherrypy.config.update(conf)
	app = cherrypy.tree.mount(None, config=conf)
	cherrypy.quickstart(app)

if __name__ == '__main__':
	start_service()
