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
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks

from preprocess import DataPreprocessor, create_train_test_split
from feature_analysis import perform_pca_analysis, get_optimal_n_components

class OccupancyPredictor:
    """Train and evaluate occupancy rate prediction models."""
    
    def __init__(self, model_type='random_forest', input_dim=None, use_pca=False, n_components=None, feature_weights=None):
        self.model_type = model_type
        self.input_dim = input_dim
        self.use_pca = use_pca
        self.n_components = n_components
        self.feature_weights = feature_weights
        self.pca = None
        self.model = self._create_model(model_type, input_dim)
        self.preprocessor = DataPreprocessor()
        self.is_trained = False
        self.history = None
    
    def _create_model(self, model_type, input_dim=None):
        """Create model based on type."""
        if model_type == 'neural_network':
            if input_dim is None:
                raise ValueError("input_dim must be specified for neural network")
            
            # Set random seeds for reproducibility
            np.random.seed(42)
            tf.random.set_seed(42)
            
            model = keras.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
                layers.Dropout(0.2),
                layers.Dense(32, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
                layers.Dropout(0.2),
                layers.Dense(16, activation='relu'),
                layers.Dense(1)
            ])
            
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae']
            )
            
            return model
        
        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=3,
                min_samples_leaf=1,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.05,
                random_state=42
            ),
            'knn': KNeighborsRegressor(
                n_neighbors=5,
                weights='distance',
                n_jobs=-1
            )
        }
        
        if model_type not in models:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return models[model_type]
    
    def apply_feature_weighting(self, X, weights):
        """Apply feature weights to the data."""
        if weights is None:
            return X
        # Normalize weights to have mean=1 to preserve scale
        weights_normalized = weights / weights.mean()
        return X * weights_normalized
    
    def apply_pca_transform(self, X):
        """Apply PCA transformation if enabled."""
        if self.use_pca and self.pca is not None:
            return self.pca.transform(X)
        return X
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=200, batch_size=32):
        """Train the model."""
        print(f"\nTraining {self.model_type} model...")
        
        # Apply PCA if enabled
        if self.use_pca:
            if self.pca is None:
                self.pca = PCA(n_components=self.n_components)
                X_train = self.pca.fit_transform(X_train)
                print(f"Applied PCA: {X_train.shape[1]} components")
                
                # Recreate neural network with new input dimension
                if self.model_type == 'neural_network':
                    self.input_dim = X_train.shape[1]
                    self.model = self._create_model('neural_network', self.input_dim)
            else:
                X_train = self.pca.transform(X_train)
            
            if X_val is not None:
                X_val = self.pca.transform(X_val)
        
        # Apply feature weighting
        X_train = self.apply_feature_weighting(X_train, self.feature_weights)
        if X_val is not None:
            X_val = self.apply_feature_weighting(X_val, self.feature_weights)
        
        if self.model_type == 'neural_network':
            # Callbacks for neural network
            early_stop = callbacks.EarlyStopping(
                monitor='val_loss',
                patience=30,
                restore_best_weights=True,
                verbose=1
            )
            
            reduce_lr = callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=15,
                verbose=1
            )
            
            if X_val is not None and y_val is not None:
                self.history = self.model.fit(
                    X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=epochs,
                    batch_size=batch_size,
                    callbacks=[early_stop, reduce_lr],
                    verbose=1
                )
            else:
                self.history = self.model.fit(
                    X_train, y_train,
                    validation_split=0.2,
                    epochs=epochs,
                    batch_size=batch_size,
                    callbacks=[early_stop, reduce_lr],
                    verbose=1
                )
        else:
            self.model.fit(X_train, y_train)
        
        self.is_trained = True
        print("Training completed!")
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Apply PCA if enabled
        if self.use_pca and self.pca is not None:
            X_test = self.pca.transform(X_test)
        
        # Apply feature weighting
        X_test = self.apply_feature_weighting(X_test, self.feature_weights)
        
        if self.model_type == 'neural_network':
            y_pred = self.model.predict(X_test, verbose=0)
        else:
            y_pred = self.model.predict(X_test)
        
        if len(y_pred.shape) > 1:
            y_pred = y_pred.flatten()
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        metrics = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'MAPE': mape
        }
        
        print(f"\n{'='*50}")
        print(f"Model Evaluation - {self.model_type}")
        print(f"{'='*50}")
        for metric, value in metrics.items():
            print(f"{metric:12s}: {value:.4f}")
        print(f"{'='*50}\n")
        
        return metrics, y_pred
    
    def get_feature_importance(self, feature_names):
        """Get feature importance for tree-based models."""
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            return feature_importance
        else:
            return None
    
    def save(self, model_path, preprocessor_path):
        """Save model and preprocessor to disk."""
        if self.model_type == 'neural_network':
            self.model.save(model_path.replace('.pkl', '.keras'))
            print(f"Model saved to {model_path.replace('.pkl', '.keras')}")
        else:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"Model saved to {model_path}")
        
        with open(preprocessor_path, 'wb') as f:
            pickle.dump(self.preprocessor, f)
        print(f"Preprocessor saved to {preprocessor_path}")

def plot_predictions(y_test, y_pred, model_type, save_path=None):
    """Plot actual vs predicted values."""
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolors='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'r--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual Occupancy Rate', fontsize=12)
    plt.ylabel('Predicted Occupancy Rate', fontsize=12)
    plt.title(f'Actual vs Predicted Occupancy Rate - {model_type}', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Prediction plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

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
    labels = ['Low (0-40%)', 'Medium (40-60%)', 'High (60-80%)', 'Very High (80-100%)']
    cm = confusion_matrix(y_test_binned, y_pred_binned, labels=labels)
    
    # Calculate percentages
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    # Create figure
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Count'})
    
    # Add percentage annotations
    for i in range(len(labels)):
        for j in range(len(labels)):
            if not np.isnan(cm_percent[i, j]):
                plt.text(j + 0.5, i + 0.7, f'({cm_percent[i, j]:.1f}%)',
                        ha='center', va='center', fontsize=9, color='gray')
    
    plt.title(f'Confusion Matrix - {model_type}\n{config_name}', fontsize=14, fontweight='bold')
    plt.ylabel('Actual Occupancy Category', fontsize=12)
    plt.xlabel('Predicted Occupancy Category', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Confusion matrix saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    # Calculate and return accuracy
    accuracy = np.trace(cm) / np.sum(cm) * 100
    return accuracy

def train_and_compare_models(X_train, y_train, X_test, y_test, feature_names, 
                              use_pca=False, n_components=None, feature_weights=None):
    """Train and compare multiple models."""
    config_name = f"{'PCA' if use_pca else 'No PCA'} + {'Weighted' if feature_weights is not None else 'No Weighting'}"
    print("\n" + "="*60)
    print(f"Training Models {'with PCA' if use_pca else 'without PCA'} "
          f"{'and feature weighting' if feature_weights is not None else ''}")
    print("="*60)
    
    model_types = ['neural_network', 'random_forest', 'gradient_boosting', 'knn']
    results = {}
    predictions = {}
    confusion_accuracies = {}
    
    for model_type in model_types:
        print(f"\n{'='*60}")
        print(f"Training: {model_type.upper().replace('_', ' ')}")
        print(f"{'='*60}")
        
        input_dim = X_train.shape[1] if model_type == 'neural_network' else None
        predictor = OccupancyPredictor(
            model_type=model_type, 
            input_dim=input_dim,
            use_pca=use_pca,
            n_components=n_components,
            feature_weights=feature_weights
        )
        
        predictor.train(X_train, y_train)
        metrics, y_pred = predictor.evaluate(X_test, y_test)
        
        results[model_type] = metrics
        predictions[model_type] = y_pred
        
        # Print some sample predictions
        print("\nSample predictions (first 5):")
        print("Actual | Predicted")
        print("-" * 25)
        for actual, pred in zip(y_test[:5], y_pred[:5]):
            print(f"{actual:6.2f} | {pred:6.2f}")
        
        # Generate confusion matrix
        cm_save_path = f'models/confusion_matrix_{model_type}_{config_name.replace(" ", "_").replace("+", "")}.png'
        cm_accuracy = plot_confusion_matrix(y_test, y_pred, model_type, config_name, cm_save_path)
        confusion_accuracies[model_type] = cm_accuracy
        print(f"\nCategory Classification Accuracy: {cm_accuracy:.2f}%")
        
        # Save best model (Random Forest)
        if model_type == 'random_forest':
            model_path = 'models/occupancy_model.pkl'
            preprocessor_path = 'models/preprocessor.pkl'
            os.makedirs('models', exist_ok=True)
            predictor.save(model_path, preprocessor_path)
            
            # Get and display feature importance
            feature_importance = predictor.get_feature_importance(feature_names)
            if feature_importance is not None:
                print("\nFeature Importance:")
                print(feature_importance.to_string(index=False))
            
            # Plot predictions
            plot_path = 'models/predictions_plot.png'
            plot_predictions(y_test, y_pred, model_type, plot_path)
    
    # Compare all models
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    comparison_df = pd.DataFrame(results).T
    comparison_df['Category_Accuracy'] = pd.Series(confusion_accuracies)
    print(comparison_df.to_string())
    
    # Find best model
    best_model = comparison_df['RMSE'].idxmin()
    print(f"\nBest Model (by RMSE): {best_model.upper().replace('_', ' ')}")
    print(f"RMSE: {comparison_df.loc[best_model, 'RMSE']:.4f}")
    print(f"Category Accuracy: {comparison_df.loc[best_model, 'Category_Accuracy']:.2f}%")
    
    return results, predictions

def main():
    """Main training pipeline."""
    print("="*60)
    print("OCCUPANCY RATE PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    from data_loader import load_listings_from_json
    listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    df = load_listings_from_json(listings_dir)
    print(f"Loaded {len(df)} listings")
    
    # Create train-test split
    print("\nCreating train-test split...")
    X = df.drop('occ_rate', axis=1)
    y = df['occ_rate']
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    # Preprocess data
    print("\nPreprocessing data...")
    preprocessor = DataPreprocessor()
    X_train_processed, _ = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    feature_names = preprocessor.feature_names
    
    print(f"\nTraining set size: {X_train_processed.shape[0]} samples")
    print(f"Test set size: {X_test_processed.shape[0]} samples")
    print(f"Number of features: {X_train_processed.shape[1]}")
    print(f"Features: {feature_names}")
    
    # First, perform PCA analysis to understand the data
    print("\n" + "="*60)
    print("PERFORMING PCA ANALYSIS")
    print("="*60)
    pca_model, X_pca, explained_variance, pca_importance = perform_pca_analysis(X_train_processed, feature_names)
    optimal_n = get_optimal_n_components(explained_variance, threshold=0.95)
    print(f"\nOptimal number of components (95% variance): {optimal_n}")
    
    # Get feature importance from a quick Random Forest model
    print("\n" + "="*60)
    print("CALCULATING FEATURE IMPORTANCE")
    print("="*60)
    rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_temp.fit(X_train_processed, y_train)
    feature_importance = rf_temp.feature_importances_
    
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance (for weighting):")
    print(feature_importance_df.to_string(index=False))
    
    # Create feature weights dictionary
    feature_weights = np.array(feature_importance)
    
    # Train models without PCA or weighting (baseline)
    print("\n" + "="*60)
    print("BASELINE: NO PCA, NO FEATURE WEIGHTING")
    print("="*60)
    results_baseline, _ = train_and_compare_models(
        X_train_processed, y_train, X_test_processed, y_test, 
        feature_names,
        use_pca=False,
        feature_weights=None
    )
    
    # Train models with feature weighting only
    print("\n" + "="*60)
    print("WITH FEATURE WEIGHTING (NO PCA)")
    print("="*60)
    results_weighted, _ = train_and_compare_models(
        X_train_processed, y_train, X_test_processed, y_test, 
        feature_names,
        use_pca=False,
        feature_weights=feature_weights
    )
    
    # Train models with PCA only
    print("\n" + "="*60)
    print("WITH PCA (NO FEATURE WEIGHTING)")
    print("="*60)
    results_pca, _ = train_and_compare_models(
        X_train_processed, y_train, X_test_processed, y_test, 
        feature_names,
        use_pca=True,
        n_components=optimal_n,
        feature_weights=None
    )
    
    # Train models with both PCA and feature weighting
    print("\n" + "="*60)
    print("WITH PCA AND FEATURE WEIGHTING")
    print("="*60)
    results_pca_weighted, _ = train_and_compare_models(
        X_train_processed, y_train, X_test_processed, y_test, 
        feature_names,
        use_pca=True,
        n_components=optimal_n,
        feature_weights=feature_weights
    )
    
    # Final comparison
    print("\n" + "="*60)
    print("FINAL COMPARISON - ALL CONFIGURATIONS")
    print("="*60)
    
    all_results = {}
    for model in results_baseline.keys():
        all_results[f"{model}_baseline"] = results_baseline[model]
        all_results[f"{model}_weighted"] = results_weighted[model]
        all_results[f"{model}_pca"] = results_pca[model]
        all_results[f"{model}_pca_weighted"] = results_pca_weighted[model]
    
    final_comparison = pd.DataFrame(all_results).T
    final_comparison = final_comparison.sort_values('RMSE')
    
    print("\nAll Models Ranked by RMSE:")
    print(final_comparison.to_string())
    
    print("\n" + "="*60)
    print("BEST OVERALL MODEL:")
    best_config = final_comparison.index[0]
    print(f"{best_config.upper()}")
    print(f"RMSE: {final_comparison.loc[best_config, 'RMSE']:.4f}")
    print(f"MAE: {final_comparison.loc[best_config, 'MAE']:.4f}")
    print(f"R2: {final_comparison.loc[best_config, 'R2']:.4f}")
    print("="*60)

if __name__ == "__main__":
    main()
