"""
Multi-Modal Ensemble Model for Occupancy Prediction
Uses different models for different feature types:
- KNN for location features (lat, lng)
- Random Forest for property features (price, bedrooms, beds, baths)
- Gradient Boosting for guest capacity and listing type
Then combines predictions using weighted averaging or meta-model
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

from data_loader import load_listings_from_json
from preprocess import DataPreprocessor, create_train_test_split

class MultiModalEnsemble:
    """
    Multi-modal ensemble that uses different models for different feature groups.
    
    Architecture:
    - KNN Model: Specializes in location features (lat, lng)
    - Random Forest: Specializes in property features (price, bedrooms, beds, baths)
    - Gradient Boosting: Specializes in guest/listing features (max_guests, listing_type, room_type)
    - Meta-Model (Ridge): Combines predictions from all base models
    """
    
    def __init__(self):
        # Base models
        self.location_model = KNeighborsRegressor(n_neighbors=7, weights='distance')
        self.property_model = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42)
        self.guest_model = GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, random_state=42)
        
        # Meta-model to combine predictions
        self.meta_model = Ridge(alpha=1.0)
        
        # Feature groups
        self.location_features = ['lat', 'lng']
        self.property_features = ['price', 'bedrooms', 'beds', 'baths']
        self.guest_features = ['max_guests', 'listing_type', 'room_type']
        
        self.preprocessor = None
        self.feature_names = None
        self.is_trained = False
        
    def _get_feature_indices(self):
        """Get indices for each feature group."""
        location_indices = [self.feature_names.index(f) for f in self.location_features if f in self.feature_names]
        property_indices = [self.feature_names.index(f) for f in self.property_features if f in self.feature_names]
        guest_indices = [self.feature_names.index(f) for f in self.guest_features if f in self.feature_names]
        
        return location_indices, property_indices, guest_indices
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train all base models and meta-model.
        
        Stage 1: Train base models on their specialized feature groups
        Stage 2: Generate predictions from base models
        Stage 3: Train meta-model to optimally combine base model predictions
        """
        print("\n" + "="*70)
        print("MULTI-MODAL ENSEMBLE TRAINING")
        print("="*70)
        
        # Convert to numpy array if DataFrame
        if hasattr(X_train, 'values'):
            X_train = X_train.values
        if hasattr(X_val, 'values'):
            X_val = X_val.values
        
        # Get feature indices
        location_idx, property_idx, guest_idx = self._get_feature_indices()
        
        print(f"\nFeature Groups:")
        print(f"  Location Features ({len(location_idx)}): {[self.feature_names[i] for i in location_idx]}")
        print(f"  Property Features ({len(property_idx)}): {[self.feature_names[i] for i in property_idx]}")
        print(f"  Guest Features ({len(guest_idx)}): {[self.feature_names[i] for i in guest_idx]}")
        
        # Stage 1: Train base models
        print("\n" + "-"*70)
        print("Stage 1: Training Base Models")
        print("-"*70)
        
        # Train location model (KNN)
        print("\n1. Training KNN on location features...")
        X_location = X_train[:, location_idx]
        self.location_model.fit(X_location, y_train)
        location_pred = self.location_model.predict(X_location)
        location_rmse = np.sqrt(mean_squared_error(y_train, location_pred))
        print(f"   ✓ Location Model RMSE: {location_rmse:.4f}")
        
        # Train property model (Random Forest)
        print("\n2. Training Random Forest on property features...")
        X_property = X_train[:, property_idx]
        self.property_model.fit(X_property, y_train)
        property_pred = self.property_model.predict(X_property)
        property_rmse = np.sqrt(mean_squared_error(y_train, property_pred))
        print(f"   ✓ Property Model RMSE: {property_rmse:.4f}")
        
        # Train guest model (Gradient Boosting)
        print("\n3. Training Gradient Boosting on guest features...")
        X_guest = X_train[:, guest_idx]
        self.guest_model.fit(X_guest, y_train)
        guest_pred = self.guest_model.predict(X_guest)
        guest_rmse = np.sqrt(mean_squared_error(y_train, guest_pred))
        print(f"   ✓ Guest Model RMSE: {guest_rmse:.4f}")
        
        # Stage 2: Generate meta-features (predictions from base models)
        print("\n" + "-"*70)
        print("Stage 2: Generating Meta-Features")
        print("-"*70)
        
        meta_features_train = np.column_stack([
            location_pred,
            property_pred,
            guest_pred
        ])
        
        print(f"Meta-features shape: {meta_features_train.shape}")
        
        # Stage 3: Train meta-model
        print("\n" + "-"*70)
        print("Stage 3: Training Meta-Model (Ridge Regression)")
        print("-"*70)
        
        self.meta_model.fit(meta_features_train, y_train)
        
        # Get meta-model weights
        weights = self.meta_model.coef_
        print(f"\nLearned Weights:")
        print(f"  Location Model (KNN): {weights[0]:.4f}")
        print(f"  Property Model (RF): {weights[1]:.4f}")
        print(f"  Guest Model (GB): {weights[2]:.4f}")
        print(f"  Intercept: {self.meta_model.intercept_:.4f}")
        
        # Final ensemble prediction on training data
        ensemble_pred = self.meta_model.predict(meta_features_train)
        ensemble_rmse = np.sqrt(mean_squared_error(y_train, ensemble_pred))
        
        print(f"\n" + "="*70)
        print("TRAINING RESULTS")
        print("="*70)
        print(f"Location Model RMSE:  {location_rmse:.4f}")
        print(f"Property Model RMSE:  {property_rmse:.4f}")
        print(f"Guest Model RMSE:     {guest_rmse:.4f}")
        print(f"Ensemble Model RMSE:  {ensemble_rmse:.4f}")
        print("="*70)
        
        self.is_trained = True
        
    def predict(self, X_test):
        """Generate predictions using the ensemble."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Convert to numpy array if DataFrame
        if hasattr(X_test, 'values'):
            X_test = X_test.values
        
        # Get feature indices
        location_idx, property_idx, guest_idx = self._get_feature_indices()
        
        # Get predictions from each base model
        X_location = X_test[:, location_idx]
        X_property = X_test[:, property_idx]
        X_guest = X_test[:, guest_idx]
        
        location_pred = self.location_model.predict(X_location)
        property_pred = self.property_model.predict(X_property)
        guest_pred = self.guest_model.predict(X_guest)
        
        # Create meta-features
        meta_features = np.column_stack([
            location_pred,
            property_pred,
            guest_pred
        ])
        
        # Get final ensemble prediction
        ensemble_pred = self.meta_model.predict(meta_features)
        
        return ensemble_pred, {
            'location': location_pred,
            'property': property_pred,
            'guest': guest_pred
        }
    
    def evaluate(self, X_test, y_test):
        """Evaluate the ensemble on test data."""
        ensemble_pred, base_predictions = self.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, ensemble_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, ensemble_pred)
        r2 = r2_score(y_test, ensemble_pred)
        
        print("\n" + "="*70)
        print("MULTI-MODAL ENSEMBLE EVALUATION")
        print("="*70)
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE:  {mae:.4f}")
        print(f"R²:   {r2:.4f}")
        
        # Evaluate individual models
        print("\nBase Model Performance on Test Set:")
        for name, pred in base_predictions.items():
            model_rmse = np.sqrt(mean_squared_error(y_test, pred))
            print(f"  {name.capitalize()} Model: {model_rmse:.4f}")
        
        print("="*70)
        
        return {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'base_predictions': base_predictions
        }
    
    def save(self, filepath):
        """Save the entire ensemble."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'location_model': self.location_model,
            'property_model': self.property_model,
            'guest_model': self.guest_model,
            'meta_model': self.meta_model,
            'feature_names': self.feature_names,
            'preprocessor': self.preprocessor
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\n✓ Multi-modal ensemble saved to {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """Load a saved ensemble."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        ensemble = cls()
        ensemble.location_model = model_data['location_model']
        ensemble.property_model = model_data['property_model']
        ensemble.guest_model = model_data['guest_model']
        ensemble.meta_model = model_data['meta_model']
        ensemble.feature_names = model_data['feature_names']
        ensemble.preprocessor = model_data['preprocessor']
        ensemble.is_trained = True
        
        print(f"✓ Multi-modal ensemble loaded from {filepath}")
        return ensemble

def plot_model_comparison(y_test, ensemble_pred, base_predictions, save_path=None):
    """Plot comparison of all model predictions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    models = [
        ('Location Model (KNN)', base_predictions['location'], axes[0, 0]),
        ('Property Model (RF)', base_predictions['property'], axes[0, 1]),
        ('Guest Model (GB)', base_predictions['guest'], axes[1, 0]),
        ('Ensemble Model', ensemble_pred, axes[1, 1])
    ]
    
    for title, pred, ax in models:
        ax.scatter(y_test, pred, alpha=0.6, edgecolors='k')
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                'r--', lw=2)
        
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        ax.set_xlabel('Actual Occupancy Rate', fontsize=11)
        ax.set_ylabel('Predicted Occupancy Rate', fontsize=11)
        ax.set_title(f'{title}\nRMSE: {rmse:.2f}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Comparison plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def compare_with_single_models(X_train, y_train, X_test, y_test, feature_names):
    """Compare multi-modal ensemble with traditional single models."""
    print("\n" + "="*70)
    print("COMPARISON: Multi-Modal vs Single Models")
    print("="*70)
    
    results = {}
    
    # Train single models on all features
    print("\nTraining single models on ALL features...")
    
    models = {
        'KNN': KNeighborsRegressor(n_neighbors=5, weights='distance'),
        'Random Forest': RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, max_depth=7, random_state=42)
    }
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        results[f'{name} (All Features)'] = rmse
        print(f"  {name}: {rmse:.4f}")
    
    # Train multi-modal ensemble
    print("\nTraining Multi-Modal Ensemble...")
    ensemble = MultiModalEnsemble()
    ensemble.feature_names = feature_names
    ensemble.train(X_train, y_train)
    
    ensemble_pred, base_preds = ensemble.predict(X_test)
    ensemble_rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
    results['Multi-Modal Ensemble'] = ensemble_rmse
    
    # Display comparison
    print("\n" + "="*70)
    print("FINAL COMPARISON")
    print("="*70)
    results_sorted = sorted(results.items(), key=lambda x: x[1])
    for i, (name, rmse) in enumerate(results_sorted, 1):
        marker = "🏆" if i == 1 else "  "
        print(f"{marker} {i}. {name}: {rmse:.4f}")
    print("="*70)
    
    # Plot comparison
    plot_model_comparison(y_test, ensemble_pred, base_preds, 
                         'models/multimodal_comparison.png')
    
    return ensemble, results

def main():
    """Train and evaluate multi-modal ensemble."""
    print("="*70)
    print("MULTI-MODAL ENSEMBLE MODEL TRAINING")
    print("="*70)
    
    # Load data
    print("\nLoading data...")
    listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    df = load_listings_from_json(listings_dir)
    print(f"Loaded {len(df)} listings")
    
    # Split and preprocess
    X = df.drop('occ_rate', axis=1)
    y = df['occ_rate']
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    preprocessor = DataPreprocessor()
    X_train_processed, _ = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    feature_names = preprocessor.feature_names
    
    print(f"Train: {len(X_train_processed)} | Test: {len(X_test_processed)} | Features: {len(feature_names)}")
    print(f"Features: {feature_names}")
    
    # Train multi-modal ensemble
    ensemble = MultiModalEnsemble()
    ensemble.feature_names = feature_names
    ensemble.preprocessor = preprocessor
    ensemble.train(X_train_processed, y_train)
    
    # Evaluate
    metrics = ensemble.evaluate(X_test_processed, y_test)
    
    # Plot predictions
    ensemble_pred, base_preds = ensemble.predict(X_test_processed)
    plot_model_comparison(y_test, ensemble_pred, base_preds, 
                         'models/multimodal_predictions.png')
    
    # Save model
    ensemble.save('models/multimodal_ensemble.pkl')
    
    # Compare with traditional models
    print("\n")
    ensemble_full, comparison_results = compare_with_single_models(
        X_train_processed, y_train, X_test_processed, y_test, feature_names
    )
    
    # Save the better-performing ensemble
    if comparison_results['Multi-Modal Ensemble'] < min([v for k, v in comparison_results.items() if k != 'Multi-Modal Ensemble']):
        print("\n✓ Multi-Modal Ensemble is the best performer!")
        ensemble_full.save('models/multimodal_ensemble_best.pkl')
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
