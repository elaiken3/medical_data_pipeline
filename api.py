from flask import Flask, jsonify, request
import pandas as pd
import logging
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from sqlalchemy import create_engine
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
jwt = JWTManager(app)

# Database connection parameters
DB_NAME = "medical_records"
DB_USER = "postgres"
DB_PASS = ""  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def get_person_data(person_id, table_name):
    try:
        #Fetch data from each table for a particular person_id
        query = f"SELECT * FROM {table_name} WHERE person_id = {person_id}"
        df = pd.read_sql_query(query, engine)
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error fetching data from table {table_name} for person_id {person_id}: {e}")
        raise

def get_person_features(person_id):
    features = {}
    
    # Fetch and process data from rx table
    rx_data = get_person_data(person_id, 'rx')
    if rx_data:
        df = pd.DataFrame(rx_data)
        features['taking_alpha_blockers'] = bool(df['taking_alpha_blockers'].max())

    # Fetch and process data from labs table
    labs_data = get_person_data(person_id, 'labs')
    if labs_data:
        df = pd.DataFrame(labs_data)
        features['most_recent_hgb'] = float(df['most_recent_hgb'].max())
        features['most_recent_a1c'] = float(df['most_recent_a1c'].max())
        features['high_cholesterol_events'] = int(df['high_cholesterol_events'].max())

    # Fetch and process data from tests table
    tests_data = get_person_data(person_id, 'tests')
    if tests_data:
        df = pd.DataFrame(tests_data)
        features['average_systolic_bp'] = float(df['average_systolic_bp'].max())
        features['average_diastolic_bp'] = float(df['average_diastolic_bp'].max())

    return features

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/person/<int:person_id>', methods=['GET'])
@jwt_required()
def get_person(person_id):
    try:
        data = {
            "person_id": person_id,
            "data": {
                "rx": get_person_data(person_id, 'rx'),
                "labs": get_person_data(person_id, 'labs'),
                "tests": get_person_data(person_id, 'tests')
            }
        }
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in fetching data for person_id {person_id}: {e}")
        return jsonify({"error": "Data fetch error"}), 500

@app.route('/person/<int:person_id>/features', methods=['GET'])
@jwt_required()
def get_person_features_route(person_id):
    try:
        features = get_person_features(person_id)
        return jsonify({"person_id": person_id, "features": features})
    except Exception as e:
        logger.error(f"Error in fetching features for person_id {person_id}: {e}")
        return jsonify({"error": "Feature fetch error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
