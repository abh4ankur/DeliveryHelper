import googlemaps
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np 
import pandas as pd
import os 
import requests 

INPUT_EXCEL_SHEET= "Address.xlsx"
API_KEY = "YOUR_API_KEY"

gmaps = googlemaps.Client(key=API_KEY)

# Function to get address from latitude and longitude
# It returns multiple addresses so picking up index 1 address, this might not be accurate like GPS
# but it would give fair idea on location coords from other addresses
def get_address(lat, lng):
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    if reverse_geocode_result:
        return reverse_geocode_result[1]['formatted_address']
    else:
        return "Address not found"
   

# Function to get lat/long from address
def get_coordinates(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        return None

# Get the current location
def get_current_location():
    try:
        # This URL is used to get the geolocation data
        url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + API_KEY
        response = requests.post(url)
        response.raise_for_status()  # Check for HTTP errors
        location = response.json().get('location')
        if location:
            return get_address(location.get('lat'),location.get('lng'))
        else:
            print("Location data not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None




def plot_addresses(df):
    
    currLoc = get_current_location()
    print(f"Current location: {currLoc}")

    curr_coords = get_coordinates(currLoc)
    if not curr_coords:
        raise ValueError("Invalid curr cords")

    address_coords = []
    invalid_addresses = []
    address_labels = []
    
    for i, row in df.iterrows():
       
        name = row['Name']
        address = row['Address']
        
        coords = get_coordinates(address)
        if coords:
            address_coords.append(coords)
            distance = geodesic(curr_coords, coords).miles
            # Appending only Name of person , address and distance in miles from current location.
            # Can be enhanced to add more data in labels which would be shown when we hover over them
            address_labels.append(f"{name}\n{address}\nDistance: {distance:.2f} miles")
        else:
            print(f"Wrong address {address} found for {name}")
            invalid_addresses.append(address)

    fig, ax = plt.subplots(figsize=(10, 8))
    #all addresses are shown with blue markers
    scatter = ax.scatter(*zip(*address_coords), c='blue', label='Addresses')
    #current location shown with red marker
    ax.scatter(*curr_coords, c='red', label='Current Address', marker='x')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title('Addresses Cluster')
    ax.legend()

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "\n".join([address_labels[n] for n in ind["ind"]])
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor('lightblue')
        annot.get_bbox_patch().set_alpha(0.8)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

if __name__ == "__main__":
    
    # Load the Excel file
    readFilePath = os.path.join(os.getcwd(),INPUT_EXCEL_SHEET)

    df = pd.read_excel(readFilePath)

    plot_addresses(df)
