import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

agents = Blueprint('agents', 'agents')

@agents.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['email'].lower()

	try:
		models.Agent.get(models.Agent.email == payload['email'])
		return jsonify(data={}, status={'code': 401, 'message' : 'An agent with that email already exists. Try again!'}), 401

	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		agent = models.Agent.create(**payload)

		login_user(agent)

		agent_dict = model_to_dict(agent)

		print(agent_dict)
		del agent_dict['password']

		return jsonify(data=agent_dict, status={'code': 201, 'message': 'Successfully registered! {}'.format(agent_dict['email'])}), 201


@agents.route('/login', methods=['POST'])
def login():
	payload = request.get_json()

	try:
		agent = models.Agent.get(models.Agent.email == payload['email'])
		agent_dict = model_to_dict(agent)
		if(check_password_hash(agent_dict['password'], payload['password'])):
			login_user(agent)

			del agent_dict['password']
			

			return jsonify(data=agent_dict, status={'code': 200, 'message': 'Successfully logged in {}'.format(agent_dict['email'])}), 200

		else:
			print('password is not correct')
			return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401

	except models.DoesNotExist:
		print('email not found')
		return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401

@agents.route('/logged_in', methods=['GET'])
def get_logged_in_agent():
	if not current_user.is_authenticated:
		return jsonify(data={}, status={
			'code': 401,
			'message': 'No user is currently logged in.'
			}), 401
	else:
		agent_dict= model_to_dict(current_user)
		agent_dict.pop('password')
		return jsonify(data=user_dict, status={
			'code': 200,
			'message': 'Current user is {}'.format(user_dict['email'])
			}), 200

@agents.route('/logout', methods=['GET'])
def logout():
	email = model_to_dict(current_user)['email']
	logout_user()

	return jsonify(data={}, status={
		'code': 200,
		'message': 'Successfully logged out {}'.format(email)
		})










