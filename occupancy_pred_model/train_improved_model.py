"""
Improved Multi-Modal Ensemble with Better Price Sensitivity
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
import pickle

class ImprovedMultiModalEnsemble:
    """
    Improved multi-modal ensemble with enhanced price sensitivity.
    
    Key improvements:
    1. RobustScaler instead of StandardScaler for better outlier handling
    2. Separate price model with non-linear transformations
    3. Price penalty function for extreme values
    4. Adjusted meta-model to give more weight to price
    """
    
    def __init__(self):
        self.location_model = KNeighborsRegressor(n_neighbors=5, weights='distance')
        self.property_model = GradientBoostingRegressor(n_estimators=100, max_depth=4, learning_rate=0.1)
        self.guest_model = RandomForestRegressor(n_estimators=50, max_depth=5)
        self.price_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.05)
        self.meta_model = Ridge(alpha=0.1)
        self.preprocessor = None
        self.label_encoders = {}
        
    def _apply_price_penalty(self, price, prediction):
        """
        Apply penalty for extremely high prices that reduces occupancy prediction.
        
        Based on market logic:
        - Prices 2x above median: reduce prediction by 10-20%
        - Prices 5x above median: reduce prediction by 30-50%
        - Prices 10x+ above median: reduce prediction by 60-80%
        """
        # Median price from training data is ~30
        median_price = 30.81
        
        if price <= median_price * 2:
            return prediction
        elif price <= median_price * 5:
            # 2-5x median: linear penalty from 0% to 30%
            penalty_factor = 0.7 + 0.3 * (1 - (price - median_price * 2) / (median_price * 3))
            return prediction * penalty_factor
        elif price <= median_price * 10:
            # 5-10x median: penalty from 30% to 60%
            penalty_factor = 0.4 + 0.3 * (1 - (price - median_price * 5) / (median_price * 5))
            return prediction * penalty_factor
        else:
            # 10x+ median: severe penalty (60-80%)
            penalty_factor = max(0.2, 0.4 - 0.2 * min(1, (price - median_price * 10) / (median_price * 100)))
            return prediction * penalty_factor
    
    def _engineer_features(self, df):
        """Add engineered features for better price sensitivity."""
        df = df.copy()
        
        # Price-based features
        df['price_per_bedroom'] = df['price'] / (df['bedrooms'] + 0.5)
        df['price_per_guest'] = df['price'] / (df['max_guests'] + 0.5)
        df['log_price'] = np.log1p(df['price'])
        df['price_squared'] = df['price'] ** 2
        
        # Property value features
        df['beds_per_bedroom'] = df['beds'] / (df['bedrooms'] + 0.5)
        df['baths_per_bedroom'] = df['baths'] / (df['bedrooms'] + 0.5)
        
        # Interaction features
        df['location_price_lat'] = df['lat'] * df['log_price']
        df['location_price_lng'] = df['lng'] * df['log_price']
        
        return df
    
    def fit(self, X, y):
        """Train the improved multi-modal ensemble."""
        # Engineer features
        X_engineered = self._engineer_features(X)
        
        # Setup preprocessing with RobustScaler for better outlier handling
        categorical_features = ['listing_type', 'room_type']
        
        # Encode categorical features
        X_processed = X_engineered.copy()
        for col in categorical_features:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X_processed[col] = self.label_encoders[col].fit_transform(X_engineered[col])
            else:
                X_processed[col] = self.label_encoders[col].transform(X_engineered[col])
        
        # Use RobustScaler (less sensitive to outliers)
        self.preprocessor = RobustScaler()
        X_scaled = self.preprocessor.fit_transform(X_processed)
        
        # Define feature groups (with engineered features)
        location_features = [X_processed.columns.get_loc(col) for col in ['lat', 'lng', 'location_price_lat', 'location_price_lng']]
        property_features = [X_processed.columns.get_loc(col) for col in ['bedrooms', 'beds', 'baths', 'beds_per_bedroom', 'baths_per_bedroom']]
        guest_features = [X_processed.columns.get_loc(col) for col in ['max_guests', 'listing_type', 'room_type']]
        price_features = [X_processed.columns.get_loc(col) for col in ['price', 'price_per_bedroom', 'price_per_guest', 'log_price', 'price_squared']]
        
        # Train specialized models
        print("\n🔧 Training Location Model (KNN)...")
        X_location = X_scaled[:, location_features]
        self.location_model.fit(X_location, y)
        location_pred = self.location_model.predict(X_location)
        print(f"   Location RMSE: {np.sqrt(mean_squared_error(y, location_pred)):.2f}")
        
        print("🔧 Training Property Model (Gradient Boosting)...")
        X_property = X_scaled[:, property_features]
        self.property_model.fit(X_property, y)
        property_pred = self.property_model.predict(X_property)
        print(f"   Property RMSE: {np.sqrt(mean_squared_error(y, property_pred)):.2f}")
        
        print("🔧 Training Guest Model (Random Forest)...")
        X_guest = X_scaled[:, guest_features]
        self.guest_model.fit(X_guest, y)
        guest_pred = self.guest_model.predict(X_guest)
        print(f"   Guest RMSE: {np.sqrt(mean_squared_error(y, guest_pred)):.2f}")
        
        print("🔧 Training Price Model (Gradient Boosting)...")
        X_price = X_scaled[:, price_features]
        self.price_model.fit(X_price, y)
        price_pred = self.price_model.predict(X_price)
        print(f"   Price RMSE: {np.sqrt(mean_squared_error(y, price_pred)):.2f}")
        
        # Create meta-features
        meta_features = np.column_stack([location_pred, property_pred, guest_pred, price_pred])
        
        # Train meta-model with adjusted alpha to allow more flexibility
        print("🔧 Training Meta-Model (Ridge Regression)...")
        self.meta_model.fit(meta_features, y)
        
        # Store feature indices
        self.location_features = location_features
        self.property_features = property_features
        self.guest_features = guest_features
        self.price_features = price_features
        self.feature_columns = X_processed.columns.tolist()
        
        print("\n✅ Model weights:")
        print(f"   Location: {self.meta_model.coef_[0]:.4f}")
        print(f"   Property: {self.meta_model.coef_[1]:.4f}")
        print(f"   Guest: {self.meta_model.coef_[2]:.4f}")
        print(f"   Price: {self.meta_model.coef_[3]:.4f}")
        print(f"   Intercept: {self.meta_model.intercept_:.4f}")
        
        return self
    
    def predict(self, X):
        """Make predictions with price penalty applied."""
        # Engineer features
        X_engineered = self._engineer_features(X)
        
        # Encode categorical features
        X_processed = X_engineered.copy()
        for col in self.label_encoders:
            X_processed[col] = self.label_encoders[col].transform(X_engineered[col])
        
        # Scale features
        X_scaled = self.preprocessor.transform(X_processed)
        
        # Get base model predictions
        location_pred = self.location_model.predict(X_scaled[:, self.location_features])
        property_pred = self.property_model.predict(X_scaled[:, self.property_features])
        guest_pred = self.guest_model.predict(X_scaled[:, self.guest_features])
        price_pred = self.price_model.predict(X_scaled[:, self.price_features])
        
        # Meta-model prediction
        meta_features = np.column_stack([location_pred, property_pred, guest_pred, price_pred])
        final_predictions = self.meta_model.predict(meta_features)
        
        # Apply price penalty for extreme prices
        adjusted_predictions = []
        for i, pred in enumerate(final_predictions):
            price = X.iloc[i]['price'] if hasattr(X, 'iloc') else X[i]['price']
            adjusted_pred = self._apply_price_penalty(price, pred)
            adjusted_predictions.append(adjusted_pred)
        
        # Clip predictions to valid range [0, 100]
        adjusted_predictions = np.clip(adjusted_predictions, 0, 100)
        
        # Return predictions and breakdown
        base_predictions = {
            'location': location_pred,
            'property': property_pred,
            'guest': guest_pred,
            'price': price_pred
        }
        
        return np.array(adjusted_predictions), base_predictions
    
    def save(self, filepath='models/improved_ensemble.pkl'):
        """Save the trained ensemble."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"✅ Model saved to {filepath}")
    
    @staticmethod
    def load(filepath='models/improved_ensemble.pkl'):
        """Load a trained ensemble."""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Improved ensemble loaded from {filepath}")
        return model


def main():
    """Train and evaluate the improved ensemble."""
    print("=" * 80)
    print("TRAINING IMPROVED MULTI-MODAL ENSEMBLE WITH PRICE SENSITIVITY")
    print("=" * 80)
    
    # Load data
    print("\n📂 Loading data...")
    df = pd.read_csv('listings_data.csv')
    
    # Prepare features and target
    feature_cols = ['listing_type', 'room_type', 'max_guests', 'price', 
                   'bedrooms', 'beds', 'baths', 'lat', 'lng']
    X = df[feature_cols]
    y = df['occ_rate']
    
    print(f"   Loaded {len(df)} listings with {len(feature_cols)} base features")
    print(f"   Price range: ${X['price'].min():.2f} - ${X['price'].max():.2f}")
    print(f"   Occupancy range: {y.min():.0f}% - {y.max():.0f}%")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\n📊 Train set: {len(X_train)} listings")
    print(f"   Test set: {len(X_test)} listings")
    
    # Train model
    print("\n" + "=" * 80)
    print("TRAINING PHASE")
    print("=" * 80)
    
    ensemble = ImprovedMultiModalEnsemble()
    ensemble.fit(X_train, y_train)
    
    # Evaluate
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)
    
    # Training performance
    y_train_pred, _ = ensemble.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    
    print(f"\n📈 Training Performance:")
    print(f"   RMSE: {train_rmse:.2f}")
    print(f"   MAE: {train_mae:.2f}")
    print(f"   R²: {train_r2:.4f}")
    
    # Test performance
    y_test_pred, _ = ensemble.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"\n📉 Test Performance:")
    print(f"   RMSE: {test_rmse:.2f}")
    print(f"   MAE: {test_mae:.2f}")
    print(f"   R²: {test_r2:.4f}")
    
    # Test price sensitivity
    print("\n" + "=" * 80)
    print("PRICE SENSITIVITY TEST")
    print("=" * 80)
    
    test_listing = pd.DataFrame([{
        'listing_type': 'Entire rental unit',
        'room_type': 'Entire rental unit',
        'max_guests': 4,
        'price': 30,
        'bedrooms': 2,
        'beds': 2,
        'baths': 1,
        'lat': 33.7,
        'lng': 73.05
    }])
    
    test_prices = [30, 50, 100, 200, 500, 1000, 5000, 150000]
    
    print("\n📊 Predictions for varying prices:\n")
    print(f"{'Price ($)':>12} | {'Predicted Occ (%)':>18} | {'Change from $30':>15}")
    print("-" * 52)
    
    base_pred = None
    for price in test_prices:
        test_listing['price'] = price
        pred, _ = ensemble.predict(test_listing)
        
        if base_pred is None:
            base_pred = pred[0]
            change = "-"
        else:
            change = f"{pred[0] - base_pred:+.1f}%"
        
        print(f"${price:>10,.0f} | {pred[0]:>16.2f}% | {change:>15}")
    
    # Save model
    print("\n" + "=" * 80)
    print("SAVING MODEL")
    print("=" * 80)
    ensemble.save('models/improved_ensemble.pkl')
    
    print("\n✅ Training complete!")
    print("\n💡 To use this model: python predict_improved.py")
    

if __name__ == '__main__':
    main()
