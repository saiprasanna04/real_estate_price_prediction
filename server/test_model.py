import util

def test_estimation():
    # Load artifacts
    util.load_saved_artifacts()

    # Show available locations
    locations = util.get_location_names()
    if not locations:
        print("❌ No locations found. Check if columns.json loaded properly.")
        return

    print(f"✅ Locations loaded: {len(locations)} (e.g., {locations[:5]})")

    # Pick a known location and run a prediction
    sample_location = locations[0]
    sqft = 1000
    bhk = 2
    bath = 2

    estimated_price = util.get_estimated_price(sample_location, sqft, bhk, bath)
    
    if isinstance(estimated_price, str) and "Error" in estimated_price:
        print(f"❌ Estimation failed: {estimated_price}")
    else:
        print(f"✅ Estimated price for {sample_location}: ₹{estimated_price} lakhs")

if __name__ == "__main__":
    test_estimation()
