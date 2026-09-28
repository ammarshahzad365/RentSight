import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    """Preprocess listing data for model training."""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def fit_transform(self, df, target_col='occ_rate'):
        """Fit preprocessor and transform data."""
        df = df.copy()
        
        # Drop ID column (not useful for prediction)
        if 'id' in df.columns:
            df = df.drop('id', axis=1)
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Encode categorical variables
        categorical_cols = ['listing_type', 'room_type']
        for col in categorical_cols:
            if col in df.columns:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        
        # Separate features and target
        if target_col in df.columns:
            X = df.drop(target_col, axis=1)
            y = df[target_col]
        else:
            X = df
            y = None
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        return X_scaled, y
    
    def transform(self, df):
        """Transform new data using fitted preprocessor."""
        df = df.copy()
        
        # Drop ID column
        if 'id' in df.columns:
            df = df.drop('id', axis=1)
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Encode categorical variables
        for col, encoder in self.label_encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col].astype(str))
        
        # Drop target if present
        if 'occ_rate' in df.columns:
            df = df.drop('occ_rate', axis=1)
        
        # Scale features
        X_scaled = self.scaler.transform(df[self.feature_names])
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        return X_scaled
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset."""
        # Fill missing numerical values with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill missing categorical values with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        return df

def create_train_test_split(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('listings_data.csv')
    
    # Preprocess
    preprocessor = DataPreprocessor()
    X, y = preprocessor.fit_transform(df, target_col='occ_rate')
    
    # Create train/test split
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    print(f"\nFeatures: {preprocessor.feature_names}")
    print(f"\nTraining features shape: {X_train.shape}")
    print(f"Testing features shape: {X_test.shape}")
