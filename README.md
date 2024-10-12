# Secure ETL Service with Role-Based Access Control

## Project Overview

This project demonstrates a secure Extract, Transform, Load (ETL) service implemented with Python, Flask, and PostgreSQL. It showcases best practices in data handling, encryption, and role-based access control (RBAC) in a containerized environment using Docker.

## Key Features

- ETL process for handling user data
- Role-based access control (RBAC) for data visibility
- Data encryption at rest
- Dockerized application and database services
- Secure API endpoints with authentication

## Architecture

The project consists of two main components:

1. **ETL Service (Flask Application):**
   - Handles data ingestion, transformation, and loading
   - Implements API endpoints for data operations
   - Manages role-based access to data

2. **PostgreSQL Database:**
   - Stores encrypted user data
   - Implements database-level access control

## Security Considerations

### 1. Data Encryption
- All sensitive data is encrypted before storage using Fernet symmetric encryption.
- Encryption key is securely managed and not stored in the codebase.

### 2. Role-Based Access Control (RBAC)
- Three roles implemented: Analyst, Manager, and Admin.
- Each role has different levels of data access:
  - Analyst: Can view masked data only
  - Manager: Can view partially unmasked data
  - Admin: Has full access to unmasked data

### 3. Database-Level Security
- User authentication and authorization implemented at the database level.
- Different database users created for each role with appropriate permissions.

### 4. API Security
- All endpoints are protected with HTTP Basic Authentication.
- Sensitive operations (e.g., data deletion) restricted to admin roles.

### 5. Environment Variable Usage
- Sensitive information like database credentials and encryption keys are managed via environment variables.

## Setup and Running the Demo

Follow these steps to set up and run the project locally:

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/secure-etl-service.git
cd secure-etl-service
```

### Step 2: Set Up Environment Variables
1. Copy the sample `.env` file:
   ```bash
   cp .env.sample .env
   ```
2. Edit the `.env` file and fill in the necessary values:
   ```
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_db_name
   ANALYST_DB_USER=analyst_user
   ANALYST_DB_PASSWORD=analyst_password
   MANAGER_DB_USER=manager_user
   MANAGER_DB_PASSWORD=manager_password
   ADMIN_DB_USER=admin_user
   ADMIN_DB_PASSWORD=admin_password
   AUTH_USERNAME=your_api_username
   AUTH_PASSWORD=your_api_password
   ENCRYPTION_KEY=
   ```

### Step 3: Generate Encryption Key
1. Run the encryption key generation script:
   ```bash
   python scripts/generate_encryption_key.py
   ```
2. Copy the generated key and add it to your `.env` file:
   ```
   ENCRYPTION_KEY=your_generated_key
   ```

### Step 4: Set Script Permissions
Ensure that the scripts are executable:
```bash
chmod +x scripts/*.sh
```

### Step 5: Build and Start the Services
```bash
docker-compose up --build -d
```

### Step 6: Run the Demo Script
```bash
./scripts/run_demo.sh
```

This script will:
1. Test the health of the services
2. Demonstrate data access for different roles
3. Perform an ETL operation
4. Show the results of the ETL process
5. Clean up the data

## Understanding the Output

The demo script will show:
- Different data visibility for Analyst, Manager, and Admin roles
- The process of data ingestion and transformation
- How data is securely stored and accessed

## Extending the Project

To extend this project:
1. **Add More Complex ETL Operations in `etl_service.py`**
    - Implement additional data transformation steps such as data normalization, aggregation, and enrichment.
    - Introduce error handling and logging for each step of the ETL process to ensure data integrity and traceability.
    - Optimize the ETL pipeline for performance by using batch processing and parallel execution where applicable.

2. **Implement Additional API Endpoints for Different Data Operations**
    - Create endpoints for advanced data queries, such as filtering, sorting, and pagination.
    - Add endpoints for data export in various formats (e.g., CSV, JSON) to facilitate data sharing and analysis.
    - Implement endpoints for data validation and cleansing to ensure data quality before ingestion.

3. **Enhance the RBAC System with More Granular Permissions**
    - Define additional roles with specific permissions tailored to different user needs (e.g., Read-Only, Data Scientist, Auditor).
    - Implement field-level security to control access to specific data attributes based on user roles.
    - Introduce dynamic permission management to allow administrators to update roles and permissions without redeploying the application.

4. **Use a Proper Vault for Encryption Key Storage**
    - Integrate a dedicated secrets management service like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault for secure encryption key storage.
    - Configure the vault service to provide fine-grained access control and auditing capabilities for sensitive information.
    - Modify the application to fetch the encryption key from the vault at runtime, ensuring that keys are never hardcoded or exposed in the codebase.
- Instead of storing encryption keys in environment variables, use a dedicated secrets management service like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault.
- These services provide secure storage, access control, and auditing capabilities for sensitive information.
- Integrate the vault service with your application to fetch the encryption key at runtime, ensuring that keys are never hardcoded or exposed in the codebase.

### 5. Add Comprehensive Logging and Monitoring
- Implement logging for all critical operations, including data ingestion, transformation, and access events.
- Use a centralized logging system like ELK Stack (Elasticsearch, Logstash, Kibana) or a cloud-based solution like AWS CloudWatch or Azure Monitor.
- Set up monitoring and alerting for key metrics such as API request rates, error rates, and system performance.
- Ensure that logs are securely stored and access-controlled to prevent unauthorized access to sensitive information.
- Regularly review logs and monitoring data to detect and respond to potential security incidents promptly.

## Conclusion

This project demonstrates a secure approach to handling sensitive data in an ETL process, implementing key security practices like encryption, RBAC, and secure API design. It serves as a foundation for building more complex, secure data processing systems.