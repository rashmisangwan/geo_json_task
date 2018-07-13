from flask import Flask, request
from database_helpers import should_save_data, save_data
import json

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!!'

@app.route('/post_location', methods=['GET', 'POST'])
def postLocationHandler():
	response = {
		"payload": {},
		"status": {
			"code": ''
		}
	}
	if request.method == 'POST':
		_lat = request.values.get('lat')
		_long = request.values.get('long')
		_pincode = request.values.get('pincode')
		_city = request.values.get('city')
		_state = request.values.get('state')

		if not _lat or not _long or not _pincode:
			response['status']['code'] = 'VALIDATION_ERROR'
		else:
			shouldSave = False
			print(response)
			shouldSave, response['payload'] = should_save_data(_pincode, _lat, _long)

			if shouldSave:
				response['payload'] = save_data(_pincode, _city, _state, _lat, _long)
				response['status']['code'] = 'SUCCESS'
			else:
				response['status']['code'] = 'ALREADY_EXISTS'
	else:
		response['payload'] = 'Make a post with required params to save a pincode in Database'
		response['status']['code'] = 'WRONG_API_METHOD'

	return json.dumps(response)

if __name__ == "__main__":
	app.run(debug = True)