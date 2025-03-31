import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class FashionClassifier:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = [
            '1.How often do you shop for new clothes?',
            '2.Where do you typically shop for clothes?',
            '3.What influences your clothing purchases the most?',
            '4.How would you describe your go-to daily outfit?',
            '5.If you had to choose, would you prefer timeless pieces or trendy items?'
        ]
        
    def load_data(self, csv_path):
        """Load and preprocess the data from CSV file"""
        df = pd.read_csv(csv_path)
        
        # Clean and preprocess the data
        df = df.dropna(subset=self.feature_columns)
        
        # Encode categorical variables
        for column in self.feature_columns:
            if df[column].dtype == 'object':
                self.label_encoders[column] = LabelEncoder()
                df[column] = self.label_encoders[column].fit_transform(df[column])
        
        return df
    
    def train_model(self, csv_path):
        """Train the Random Forest model"""
        # Load and preprocess the data
        df = self.load_data(csv_path)
        
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['Fashion Identity']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Save the model and label encoders
        self.save_model()
        
        return self.model.score(X_test, y_test)
    
    def save_model(self):
        """Save the trained model and label encoders"""
        if not os.path.exists('models'):
            os.makedirs('models')
        
        joblib.dump(self.model, 'models/fashion_model.joblib')
        joblib.dump(self.label_encoders, 'models/label_encoders.joblib')
    
    def load_model(self):
        """Load the trained model and label encoders"""
        if os.path.exists('models/fashion_model.joblib'):
            self.model = joblib.load('models/fashion_model.joblib')
            self.label_encoders = joblib.load('models/label_encoders.joblib')
            return True
        return False
    
    def predict(self, user_data):
        """Predict fashion identity for new user data"""
        if self.model is None:
            if not self.load_model():
                raise ValueError("Model not trained. Please train the model first.")
        
        # Convert user data to DataFrame
        df = pd.DataFrame([user_data])
        
        # Encode categorical variables
        for column in self.feature_columns:
            if column in self.label_encoders:
                df[column] = self.label_encoders[column].transform([df[column].iloc[0]])
        
        # Make prediction
        X = df[self.feature_columns]
        prediction = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        return {
            'prediction': prediction[0],
            'probabilities': probabilities[0].tolist()
        }
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if self.model is None:
            if not self.load_model():
                raise ValueError("Model not trained. Please train the model first.")
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_columns, importance))
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)) 