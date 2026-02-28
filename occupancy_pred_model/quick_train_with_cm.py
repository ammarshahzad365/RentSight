"""
Quick Model Training for Confusion Matrix Generation
Trains only tree-based models (Random Forest, Gradient Boosting, KNN) without neural networks
to quickly generate confusion matrices for comparison.
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, confusion_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import load_listings_from_json
from preprocess import DataPreprocessor, create_train_test_split
from feature_analysis import perform_pca_analysis, get_optimal_n_components

def bin_occupancy_rates(rates):
    """Bin occupancy rates into categories for confusion matrix."""
    bins = [0, 40, 60, 80, 100]
    labels = ['Low (0-40%)', 'Medium (40-60%)', 'High (60-80%)', 'Very High (80-100%)']
    return pd.cut(rates, bins=bins, labels=labels, include_lowest=True)

def plot_confusion_matrix(y_test, y_pred, model_type, config_name, save_path=None):
    """Plot confusion matrix for binned regression predictions."""
    # Bin the actual and predicted values
    y_test_binned = bin_occupancy_rates(y_test)
    y_pred_binned = bin_occupancy_rates(y_pred)
    
    # Create confusion matrix
    labels = ['Low\n(0-40%)', 'Medium\n(40-60%)', 'High\n(60-80%)', 'Very High\n(80-100%)']
    cm = confusion_matrix(y_test_binned, y_pred_binned, 
                         labels=['Low (0-40%)', 'Medium (40-60%)', 'High (60-80%)', 'Very High (80-100%)'])
    
    # Calculate percentages
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    # Create figure
    plt.figure(figsize=(11, 9))
    
    # Create annotations with counts and percentages
    annot = np.empty_like(cm, dtype=object)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if not np.isnan(cm_percent[i, j]):
                annot[i, j] = f'{cm[i, j]}\n({cm_percent[i, j]:.1f}%)'
            else:
                annot[i, j] = f'{cm[i, j]}\n(0.0%)'
    
    # Plot heatmap
    sns.heatmap(cm, annot=annot, fmt='', cmap='Blues', 
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Count'}, linewidths=2, linecolor='white',
                vmin=0, vmax=cm.max())
    
    plt.title(f'{model_type.upper()}\n{config_name}', 
             fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Actual Occupancy Category', fontsize=13, fontweight='bold')
    plt.xlabel('Predicted Occupancy Category', fontsize=13, fontweight='bold')
    
    # Calculate and add accuracy text
    accuracy = np.trace(cm) / np.sum(cm) * 100
    plt.text(0.5, -0.15, f'Classification Accuracy: {accuracy:.2f}%', 
            transform=plt.gca().transAxes, ha='center', fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Confusion matrix saved: {os.path.basename(save_path)}")
    
    plt.close()
    
    return accuracy, cm

def train_quick_models(X_train, y_train, X_test, y_test, config_name, 
                       use_pca=False, n_components=None, feature_weights=None):
    """Train only tree-based models (faster than neural networks)."""
    print(f"\n{'='*70}")
    print(f"Configuration: {config_name}")
    print(f"{'='*70}")
    
    models = {
        'random_forest': RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
        'gradient_boosting': GradientBoostingRegressor(n_estimators=200, max_depth=7, random_state=42),
        'knn': KNeighborsRegressor(n_neighbors=5, weights='distance', n_jobs=-1)
    }
    
    results = []
    
    for model_name, model in models.items():
        print(f"\n{model_name.upper().replace('_', ' ')}")
        print("-" * 70)
        
        # Prepare data
        X_train_proc = X_train.copy()
        X_test_proc = X_test.copy()
        
        # Apply feature weighting before PCA if both are enabled
        if feature_weights is not None and not use_pca:
            weights_normalized = feature_weights / feature_weights.mean()
            X_train_proc = X_train_proc * weights_normalized
            X_test_proc = X_test_proc * weights_normalized
            print(f"  Applied feature weighting")
        elif feature_weights is not None and use_pca:
            # Apply weighting before PCA transformation
            weights_normalized = feature_weights / feature_weights.mean()
            X_train_proc = X_train_proc * weights_normalized
            X_test_proc = X_test_proc * weights_normalized
            print(f"  Applied feature weighting")
        
        # Apply PCA if enabled (after weighting if applicable)
        if use_pca:
            pca = PCA(n_components=n_components)
            X_train_proc = pca.fit_transform(X_train_proc)
            X_test_proc = pca.transform(X_test_proc)
            print(f"  Applied PCA: {X_train_proc.shape[1]} components")
        
        # Train
        model.fit(X_train_proc, y_train)
        y_pred = model.predict(X_test_proc)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"  RMSE: {rmse:.4f} | MAE: {mae:.4f} | R²: {r2:.4f}")
        
        # Generate confusion matrix
        config_safe = config_name.replace(" ", "_").replace("+", "").lower()
        cm_path = f'models/cm_{model_name}_{config_safe}.png'
        accuracy, cm = plot_confusion_matrix(y_test, y_pred, model_name.replace('_', ' '), 
                                            config_name, cm_path)
        
        results.append({
            'Model': model_name.replace('_', ' ').title(),
            'Config': config_name,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'Category_Accuracy_%': accuracy
        })
    
    return results

def main():
    """Quick training to generate confusion matrices."""
    print("="*70)
    print("QUICK MODEL TRAINING FOR CONFUSION MATRICES")
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
    
    # Get PCA components
    print("\nPerforming PCA analysis...")
    pca_model, X_pca, explained_variance, pca_importance = perform_pca_analysis(
        X_train_processed, feature_names)
    optimal_n = get_optimal_n_components(explained_variance, threshold=0.95)
    
    # Get feature importance
    print("\nCalculating feature importance...")
    rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_temp.fit(X_train_processed, y_train)
    feature_weights = np.array(rf_temp.feature_importances_)
    
    os.makedirs('models', exist_ok=True)
    
    all_results = []
    
    # Train all configurations
    configs = [
        ("Baseline (No PCA, No Weighting)", False, None, None),
        ("Feature Weighting Only", False, None, feature_weights),
        ("PCA Only", True, optimal_n, None),
        ("PCA + Feature Weighting", True, optimal_n, feature_weights)
    ]
    
    for config_name, use_pca, n_comp, weights in configs:
        results = train_quick_models(X_train_processed, y_train, X_test_processed, y_test,
                                     config_name, use_pca, n_comp, weights)
        all_results.extend(results)
    
    # Summary
    print(f"\n{'='*70}")
    print("FINAL RESULTS SUMMARY")
    print(f"{'='*70}")
    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values('RMSE')
    print(results_df.to_string(index=False))
    
    print(f"\n{'='*70}")
    print(f"✓ All confusion matrices saved in: {os.path.abspath('models')}/")
    print(f"✓ Total confusion matrices generated: {len(all_results)}")
    print(f"{'='*70}")
    
    # Best model
    best = results_df.iloc[0]
    print(f"\n🏆 BEST MODEL: {best['Model']} ({best['Config']})")
    print(f"   RMSE: {best['RMSE']:.4f}")
    print(f"   Category Accuracy: {best['Category_Accuracy_%']:.2f}%")

if __name__ == "__main__":
    main()
