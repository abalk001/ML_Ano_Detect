from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('rul_prediction_model.pk')  # Ensure the model is saved as 'rul_prediction_model.pk'

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input JSON data
        print(request.json)
        data = request.get_json()
        
        # Extract features from the input
        features = data['features']
        current_cycle = data.get('current_cycle', None)
        
        # Convert to DataFrame for prediction
        input_data = pd.DataFrame([features])
        
        # Predict RUL
        predicted_rul = model.predict(input_data)[0]
        predicted_failure_cycle = current_cycle + predicted_rul if current_cycle else None
        
        # Return the prediction
        return jsonify({
            'predicted_rul': predicted_rul,
            'predicted_failure_cycle': predicted_failure_cycle
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the server
if __name__ == '__main__':
    app.run(debug=True)