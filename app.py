from flask import Flask, request
from database_helpers import should_save_data, save_data
import json

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!!'

@app.route('/post_location', methods=['GET', 'POST'])
def postLocationHandler():
	payload = None
	if request.method == 'POST':
		_lat = request.values.get('lat')
		_long = request.values.get('long')
		_pincode = request.values.get('pincode')
		_city = request.values.get('city')
		_state = request.values.get('state')

		shouldSave = False
		payload = {}

		shouldSave, payload = should_save_data(_pincode, _lat, _long)

	else:
		payload = 'Make a post with required params to save a pincode in Database'

	return json.dumps({'payload': payload})

if __name__ == "__main__":
	app.run(debug = True)