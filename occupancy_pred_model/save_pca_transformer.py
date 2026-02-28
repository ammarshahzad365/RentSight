"""
Save PCA transformer for the trained model.
This extracts and saves the PCA transformer so it can be used for predictions.
"""

import pickle
import os
from sklearn.decomposition import PCA
from data_loader import load_listings_from_json
from preprocess import DataPreprocessor, create_train_test_split

def save_pca_transformer():
    """Create and save PCA transformer matching the training configuration."""
    print("="*60)
    print("SAVING PCA TRANSFORMER")
    print("="*60)
    
    # Load and preprocess data (same as training)
    listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    df = load_listings_from_json(listings_dir)
    
    X = df.drop('occ_rate', axis=1)
    y = df['occ_rate']
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    preprocessor = DataPreprocessor()
    X_train_processed, _ = preprocessor.fit_transform(X_train)
    
    # Create PCA with 5 components (95% variance)
    pca = PCA(n_components=5)
    pca.fit(X_train_processed)
    
    # Save PCA transformer
    os.makedirs('models', exist_ok=True)
    with open('models/pca_transformer.pkl', 'wb') as f:
        pickle.dump(pca, f)
    
    print(f"\n✓ PCA transformer saved to models/pca_transformer.pkl")
    print(f"  Components: {pca.n_components_}")
    print(f"  Variance explained: {pca.explained_variance_ratio_.sum():.4f}")
    
    # Also save the preprocessor specifically for PCA model
    with open('models/preprocessor_pca_only.pkl', 'wb') as f:
        pickle.dump(preprocessor, f)
    
    print(f"✓ Preprocessor saved to models/preprocessor_pca_only.pkl")

if __name__ == "__main__":
    save_pca_transformer()
