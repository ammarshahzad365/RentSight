import os
import json
import matplotlib.pyplot as plt

# Directory containing the sanitized listings
listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def visualize_locations():
    """Visualize listing locations on a 2D plot."""
    latitudes = []
    longitudes = []
    missing_location_count = 0
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            location = data.get('location')
            if location and isinstance(location, dict):
                lat = location.get('lat')
                lng = location.get('lng')
                if lat is not None and lng is not None:
                    latitudes.append(lat)
                    longitudes.append(lng)
                else:
                    missing_location_count += 1
            else:
                missing_location_count += 1
        
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.scatter(longitudes, latitudes, alpha=0.6, c='blue', edgecolors='darkblue', s=50)
    
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.title(f'Airbnb Listing Locations\n({len(latitudes)} listings plotted, {missing_location_count} without location)', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add some statistics as text on the plot
    if latitudes and longitudes:
        stats_text = f'Lat Range: {min(latitudes):.3f} to {max(latitudes):.3f}\n'
        stats_text += f'Lng Range: {min(longitudes):.3f} to {max(longitudes):.3f}'
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save the plot
    output_file = os.path.join(os.path.dirname(__file__), 'locations_plot.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {output_file}")
    
    # Show the plot
    plt.show()
    
    print(f"\nSummary:")
    print(f"  Total listings plotted: {len(latitudes)}")
    print(f"  Listings without location: {missing_location_count}")

if __name__ == "__main__":
    visualize_locations()