import pandas as pd
import numpy as np
from fashion_classifier import FashionClassifier
import os

def create_sample_data():
    """Create a sample dataset for training"""
    # Sample data with different fashion identities
    data = {
        '1.How often do you shop for new clothes?': ['Weekly', 'Monthly', 'Quarterly', 'Weekly', 'Monthly', 'Quarterly', 'Weekly', 'Monthly'],
        '2.Where do you typically shop for clothes?': ['Fast Fashion', 'Department Stores', 'Luxury Boutiques', 'Fast Fashion', 'Department Stores', 'Luxury Boutiques', 'Fast Fashion', 'Department Stores'],
        '3.What influences your clothing purchases the most?': ['Trends', 'Price', 'Quality', 'Trends', 'Price', 'Quality', 'Trends', 'Price'],
        '4.How would you describe your go-to daily outfit?': ['Trendy', 'Business Casual', 'Formal', 'Trendy', 'Business Casual', 'Formal', 'Trendy', 'Business Casual'],
        '5.If you had to choose, would you prefer timeless pieces or trendy items?': ['Trendy', 'Mix', 'Timeless', 'Trendy', 'Mix', 'Timeless', 'Trendy', 'Mix'],
        'Fashion Identity': ['Trendsetter', 'Budget Conscious', 'Luxury', 'Trendsetter', 'Budget Conscious', 'Luxury', 'Trendsetter', 'Budget Conscious']
    }
    
    return pd.DataFrame(data)

def main():
    # Create sample data
    df = create_sample_data()
    
    # Save the data to CSV
    if not os.path.exists('data'):
        os.makedirs('data')
    df.to_csv('data/fashion_data.csv', index=False)
    
    # Initialize classifier
    classifier = FashionClassifier()
    
    # Train the model
    accuracy = classifier.train_model('data/fashion_data.csv')
    print(f"Model trained with accuracy: {accuracy:.2f}")
    
    # Test prediction
    test_data = {
        '1.How often do you shop for new clothes?': 'Weekly',
        '2.Where do you typically shop for clothes?': 'Fast Fashion',
        '3.What influences your clothing purchases the most?': 'Trends',
        '4.How would you describe your go-to daily outfit?': 'Trendy',
        '5.If you had to choose, would you prefer timeless pieces or trendy items?': 'Trendy'
    }
    
    prediction = classifier.predict(test_data)
    print(f"\nTest prediction: {prediction['prediction']}")
    print(f"Probabilities: {prediction['probabilities']}")
    
    # Get feature importance
    importance = classifier.get_feature_importance()
    print("\nFeature Importance:")
    for feature, imp in importance.items():
        print(f"{feature}: {imp:.4f}")

if __name__ == "__main__":
    main() 