from flask import Flask, jsonify, request
import pandas as pd
import geojson
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1"]}})

# Load data from CSV
df = pd.read_csv('Mobile_Food_Facility_Permit.csv')

@app.route('/api/foodtrucks', methods=['GET'])
def get_foodtrucks():
    # Filter by query parameters (example: cuisine, location)
    cuisine = request.args.get('cuisine')
    location = request.args.get('location')  # Could be lat/long pair
    
    # Filter dataframe based on query params
    filtered_df = df.copy()
    
    if cuisine:
        filtered_df = filtered_df[filtered_df['FoodItems'].str.contains(cuisine)]
    
    # For location, perform spatial filtering (not shown here due to complexity)

    # Convert DataFrame to GeoJSON FeatureCollection
    features = [geojson.Feature(geometry=geojson.Point((row['Longitude'], row['Latitude'])), properties=row.to_dict()) for _, row in filtered_df.iterrows()]
    feature_collection = geojson.FeatureCollection(features)

    return jsonify(feature_collection)

if __name__ == '__main__':
    app.run(debug=True)