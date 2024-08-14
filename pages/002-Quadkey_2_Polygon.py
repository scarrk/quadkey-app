# ########################################################################## #
# Identification Division

# ########################################################################## #
# Packages
import streamlit as st
import mercantile
import folium
from streamlit_folium import st_folium

QUADKEY_ID_BIGBEN = "03131313113010210"


# ########################################################################## #
# inline function
# ########################################################################## #

# Function to convert a quadkey to a polygon
def quadkey_to_polygon(quadkey):
    # Convert quadkey to tile coordinates
    tile = mercantile.quadkey_to_tile(quadkey)
    # Get bounding box for the tile
    bounds = mercantile.bounds(tile)
    # Create a polygon from the bounding box
    return "Polygon("+ \
        str(bounds.west)+" "+str(bounds.south) +", "+ \
        str(bounds.west)+" "+str(bounds.north) +", "+ \
        str(bounds.east)+" "+str(bounds.north) +", "+ \
        str(bounds.east)+" "+str(bounds.south) +", "+ \
        str(bounds.west)+" "+str(bounds.south) +")"  
 
 # Function to get bounding box from quadkey
def quadkey_to_bbox(quadkey):
    tile = mercantile.quadkey_to_tile(quadkey)
    bbox = mercantile.bounds(tile)
    return bbox, tile   


# ########################################################################## #
# Procedure Section
# ########################################################################## #

# Check Session State
if "quadkey" not in st.session_state:
    st.session_state.quadkey = QUADKEY_ID_BIGBEN


st.header("Quadkey to Polygon")
quadkey = st.text_input("Enter quadkey ID:", QUADKEY_ID_BIGBEN)

if st.button('Submit'):
    # Check input is valid input (0-3 digit)
    st.session_state.quadkey = quadkey
    
polygon=quadkey_to_polygon(quadkey)

# Show map of the location with a bounding box plotted on it
bbox, tile = quadkey_to_bbox(quadkey)

# Display the bounding box
st.write(f"Quadkey: {quadkey}")
st.write(f"Zoom: {len(quadkey)}")
st.write(f"Geometry: {polygon}")

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