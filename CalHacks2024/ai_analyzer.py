import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def load_data(file_path):
    """Load financial data from CSV file."""
    data = pd.read_csv(file_path)
    # Convert numeric columns to float
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    # Drop rows with NaN values
    data = data.dropna()
    return data

def preprocess_data(data):
    """Preprocess the data for analysis."""
    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'
    
    X = data[features]
    y = data[target]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """Train a Random Forest model."""
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and return RMSE."""
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    return rmse

def analyze_financials(file_path):
    """Main function to analyze financial data."""
    data = load_data(file_path)
    X_train, X_test, y_train, y_test = preprocess_data(data)
    model = train_model(X_train, y_train)
