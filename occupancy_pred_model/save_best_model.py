"""
Save the best Random Forest with PCA model for production use.
"""

import pickle
import os
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from data_loader import load_listings_from_json
from preprocess import DataPreprocessor, create_train_test_split

def save_best_model():
    """Train and save the best model (Random Forest with PCA Only)."""
    print("="*60)
    print("TRAINING AND SAVING BEST MODEL")
    print("Random Forest with PCA Only (RMSE: 17.11)")
    print("="*60)
    
    # Load and preprocess data
    print("\nLoading data...")
    listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    df = load_listings_from_json(listings_dir)
    
    X = df.drop('occ_rate', axis=1)
    y = df['occ_rate']
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    # Preprocess
    print("Preprocessing...")
    preprocessor = DataPreprocessor()
    X_train_processed, _ = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Apply PCA
    print("Applying PCA...")
    pca = PCA(n_components=5)
    X_train_pca = pca.fit_transform(X_train_processed)
    X_test_pca = pca.transform(X_test_processed)
    
    # Train Random Forest
    print("Training Random Forest...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_pca, y_train)
    
    # Evaluate
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    y_pred = model.predict(X_test_pca)
    rmse = (mean_squared_error(y_test, y_pred)) ** 0.5
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE: {mae:.4f}")
    print(f"  R²: {r2:.4f}")
    
    # Save everything
    os.makedirs('models', exist_ok=True)
    
    # Save model
    with open('models/random_forest_pca_only.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✓ Model saved to models/random_forest_pca_only.pkl")
    
    # Save PCA transformer
    with open('models/pca_transformer.pkl', 'wb') as f:
        pickle.dump(pca, f)
    print(f"✓ PCA transformer saved to models/pca_transformer.pkl")
    
    # Save preprocessor
    with open('models/preprocessor_pca_only.pkl', 'wb') as f:
        pickle.dump(preprocessor, f)
    print(f"✓ Preprocessor saved to models/preprocessor_pca_only.pkl")
    
    print("\n" + "="*60)
    print("✓ Best model saved and ready for predictions!")
    print("  Use predict_occupancy.py to make predictions")
    print("="*60)

if __name__ == "__main__":
    save_best_model()
