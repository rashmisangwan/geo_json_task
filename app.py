from flask import Flask, request
from database_helpers import should_save_data, save_data, get_nearby_data_default, get_nearby_data_self
import json

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!!'

@app.route('/post_location', methods=['POST'])
def postLocationHandler():
	nearby_offset_distance = 5000 # in meters
	response = {
		"payload": {},
		"status": {
			"code": ''
		}
	}
	if request.method == 'POST':
		_lat = request.form.get('lat')
		_long = request.form.get('long')
		_pincode = request.form.get('pincode')
		_city = request.form.get('city')
		_state = request.form.get('state')

		if not _lat or not _long or not _pincode:
			response['status']['code'] = 'VALIDATION_ERROR :: pincode, latitude and longitude are compulsary'
		else:
			shouldSave = False
			shouldSave, response['payload'] = should_save_data(_pincode, _lat, _long, nearby_offset_distance)

			if shouldSave:
				response['status']['code'] = save_data(_pincode, _city, _state, _lat, _long)
			else:
				response['status']['code'] = 'ALREADY_EXISTS'
	# else:
	# 	response['payload'] = 'Make a post with required params - Pincode, Latitude and Longitude'
	# 	response['status']['code'] = 'WRONG_API_METHOD'

	return json.dumps(response)

@app.route('/get_using_postgres', methods=['GET'])
def getUsingPostgresHandler():
	response = {
		"payload": {},
		"status": {
			"code": ''
		}
	}
	if request.method == 'GET':
		try:
			_lat = float(request.args.get('lat'))
			_long = float(request.args.get('long'))
			_distance = float(request.args.get('distance'))

			if not _lat or not _long or not _distance:
				response['status']['code'] = 'VALIDATION_ERROR :: latitude, longitude and Distance are compulsary'
			else:
				response['status']['code'], response["payload"] = get_nearby_data_default(_lat, _long, _distance)

		except:
			response['status']['code'] = 'INCORRECT_DATA'

	return json.dumps(response)


@app.route('/get_using_self', methods=['GET'])
def getUsingSelfHandler():
	response = {
		"payload": {},
		"status": {
			"code": ''
		}
	}
	if request.method == 'GET':
		_lat = request.args.get('lat')
		_long = request.args.get('long')
		_distance = request.args.get('distance')

		if not _lat or not _long or not _distance:
			response['status']['code'] = 'VALIDATION_ERROR :: latitude, longitude and Distance are compulsary'
		else:
			response['status']['code'], response["payload"] = get_nearby_data_self(_lat, _long, _distance)
	# else:
	# 	response['payload'] = 'Make a GET request with required params - Latitude, Longitude and Distance'
	# 	response['status']['code'] = 'WRONG_API_METHOD'

	return json.dumps(response)


if __name__ == "__main__":
	app.run(debug = True)