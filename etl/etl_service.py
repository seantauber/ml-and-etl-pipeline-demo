import os
import re
import logging
import psycopg2
import pandas as pd
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth

# Setting up Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
auth = HTTPBasicAuth()

# Logger for errors
logging.basicConfig(filename='error.log', level=logging.ERROR)
logger = logging.getLogger()

# Load encryption key from environment variable
encryption_key = os.environ.get('ENCRYPTION_KEY')
cipher_suite = Fernet(encryption_key.encode())

# Database connection details
db_config = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST')
}

# Authentication
@auth.verify_password
def verify_password(username, password):
    # In a real application, you should check against secure stored credentials
    # This is a simple example and should be replaced with a secure implementation
    if username == os.environ.get('AUTH_USERNAME') and password == os.environ.get('AUTH_PASSWORD'):
        return username

# Initialize the database table
def initialize_db():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                gender TEXT,
                ip_address TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        print(f"Failed to initialize database: {str(e)}")

# Call the function to initialize the database
initialize_db()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

@app.route('/test-upload', methods=['POST'])
def test_upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    return f"File received: {file.filename}", 200

@app.route('/etl', methods=['POST'])
@auth.login_required
def etl():
    # Check if the request has the file part
    if 'file' not in request.files:
        return "No file part in the request.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400

    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        return "Unsupported file type. Please upload an Excel or CSV file.", 400

    # Save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # Load and clean data
        df = pd.read_excel(file_path) if file.filename.endswith('.xlsx') else pd.read_csv(file_path)

        # Check for expected columns
        expected_columns = {'id', 'first_name', 'last_name', 'email', 'gender', 'ip_address'}
        actual_columns = set(df.columns)

        if actual_columns != expected_columns:
            missing_columns = expected_columns - actual_columns
            extra_columns = actual_columns - expected_columns
            error_message = f"Data validation error. Missing columns: {missing_columns}. Extra columns: {extra_columns}."
            logger.error(error_message)
            return error_message, 400

        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df['email'] = df['email'].str.lower()

        # Validate data
        valid_email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        valid_ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        valid_name_pattern = r'^[A-Za-z]+$'

        invalid_rows = []
        for index, row in df.iterrows():
            valid_row = True
            if not re.match(valid_email_pattern, row['email']):
                logger.error(f"Row ID {row['id']}: Invalid email format")
                valid_row = False
            if not re.match(valid_ip_pattern, row['ip_address']):
                logger.error(f"Row ID {row['id']}: Invalid IP address format")
                valid_row = False
            if not re.match(valid_name_pattern, row['first_name']):
                logger.error(f"Row ID {row['id']}: Invalid first name format")
                valid_row = False
            if not re.match(valid_name_pattern, row['last_name']):
                logger.error(f"Row ID {row['id']}: Invalid last name format")
                valid_row = False

            if not valid_row:
                invalid_rows.append(index)

        # Drop invalid rows
        df.drop(index=invalid_rows, inplace=True)

        # Encrypt and save valid data to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            encrypted_data = [cipher_suite.encrypt(str(value).encode()).decode() for value in row]
            cursor.execute(
                "INSERT INTO users (id, first_name, last_name, email, gender, ip_address) VALUES (%s, %s, %s, %s, %s, %s)",
                encrypted_data
            )
        conn.commit()
        cursor.close()
        conn.close()

        return "ETL process completed successfully.", 200

    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        return f"ETL process failed: {str(e)}", 500

@app.route('/display-rows', methods=['GET'])
@auth.login_required
def display_rows():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Fetch the first 10 rows from the users table
        cursor.execute("SELECT * FROM users LIMIT 10")
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        cursor.close()
        conn.close()
        
        # Decrypt the data
        decrypted_rows = []
        for row in rows:
            decrypted_row = [cipher_suite.decrypt(value.encode()).decode() if value else None for value in row]
            decrypted_rows.append(dict(zip(column_names, decrypted_row)))
        
        return jsonify(decrypted_rows), 200
    except Exception as e:
        logger.error(f"Failed to fetch rows: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-all', methods=['DELETE'])
@auth.login_required
def delete_all():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        cursor.close()
        conn.close()
        return "All data deleted successfully.", 200
    except Exception as e:
        logger.error(f"Failed to delete data: {str(e)}")
        return f"Failed to delete data: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)