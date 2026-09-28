import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from preprocess import DataPreprocessor

def perform_pca_analysis(X, feature_names, n_components=None):
    """
    Perform PCA analysis on the features.
    
    Parameters:
    -----------
    X : array-like
        Feature matrix (already scaled)
    feature_names : list
        Names of features
    n_components : int or None
        Number of components to keep. If None, keeps all.
    
    Returns:
    --------
    pca : PCA object
        Fitted PCA transformer
    X_pca : array
        Transformed features
    explained_variance : array
        Variance explained by each component
    """
    if n_components is None:
        n_components = min(X.shape[0], X.shape[1])
    
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    
    print(f"\n{'='*60}")
    print(f"PCA Analysis Results")
    print(f"{'='*60}")
    print(f"Original features: {X.shape[1]}")
    print(f"PCA components: {pca.n_components_}")
    print(f"\nExplained variance ratio by component:")
    
    cumulative_variance = 0
    for i, var in enumerate(pca.explained_variance_ratio_):
        cumulative_variance += var
        print(f"  PC{i+1}: {var:.4f} (Cumulative: {cumulative_variance:.4f})")
    
    # Feature importance in principal components
    print(f"\nFeature loadings in principal components:")
    components_df = pd.DataFrame(
        pca.components_,
        columns=feature_names,
        index=[f'PC{i+1}' for i in range(pca.n_components_)]
    )
    
    print(components_df.round(3))
    
    # Calculate feature importance based on PCA
    feature_importance = np.abs(pca.components_).sum(axis=0)
    feature_importance = feature_importance / feature_importance.sum()
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\n{'='*60}")
    print("Feature Importance from PCA:")
    print(f"{'='*60}")
    print(importance_df.to_string(index=False))
    
    return pca, X_pca, pca.explained_variance_ratio_, importance_df

def plot_pca_variance(explained_variance, save_path=None):
    """Plot explained variance by PCA components."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scree plot
    components = range(1, len(explained_variance) + 1)
    ax1.bar(components, explained_variance, alpha=0.7, color='steelblue')
    ax1.set_xlabel('Principal Component', fontsize=12)
    ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
    ax1.set_title('Scree Plot - Variance per Component', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Cumulative variance
    cumulative_variance = np.cumsum(explained_variance)
    ax2.plot(components, cumulative_variance, marker='o', linestyle='-', linewidth=2, color='darkred')
    ax2.axhline(y=0.95, color='green', linestyle='--', label='95% Variance')
    ax2.axhline(y=0.90, color='orange', linestyle='--', label='90% Variance')
    ax2.set_xlabel('Number of Components', fontsize=12)
    ax2.set_ylabel('Cumulative Explained Variance', fontsize=12)
    ax2.set_title('Cumulative Explained Variance', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPCA variance plot saved to {save_path}")
    else:
        plt.show()

def plot_pca_feature_importance(importance_df, save_path=None):
    """Plot feature importance from PCA."""
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['feature'], importance_df['importance'], color='teal')
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title('Feature Importance from PCA Analysis', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"PCA feature importance plot saved to {save_path}")
    else:
        plt.show()

def get_optimal_n_components(explained_variance, threshold=0.95):
    """
    Determine optimal number of components to retain given variance threshold.
    
    Parameters:
    -----------
    explained_variance : array
        Explained variance ratios
    threshold : float
        Minimum cumulative variance to retain (default 0.95 = 95%)
    
    Returns:
    --------
    int : Optimal number of components
    """
    cumulative_variance = np.cumsum(explained_variance)
    n_components = np.argmax(cumulative_variance >= threshold) + 1
    
    print(f"\nOptimal components to retain {threshold*100}% variance: {n_components}")
    print(f"Actual variance retained: {cumulative_variance[n_components-1]:.4f}")
    
    return n_components

if __name__ == "__main__":
    import os
    
    # Load data
    print("Loading data...")
    df = pd.read_csv('listings_data.csv')
    
    # Preprocess
    print("Preprocessing data...")
    preprocessor = DataPreprocessor()
    X, y = preprocessor.fit_transform(df, target_col='occ_rate')
    
    # Perform PCA analysis
    pca, X_pca, explained_variance, importance_df = perform_pca_analysis(
        X, preprocessor.feature_names
    )
    
    # Get optimal number of components
    optimal_n = get_optimal_n_components(explained_variance, threshold=0.95)
    
    # Plot results
    model_dir = os.path.dirname(__file__)
    plot_pca_variance(
        explained_variance,
        save_path=os.path.join(model_dir, 'pca_variance.png')
    )
    
    plot_pca_feature_importance(
        importance_df,
        save_path=os.path.join(model_dir, 'pca_feature_importance.png')
    )
    
    print("\nPCA analysis completed!")
