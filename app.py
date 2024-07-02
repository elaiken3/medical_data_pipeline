from flask import Flask, jsonify, request
import psycopg2
import pandas as pd
import logging
from data_cleaner import is_taking_alpha_blockers, 



# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database connection parameters
DB_NAME = "medical_records"
DB_USER = "postgres"
DB_PASS = "password1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_person_data(person_id, table_name):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        query = f"SELECT * FROM {table_name} WHERE person_id = %s"
        df = pd.read_sql_query(query, conn, params=(person_id,))
        conn.close()
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error fetching data from table {table_name} for person_id {person_id}: {e}")
        raise

@app.route('/person/<int:person_id>', methods=['GET'])
def get_person(person_id):
    try:
        data = {
            "person_id": person_id,
            "data": {
                "lifestyle": get_person_data(person_id, 'lifestyle'),
                "rx": get_person_data(person_id, 'rx'),
                "conditions": get_person_data(person_id, 'conditions'),
                "labs": get_person_data(person_id, 'labs'),
                "tests": get_person_data(person_id, 'tests')
            }
        }
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in fetching data for person_id {person_id}: {e}")
        return jsonify({"error": "Data fetch error"}), 500

@app.route('/person/<int:person_id>/features', methods=['GET'])
def get_person_features(person_id):
    try:
        # Assuming features are calculated and stored in the respective tables
        labs_data = pd.DataFrame(get_person_data(person_id, 'labs'))
        rx_data = pd.DataFrame(get_person_data(person_id, 'rx'))

        features = {
            "taking_alpha_blockers": is_taking_alpha_blockers(rx_data),
            "most_recent_hgb": get_most_recent_hgb(labs_data),
            "most_recent_a1c": get_most_recent_a1c(labs_data),
            "high_cholesterol_events": get_high_cholesterol_events(labs_data)
        }

        return jsonify({"person_id": person_id, "data": features})
    except Exception as e:
        logger.error(f"Error in fetching features for person_id {person_id}: {e}")
        return jsonify({"error": "Feature fetch error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
