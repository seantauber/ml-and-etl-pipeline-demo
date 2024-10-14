# ETL Service with Role-Based Access Control

## Project Overview

This project demonstrates an Extract, Transform, Load (ETL) service implemented with Python, Flask, and PostgreSQL. It showcases best practices in data handling, security, and role-based access control (RBAC) in a containerized environment using Docker.

## Quick Start Guide

Follow these steps to quickly set up and run the project:

### Prerequisites
- Docker and Docker Compose
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/seantauber/ml-and-etl-pipeline-demo.git
cd etl-service
```

### Step 2: Set Up Environment Variables
```bash
cp .env.sample .env
```

Edit the `.env` file and fill in the necessary values:
```
POSTGRES_HOST=<postgres_host>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_DB=<database_name>

ANALYST_DB_USER=<analyst_username>
ANALYST_DB_PASSWORD=<analyst_password>

MANAGER_DB_USER=<manager_username>
MANAGER_DB_PASSWORD=<manager_password>

ADMIN_DB_USER=<admin_username>
ADMIN_DB_PASSWORD=<admin_password>

ENCRYPTION_KEY=<your_encryption_key>

AUTH_USERNAME=<api_username>
AUTH_PASSWORD=<api_password>
```

### Step 3: Build and Start the Services
```bash
docker-compose up --build -d
```

### Step 4: Run the Test Script
```bash
chmod +x scripts/run_demo.sh
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

## Key Features

- ETL process for handling user data
- Role-based access control (RBAC) for data visibility
- Dockerized application and database services
- Secure API endpoints with authentication

## Architecture

The project consists of two main components:

1. **ETL Service (Flask Application):**
   - Handles data ingestion, transformation, and loading
   - Implements API endpoints for data operations
   - Manages role-based access to data

2. **PostgreSQL Database:**
   - Stores user data
   - Implements database-level access control

## Best Practices and Security Measures

### 1. Data Management Best Practices

#### a. Data Validation and Cleansing
- Input data is validated for correct format and structure before processing.
- Regular expressions are used to ensure data integrity (e.g., valid email formats, IP addresses).
- Invalid data rows are logged and excluded from the ETL process to maintain data quality.

#### b. Data Transformation
- Consistent data formatting is applied (e.g., email addresses are converted to lowercase).
- Data is stripped of leading and trailing whitespaces to ensure consistency.

#### c. Error Handling and Logging
- Comprehensive error handling is implemented throughout the ETL process.
- Errors are logged with detailed information for troubleshooting and auditing purposes.

#### d. Modular Code Structure
- The ETL process is divided into distinct functions for extraction, transformation, and loading.
- This modular approach enhances maintainability and allows for easier testing and updates.

### 2. Security Measures

#### a. Role-Based Access Control (RBAC)
- Three roles implemented: Analyst, Manager, and Admin.
- Each role has different levels of data access:
  - Analyst: Can view masked data only
  - Manager: Can view partially unmasked data
  - Admin: Has full access to unmasked data
- Role-based access is enforced at both the application and database levels.

#### b. Database-Level Security
- User authentication and authorization implemented at the database level.
- Different database users created for each role with appropriate permissions:
  - Analyst: Read-only access to specific views with masked data
  - Manager: Read access to tables with some sensitive fields masked
  - Admin: Full read/write access to all tables
- Database connections use SSL/TLS encryption for data in transit.
- Regular security patches and updates are applied to the database system.

#### c. API Security
- All endpoints are protected with HTTP Basic Authentication.
- HTTPS is used for all API communications to encrypt data in transit.
- Input validation is performed on all API requests to prevent injection attacks.
- Rate limiting is implemented to prevent abuse and DoS attacks.
- Sensitive operations (e.g., data deletion) are restricted to admin roles.

#### d. Environment Variable Usage
- Sensitive information like database credentials are managed via environment variables.
- This practice prevents hardcoding of sensitive data in the codebase.

#### e. Containerization
- The application and database are containerized using Docker.
- Containerization ensures consistency across different environments and simplifies deployment.
- Container images are regularly updated and scanned for vulnerabilities.

#### f. Principle of Least Privilege
- Each component and user role is granted only the minimum level of access required to perform its function.
- This minimizes the potential impact of a security breach.

### 3. Monitoring and Auditing
- All data access and modifications are logged for auditing purposes.
- Regular monitoring of system logs and API usage patterns to detect unusual activities.
- Automated alerts are set up for potential security incidents or system anomalies.

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