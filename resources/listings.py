import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

listings = Blueprint('listings', 'listings')


# Index Route
@listings.route('/', methods=['GET'])
def get_all_listings():
	try: 
		query = models.Listing.select().where(models.Listing.agent_id == current_user.id)
		listings = [model_to_dict(listings) for listings in query]
		print(listings)
		
		[ listing["agent_id"].pop("password") for listing in listings]
		

		return jsonify(data=listings, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401

#Create Route
@listings.route('/', methods=['POST'])
def create_listing():
	payload = request.get_json()
	print(type(payload), 'payload')
	listings = models.Listing.create(**payload,
		agent_id=current_user.id)
	print(listings.__dict__)
	print(dir(listings))

	print(model_to_dict(listings), 'model to dict')
	listings_dict = model_to_dict(listings)
	return jsonify(data=listings_dict, status={'code': 201, 'message': 'Success'})


# # Show Route
# @listings.route('/<id>', methods=['GET'])
# def get_one_listing(id):
# 	print(id)
# 	listings = models.Listing.get_by_id(id)

# 	return jsonify(data=model_to_dict(listings), status={'code': 201, 'message': 'Success'})

#Update Route
@listings.route('/<id>', methods=['PUT'])
def update_listings(id):
	payload = request.get_json()
	print(payload)
	query = models.Listing.update(**payload).where(models.Listing.id == id)
	query.execute()
	listings = models.Listing.get_by_id(id)

	listings_dict = model_to_dict(listings)
	return jsonify(data=listings_dict, status={'code': 200, 'message':'Resource updated successfully!'})

#Delete Route 

@listings.route('/<id>', methods=['Delete'])
def delete_listings(id):
	query = models.Listing.delete().where(models.Listing.id == id)
	query.execute()

	return jsonify(data='Resource has successfully been deleted', status={
		'code': 200, 'message': 'Resource has been deleted successfully'
		})






