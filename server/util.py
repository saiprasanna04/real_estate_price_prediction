import pickle
import json
import numpy as np
import pandas as pd
import difflib  # For fuzzy matching

# Global variables to store the model and metadata
__locations = None
__data_columns = None
__model = None


def load_saved_artifacts():
    """
    Load the saved model and data columns from disk.
    """
    global __data_columns
    global __locations
    global __model

    print("Loading saved artifacts...")

    try:
        with open("./artifacts/columns.json", "r") as f:
            json_data = json.load(f)
            __data_columns = json_data['data_columns']
            __locations = __data_columns[3:]  # Skip sqft, bath, bhk

        with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)

        print("Artifacts loaded successfully!")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from columns.json.")
    except pickle.UnpicklingError:
        print("Error: Failed to load the model from pickle file.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def get_estimated_price(location, sqft, bhk, bath):
    """
    Predict the estimated home price for a given location and configuration.
    """
    if __model is None or __data_columns is None:
        raise Exception("Model or data columns not loaded. Please call load_saved_artifacts().")

    try:
        # Match location case-insensitively and ignoring extra spaces
        location_cleaned = location.strip().lower()
        loc_index = next(
            (i for i, col in enumerate(__data_columns) if col.strip().lower() == location_cleaned),
            -1
        )

        if loc_index == -1:
            # Fuzzy match for possible close locations
            suggestions = difflib.get_close_matches(
                location_cleaned, [loc.lower() for loc in __locations], n=3, cutoff=0.6
            )
            suggestion_msg = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            raise ValueError(f"Location '{location}' not found in model data.{suggestion_msg}")

        # Prepare input vector
        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        x[loc_index] = 1

        # Predict using pandas DataFrame to avoid sklearn warnings
        x_df = pd.DataFrame([x], columns=__data_columns)
        return round(__model.predict(x_df)[0], 2)

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")


def get_location_names():
    """
    Return the list of available location names.
    """
    if __locations is None:
        raise Exception("Locations not loaded. Call load_saved_artifacts() first.")
    return __locations


def get_data_columns():
    """
    Return the full list of data columns (features).
    """
    if __data_columns is None:
        raise Exception("Data columns not loaded. Call load_saved_artifacts() first.")
    return __data_columns


if __name__ == '__main__':
    load_saved_artifacts()

    print("Location Names:", get_location_names())

    try:
        print("Prediction (1st Phase JP Nagar, 3BHK):", get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
        print("Prediction (Whitefield, 2BHK):", get_estimated_price('Whitefield', 1200, 2, 2))
        print("Prediction (Unknown Location):", get_estimated_price('Kalhalli', 1000, 2, 2))
    except Exception as e:
        print(e)
