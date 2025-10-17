import requests

def get_prediction(server_url, features, current_cycle=None):
    payload = {
        'features': features,
        'current_cycle': current_cycle
    }

    response = requests.post(f"{server_url}/predict", json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")




if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    features = {
		"sensor_2": 0.412651,
		"sensor_3": 0.221932,
		"sensor_4": 0.281229,
		"sensor_7": 0.735910,
		"sensor_11": 0.226190,
		"sensor_12": 0.660981,
		"cycle": 31.000000,
        "setting_1": 0.465517,
		"setting_2": 0.833333,
		"setting_3": 0.000000
	}
    current_cycle = 31.000

    try:
        prediction = get_prediction(server_url, features, current_cycle)
        print("Prediction:", prediction)
    except Exception as e:
        print("Error:", e)