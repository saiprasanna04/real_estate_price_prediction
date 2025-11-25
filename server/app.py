from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

model = None
data_columns = None
locations = None

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global data_columns
    global model
    global locations

    # Load columns
    with open("./artifacts/columns.pkl", "rb") as f:
        data_columns = pickle.load(f)
        # Assuming location names are after some fixed columns, e.g. from index 3 onward
        locations = data_columns[3:]

    # Load model
    with open("./artifacts/home_price_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Loading saved artifacts...done")

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    return jsonify({"locations": locations})

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    if model is None or data_columns is None:
        return jsonify({"error": "Model or data columns not loaded. Please call load_saved_artifacts()"}), 500

    try:
        total_sqft = float(request.form.get('total_sqft', ''))
        bhk = int(request.form.get('bhk', ''))
        bath = int(request.form.get('bath', ''))
        location = request.form.get('location', '')

        # Prepare input vector
        x = np.zeros(len(data_columns))
        x[0] = total_sqft
        x[1] = bath
        x[2] = bhk

        if location.lower() in [loc.lower() for loc in locations]:
            loc_index = [loc.lower() for loc in locations].index(location.lower())
            x[3 + loc_index] = 1
        else:
            return jsonify({"error": f"Location '{location}' not recognized."})

        predicted_price = model.predict([x])[0]
        return jsonify({"estimated_price": round(predicted_price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    load_saved_artifacts()
    app.run(port=5000, debug=True)
