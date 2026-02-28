import os
import json
import folium
from folium.plugins import MarkerCluster

# Directory containing the sanitized listings
listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def visualize_locations():
    """Visualize listing locations on an interactive map."""
    locations = []
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
                    # Extract some info for the popup
                    title = data.get('title', 'Untitled')
                    price = data.get('price', 'N/A')
                    url = data.get('url', '#')
                    
                    locations.append({
                        'lat': lat,
                        'lng': lng,
                        'title': title,
                        'price': price,
                        'url': url,
                        'filename': filename
                    })
                else:
                    missing_location_count += 1
            else:
                missing_location_count += 1
        
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
    
    if not locations:
        print("No locations found to display on map!")
        return
    
    # Calculate center of all locations
    center_lat = sum(loc['lat'] for loc in locations) / len(locations)
    center_lng = sum(loc['lng'] for loc in locations) / len(locations)
    
    # Create the map centered on the average location
    map_obj = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add marker cluster for better performance with many markers
    marker_cluster = MarkerCluster().add_to(map_obj)
    
    # Add markers for each listing
    for loc in locations:
        popup_html = f"""
        <div style="width: 200px;">
            <b>{loc['title']}</b><br>
            <b>Price:</b> {loc['price']}<br>
            <a href="{loc['url']}" target="_blank">View Listing</a>
        </div>
        """
        
        folium.Marker(
            location=[loc['lat'], loc['lng']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{loc['title']} - {loc['price']}",
            icon=folium.Icon(color='blue', icon='home', prefix='fa')
        ).add_to(marker_cluster)
    
    # Save the map
    output_file = os.path.join(os.path.dirname(__file__), 'locations_map.html')
    map_obj.save(output_file)
    print(f"\nInteractive map saved to: {output_file}")
    print(f"Open this file in a web browser to view the map.")
    
    print(f"\nSummary:")
    print(f"  Total listings plotted: {len(locations)}")
    print(f"  Listings without location: {missing_location_count}")
    
    # Calculate and display coordinate ranges
    if locations:
        all_lats = [loc['lat'] for loc in locations]
        all_lngs = [loc['lng'] for loc in locations]
        print(f"  Latitude range: {min(all_lats):.4f} to {max(all_lats):.4f}")
        print(f"  Longitude range: {min(all_lngs):.4f} to {max(all_lngs):.4f}")

if __name__ == "__main__":
    visualize_locations()