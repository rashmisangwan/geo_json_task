from flask import Flask, request
from database_helpers import should_save_data, save_data, get_nearby_data_default, get_nearby_data_self, get_containing_area
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
	response = {
		"API_INFORMATION": {
			"post_location": {
				"method": "POST",
				"data": [
					{
						"lat": "float",
						"long": "float",
						"pincode": "string",
						"city": "string",
						"state": "string",
					}
				]
			},
			"get_using_postgres": {
				"method": "GET",
				"data": [
					{
						"lat": "float",
						"long": "float",
						"distance": "float",
					}
				]
			},
			"get_using_self": {
				"method": "GET",
				"data": [
					{
						"lat": "float",
						"long": "float",
						"distance": "float",
					}
				]
			},
			"get_containing_area": {
				"method": "GET",
				"data": [
					{
						"lat": "float",
						"long": "float"
					}
				]
			}
		}
	}

	return jsonify(response)

@app.route('/post_location', methods=['POST'])
def postLocationHandler():
	nearby_offset_distance = 5 # in km
	response = {
		"payload": {},
		"status": {
			"code": ''
		}
	}
	if request.method == 'POST':
		try:
			_lat = float(request.form.get('lat'))
			_long = float(request.form.get('long'))
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
		except:
			response['status']['code'] = 'INCORRECT_DATA'

	return jsonify(response)

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
			_distance_meters = _distance *  1000
			if not _lat or not _long or not _distance:
				response['status']['code'] = 'VALIDATION_ERROR :: latitude, longitude and Distance are compulsary'
			else:
				response['status']['code'], response["payload"] = get_nearby_data_default(_lat, _long, _distance_meters)

		except:
			response['status']['code'] = 'INCORRECT_DATA'

	return jsonify(response)


@app.route('/get_using_self', methods=['GET'])
def getUsingSelfHandler():
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
				response['status']['code'], response["payload"] = get_nearby_data_self(_lat, _long, _distance)

		except:
			response['status']['code'] = 'INCORRECT_DATA'

	return jsonify(response)

@app.route('/get_containing_area', methods=['GET'])
def getContainingAreaHandler():
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

			if not _lat or not _long:
				response['status']['code'] = 'VALIDATION_ERROR :: latitude and longitude are compulsary'
			else:
				response['status']['code'], response["payload"] = get_containing_area(_lat, _long)

		except:
			response['status']['code'] = 'INCORRECT_DATA'

	return jsonify(response)




if __name__ == "__main__":
	app.run(debug = True)