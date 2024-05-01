from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx
import pandas as pd
from shapely.geometry import Point
import geohash2

app = Flask(__name__)

# Load the graph
G_drive = ox.load_graphml('https://drive.google.com/file/d/1pJuEUv-mt6Azw8iks7lYsoIqEwASfdCb/view?usp=drive_link')

# Prepare NO2 data and integrate into the graph
def prepare_no2_data():
    # Load your NO2 data here
    no2_data = pd.read_csv('https://drive.google.com/file/d/1HWzKV2f1nXtcTsfjwK37Cac-b60ykZaY/view?usp=drive_link')
    no2_data['geohash'] = no2_data.apply(lambda row: geohash2.encode(row.latitude, row.longitude, precision=7), axis=1)
    # Convert to DataFrame and set CRS (assuming you have latitude and longitude columns)
    return no2_data

@app.route('/route', methods=['GET'])
def calculate_route():
    lat_start = float(request.args.get('lat_start'))
    lon_start = float(request.args.get('lon_start'))
    lat_end = float(request.args.get('lat_end'))
    lon_end = float(request.args.get('lon_end'))

    orig_node = ox.get_nearest_node(G_drive, (lat_start, lon_start))
    dest_node = ox.get_nearest_node(G_drive, (lat_end, lon_end))

    route = ox.shortest_path(G_drive, orig_node, dest_node, weight='weight')
    route_coords = ox.utils_graph.node_list_to_coordinate_lines(G_drive, route)
    return jsonify(route_coords)

if __name__ == "__main__":
    app.run(debug=True)
