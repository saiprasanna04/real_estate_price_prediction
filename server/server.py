from flask import Flask, request, jsonify
import util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        return jsonify({'locations': locations})
    except Exception as e:
        return jsonify({'error': f'Error retrieving locations: {str(e)}'}), 500

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        data = request.form if request.method == 'POST' else request.args
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])

        if total_sqft <= 0 or bhk <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid input values. All inputs must be greater than 0.'}), 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return jsonify({'estimated_price': estimated_price})

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid value type. Ensure all inputs are correct.'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    try:
        print("Starting Python Flask Server for Home Price Prediction...")
        util.load_saved_artifacts()
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask server: {str(e)}")

