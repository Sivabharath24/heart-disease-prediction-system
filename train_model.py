import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def generate_mock_dataset(n_samples=1000):
    np.random.seed(42)
    # Generate somewhat realistic mock data based on UCI Heart Disease dataset ranges
    data = {
        'age': np.random.randint(29, 78, n_samples),
        'sex': np.random.choice([0, 1], n_samples),
        'cp': np.random.choice([0, 1, 2, 3], n_samples),
        'trestbps': np.random.randint(94, 201, n_samples),
        'chol': np.random.randint(126, 565, n_samples),
        'fbs': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'restecg': np.random.choice([0, 1, 2], n_samples),
        'thalach': np.random.randint(71, 203, n_samples),
        'exang': np.random.choice([0, 1], n_samples),
        'oldpeak': np.round(np.random.uniform(0, 6.2, n_samples), 1),
        'slope': np.random.choice([0, 1, 2], n_samples),
        'ca': np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
        'thal': np.random.choice([0, 1, 2, 3], n_samples, p=[0.05, 0.35, 0.4, 0.2])
    }
    df = pd.DataFrame(data)
    
    # Create target (1: high risk, 0: low risk)
    # Simple logic to make the model learnable
    risk_score = (df['age'] > 50).astype(int) + df['cp'] + (df['thalach'] < 140).astype(int) + df['exang']
    df['target'] = (risk_score >= 2).astype(int)
    
    return df

def train_and_save():
    print("Generating training data...")
    df = generate_mock_dataset()
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model accuracy on test set: {score:.4f}")
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved to model.pkl")

if __name__ == '__main__':
    train_and_save()
