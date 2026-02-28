"""Generate confusion matrices for trained models."""
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from data_loader import load_listings_from_json
from preprocess import DataPreprocessor, create_train_test_split

def bin_occupancy_rates(rates):
    """Bin occupancy rates into categories for confusion matrix."""
    bins = [0, 40, 60, 80, 100]
    labels = ['Low (0-40%)', 'Medium (40-60%)', 'High (60-80%)', 'Very High (80-100%)']
    return pd.cut(rates, bins=bins, labels=labels, include_lowest=True)

def plot_confusion_matrix(y_test, y_pred, model_name, save_path=None):
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
    
    # Plot heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Count'}, linewidths=1, linecolor='gray')
    
    # Add percentage annotations
    for i in range(len(labels)):
        for j in range(len(labels)):
            if not np.isnan(cm_percent[i, j]):
                plt.text(j + 0.5, i + 0.7, f'({cm_percent[i, j]:.1f}%)',
                        ha='center', va='center', fontsize=9, color='gray', weight='bold')
    
    plt.title(f'Confusion Matrix - {model_name}', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Actual Occupancy Category', fontsize=13, fontweight='bold')
    plt.xlabel('Predicted Occupancy Category', fontsize=13, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    # Calculate and print accuracy
    accuracy = np.trace(cm) / np.sum(cm) * 100
    print(f"  Category Classification Accuracy: {accuracy:.2f}%")
    print(f"  Total samples: {np.sum(cm)}")
    print(f"  Correctly classified: {np.trace(cm)}")
    
    return accuracy, cm

def main():
    """Generate confusion matrices for all trained models."""
    print("="*60)
    print("GENERATING CONFUSION MATRICES")
    print("="*60)
    
    # Load and preprocess data
    print("\nLoading data...")
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
    
    print(f"Test set size: {len(y_test)} samples")
    
    # Check for trained models
    models_dir = 'models'
    model_files = {
        'Random Forest': 'occupancy_model.pkl',
        'Neural Network': 'occupancy_model.keras'
    }
    
    os.makedirs(models_dir, exist_ok=True)
    
    results = []
    
    for model_name, model_file in model_files.items():
        model_path = os.path.join(models_dir, model_file)
        
        if not os.path.exists(model_path):
            print(f"\n⚠ {model_name} model not found at {model_path}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {model_name}")
        print(f"{'='*60}")
        
        try:
            # Load model
            if model_file.endswith('.pkl'):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                y_pred = model.predict(X_test_processed)
            else:  # Keras model
                from tensorflow import keras
                model = keras.models.load_model(model_path)
                y_pred = model.predict(X_test_processed, verbose=0).flatten()
            
            # Generate confusion matrix
            save_path = os.path.join(models_dir, f'confusion_matrix_{model_name.replace(" ", "_").lower()}.png')
            accuracy, cm = plot_confusion_matrix(y_test, y_pred, model_name, save_path)
            
            results.append({
                'Model': model_name,
                'Category_Accuracy': accuracy,
                'Total_Samples': np.sum(cm),
                'Correct': np.trace(cm)
            })
            
        except Exception as e:
            print(f"✗ Error processing {model_name}: {str(e)}")
    
    # Summary
    if results:
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))
        print(f"\nAll confusion matrices saved in {os.path.abspath(models_dir)}/")
    else:
        print("\n⚠ No trained models found. Please train models first using train_model.py")

if __name__ == "__main__":
    main()
