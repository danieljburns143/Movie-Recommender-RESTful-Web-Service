import cherrypy
import re, json

class UserController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def FULL_GET(self):
		output = {'result': 'success'}
		output['users'] = []
		try:
			for key_value in self.mdb.users.items():
				JSONString = self.GET(key_value[0])
				JSONString = json.loads(JSONString)
				output['users'].append(JSONString)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not list all users'
		return json.dumps(output)

	def FULL_POST(self):
		output = {'result': 'success'}
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			new_user_id = max(self.mdb.get_users()) + 1
			listParameter = [the_body['gender'], int(the_body['age']), \
				int(the_body['occupation']), the_body['zipcode']]
			self.mdb.set_user(new_user_id, listParameter)
			output['id'] = new_user_id
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not add a new user'
		return json.dumps(output)

	def FULL_DELETE(self):
		output = {'result': 'success'}
		try:
			self.mdb.users.clear()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not clear users database'
		return json.dumps(output)

	def GET(self, user_id):
		output = {'result': 'success'}
		user_id = int(user_id)
		try:
			tempList = self.mdb.get_user(user_id)
			output['gender'] = tempList[0]
			output['age'] = tempList[1]
			output['occupation'] = tempList[2]
			output['zipcode'] = tempList[3]
			output['id'] = user_id
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not retrieve user\'s profile information'
		return json.dumps(output)

	def PUT(self, user_id):
		output = {'result': 'success'}
		user_id = int(user_id)
		the_body = cherrypy.request.body.read().decode()
		try:
			the_body = json.loads(the_body)
			listParameter = [the_body['gender'], int(the_body['age']), \
				int(the_body['occupation']), the_body['zipcode']]
			self.mdb.set_user(user_id, listParameter)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not replace (or create) user'
		return json.dumps(output)

	def DELETE(self, user_id):
		output = {'result': 'success'}
		user_id = int(user_id)
		try:
			self.mdb.delete_user(user_id)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = 'could not delete the user'
		return json.dumps(output)
