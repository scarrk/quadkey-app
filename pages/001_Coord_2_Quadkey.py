# ########################################################################## #
# Identification Division

# ########################################################################## #
# Packages
import streamlit as st
import mercantile
import folium
from streamlit_folium import st_folium

# ########################################################################## #
# inline function
# ########################################################################## #

# Function to calculate the centroid of a quadkey
def quadkey_to_lat_lon(quadkey):
    # Convert quadkey to tile
    tile = mercantile.quadkey_to_tile(quadkey)
    # Get the bounding box of the tile
    bounds = mercantile.bounds(tile)
    # Calculate the center of the tile
    lat = (bounds.north + bounds.south) / 2
    lon = (bounds.east + bounds.west) / 2
    return lat, lon
    

# Function to convert a quadkey to a polygon
def quadkey_to_polygon(quadkey):
    # Convert quadkey to tile coordinates
    tile = mercantile.quadkey_to_tile(quadkey)
    # Get bounding box for the tile
    bounds = mercantile.bounds(tile)
    # Create a polygon from the bounding box
    return Polygon([
        (bounds.west, bounds.south),  # Bottom left
        (bounds.west, bounds.north),  # Top left
        (bounds.east, bounds.north),  # Top right
        (bounds.east, bounds.south),  # Bottom right
        (bounds.west, bounds.south)   # Close polygon
    ])

def latlng_to_quadkey(lat, lng, zoom):
    # Get the tile (x, y, z) from the latitude, longitude, and zoom
    tile = mercantile.tile(lng, lat, zoom)
    
    # Convert the tile to a quadkey
    quadkey = mercantile.quadkey(tile)
    
    return quadkey

# Function to get bounding box from quadkey
def quadkey_to_bbox(quadkey):
    tile = mercantile.quadkey_to_tile(quadkey)
    bbox = mercantile.bounds(tile)
    return bbox, tile

# ########################################################################## #
# Procedure Section
# ########################################################################## #


# Check session state
if "lat" not in st.session_state:
    st.session_state.lat = "51.50076556292535"
if "lng" not in st.session_state:
    st.session_state.lng = "-0.12461246544526973"
if "zoom" not in st.session_state:
    st.session_state.zoom = 17


st.header('Co-ordinates to Quadkeys')

lat = st.text_input('Latitude:', st.session_state.lat) 
lng = st.text_input('Longitude:', st.session_state.lng)
zoom = st.slider('Zoom Level', 14, 19, int(st.session_state.zoom) )
quadkey = latlng_to_quadkey( float(lat), float(lng), zoom)

if st.button('Submit'):
    if ( (float(lat) >= -90) and (float(lat) <= 90) ):
        st.session_state.lat = lat
    else:
        st.write("Invalid latitude value")
    
    if ( (float(lng) >= -180) and (float(lng) <= 180) ):
        st.session_state.lng = lng
    else:
        st.write("Invalid longitude value")

    quadkey = latlng_to_quadkey( float(lat), float(lng) , zoom )

# Show map of the location with a bounding box plotted on it
bbox, tile = quadkey_to_bbox(quadkey)

# Display the bounding box
st.write(f"Quadkey: {quadkey}")
#st.write(f"Tile (X, Y, Z): {tile}")
#st.write(f"Bounding Box: {bbox}")

# Create a Folium map centered on the bounding box
m = folium.Map(location=[(bbox.south + bbox.north) / 2, (bbox.west + bbox.east) / 2], zoom_start=tile.z + 1)

# Add bounding box to map
folium.Rectangle(
    bounds=[[bbox.south, bbox.west], [bbox.north, bbox.east]],
    color="blue",
    fill=True,
    fill_opacity=0.2
).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)