import os
"""
ETL Service
This module provides a Flask-based web service for performing ETL (Extract, Transform, Load) operations on user data.
It includes endpoints for health checks, file uploads, ETL processing, displaying rows, and deleting all data.
Modules:
    os: Provides a way of using operating system dependent functionality.
    re: Provides regular expression matching operations.
    logging: Provides a way to configure and use loggers.
    psycopg2: Provides a PostgreSQL database adapter for Python.
    pandas: Provides data structures and data analysis tools.
    flask: Provides a micro web framework for Python.
    werkzeug.utils: Provides utility functions for Flask.
    flask_httpauth: Provides HTTP authentication for Flask.
Configuration:
    UPLOAD_FOLDER: Directory where uploaded files are saved.
    db_role_configs: Dictionary containing database configurations for different roles (analyst, manager, admin).
Endpoints:
    /health (GET): Performs a health check on the service and database connection.
    /test-upload (POST): Tests file upload functionality.
    /etl (POST): Performs ETL operations on uploaded files. Requires authentication.
    /display-rows (GET): Displays rows from the database. Requires authentication.
    /delete-all (DELETE): Deletes all data from the database. Requires authentication.
Functions:
    verify_password(username, password): Verifies the provided username and password against environment variables.
    health_check(): Performs a health check on the service and database connection.
    test_upload(): Tests file upload functionality.
    etl(): Performs ETL operations on uploaded files.
    display_rows(): Displays rows from the database.
    delete_all(): Deletes all data from the database.
Usage:
    Run the module as a standalone script to start the Flask web service.
"""
import re
import logging
import psycopg2
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth

# Setting up Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
auth = HTTPBasicAuth()

# Logger for errors
logging.basicConfig(filename='error.log', level=logging.ERROR)
logger = logging.getLogger()

# Database configurations
db_role_configs = {
    'analyst': {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('ANALYST_DB_USER'),
        'password': os.environ.get('ANALYST_DB_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST')
    },
    'manager': {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('MANAGER_DB_USER'),
        'password': os.environ.get('MANAGER_DB_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST')
    },
    'admin': {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('ADMIN_DB_USER'),
        'password': os.environ.get('ADMIN_DB_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST')
    }
}

# Authentication
@auth.verify_password
def verify_password(username, password):
    if username == os.environ.get('AUTH_USERNAME') and password == os.environ.get('AUTH_PASSWORD'):
        return username

@app.route('/health', methods=['GET'])
def health_check():
    """
    Perform a health check on the service.

    This function checks the health of the service by attempting to connect to the database
    using the configuration specified for the role provided in the request arguments. If no
    role is specified, it defaults to 'analyst'. It returns a JSON response indicating the
    health status of the service and the database connection status.

    Returns:
        Response: A Flask JSON response with the health status and HTTP status code.
            - If the health check is successful:
                {
                    "status": "healthy",
                    "database": "connected"
                }, 200
            - If the health check fails:
                {
                    "status": "unhealthy",
                    "database": "disconnected",
                    "error": str(e)
                }, 500

    Raises:
        Exception: If there is an error during the health check process, it is logged and
                   included in the response.
    """
    try:
        role = request.args.get('role', 'analyst')  # Default to analyst if no role specified
        db_config = db_role_configs[role]

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
    """
    Handles file upload from a request.

    This function checks if a file is included in the request and if a file is selected.
    It returns appropriate messages and HTTP status codes based on the presence and selection of the file.

    Returns:
        tuple: A message indicating the status of the file upload and an HTTP status code.
    """
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    return f"File received: {file.filename}", 200

@app.route('/etl', methods=['POST'])
@auth.login_required
def etl():
    """
    ETL Service Module
    This module provides an ETL (Extract, Transform, Load) service endpoint for processing and validating uploaded files,
    and inserting the validated data into a PostgreSQL database.
    Routes:
        /etl (POST): Endpoint to handle ETL process.
    Functions:
        etl(): Handles the ETL process including file upload, validation, and database insertion.
    Decorators:
        @app.route('/etl', methods=['POST']): Defines the route and HTTP method for the ETL service.
        @auth.login_required: Ensures that the endpoint is accessible only to authenticated users.
    ETL Process:
        1. Extract: Receives a file upload (Excel or CSV) and reads it into a pandas DataFrame.
        2. Transform: Validates the data for required columns, formats, and patterns.
        3. Load: Inserts the validated data into the PostgreSQL database.
    Error Handling:
        - Returns appropriate HTTP status codes and error messages for various failure scenarios such as:
            - Database authentication failure
            - Missing or unsupported file
            - Data validation errors
            - File read errors
            - Database insertion errors
    Logging:
        - Logs errors and important events for debugging and monitoring purposes.
    """
    role = request.form.get('role', 'analyst')  # Default to analyst if no role specified
    db_config = db_role_configs[role]
    
    try:
        conn = psycopg2.connect(**db_config)
        conn.close()
    except Exception as e:
        logger.error(f"Database authentication failed: {str(e)}")
        return f"Database authentication failed: {str(e)}", 401

    if 'file' not in request.files:
        return "No file part in the request.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400

    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        return "Unsupported file type. Please upload an Excel or CSV file.", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        df = pd.read_excel(file_path) if file.filename.endswith('.xlsx') else pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"ETL process failed during file load: {str(e)}")
        return jsonify({"error": str(e)}), 500

    try:
        expected_columns = {'id', 'first_name', 'last_name', 'email', 'gender', 'ip_address'}
        actual_columns = set(df.columns)

        if actual_columns != expected_columns:
            missing_columns = expected_columns - actual_columns
            extra_columns = actual_columns - expected_columns
            error_message = f"Data validation error. Missing columns: {missing_columns}. Extra columns: {extra_columns}."
            logger.error(error_message)
            return jsonify({"error": error_message}), 400

        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df['email'] = df['email'].str.lower()

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

        df.drop(index=invalid_rows, inplace=True)

    except Exception as e:
        logger.error(f"ETL process failed during data processing: {str(e)}")
        return jsonify({"error": str(e)}), 500

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO users (id, first_name, last_name, email, gender, ip_address) VALUES (%s, %s, %s, %s, %s, %s)",
                tuple(row)
            )
        conn.commit()
        cursor.close()
        conn.close()

        return "ETL process completed successfully.", 200

    except Exception as e:
        logger.error(f"ETL process failed while writing to database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/display-rows', methods=['GET'])
@auth.login_required
def display_rows():
    """
    Fetches and displays rows from the database based on the user's role.
    This function connects to a PostgreSQL database using role-specific configurations,
    executes a query to fetch rows from either the 'masked_users' or 'users' table,
    and returns the results as a JSON response.
    The role is determined from the request arguments, defaulting to 'analyst' if not specified.
    - 'analyst': Fetches rows from the 'masked_users' table.
    - 'manager' or 'admin': Fetches rows from the 'users' table.
    Returns:
        tuple: A JSON response containing the fetched rows and an HTTP status code.
               On success, returns a list of dictionaries representing the rows and a 200 status code.
               On failure, returns an error message and a 500 status code.
    Raises:
        Exception: If any error occurs during database connection, query execution, or data fetching.
    Logs:
        Logs an error message if any exception is raised during the process.
    """
    try:
        role = request.args.get('role', 'analyst')  # Default to analyst if no role specified
        db_config = db_role_configs[role]
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        if role == 'analyst':
            cursor.execute("SELECT * FROM masked_users LIMIT 5")
        elif role in ['manager', 'admin']:
            cursor.execute("SELECT * FROM users LIMIT 5")
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(zip(columns, row)) for row in rows]), 200
    except Exception as e:
        logger.error(f"Display Rows Failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-all', methods=['DELETE'])
@auth.login_required
def delete_all():
    """
    Deletes all data from the 'users' table in the database.

    This function attempts to connect to the database using the role specified
    in the request form. If no role is specified, it defaults to 'analyst'.
    Upon successful connection, it deletes all records from the 'users' table.

    Returns:
        tuple: A message indicating the result of the operation and an HTTP status code.
            - ("All data deleted successfully.", 200) if the operation is successful.
            - ("Database authentication failed: {error_message}", 401) if database authentication fails.
            - ("Failed to delete data: {error_message}", 500) if the deletion operation fails.

    Raises:
        Exception: If there is an error during database connection or data deletion.
    """
    try:
        role = request.form.get('role', 'analyst')  # Default to analyst if no role specified
        db_config = db_role_configs[role]
        conn = psycopg2.connect(**db_config)
    except Exception as e:
        logger.error(f"Database authentication failed: {str(e)}")
        return f"Database authentication failed: {str(e)}", 401
    try:
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