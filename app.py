from flask import Flask, request, jsonify, send_from_directory
import pickle
import numpy as np
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Load model
MODEL_PATH = 'model.pkl'
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.json
        
        # Ensure the order matches what the model expects
        features = [
            data.get('age', 0),
            data.get('sex', 0),
            data.get('cp', 0),
            data.get('trestbps', 0),
            data.get('chol', 0),
            data.get('fbs', 0),
            data.get('restecg', 0),
            data.get('thalach', 0),
            data.get('exang', 0),
            data.get('oldpeak', 0),
            data.get('slope', 0),
            data.get('ca', 0),
            data.get('thal', 0)
        ]
        
        # Convert to numpy array and reshape
        features_array = np.array([features])
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0][1] # Probability of class 1 (High Risk)
        
        # If model outputs 0 but we need to format it, we return probability of the predicted class
        if prediction == 0:
            probability = model.predict_proba(features_array)[0][0]
            
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability)
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
