# BPC Project: Data Engineering and ML Model Deployment

This repository contains the deliverables for the BPC Project, which includes database configuration, ETL process, ML model deployment, and a data engineering management plan.

## Project Structure

- `/etl`: ETL process and database configuration
- `/ml_server`: ML model deployment
- `Sean Tauber - BPC Project Deck.pdf`: Data Engineering Management plan

## Section 1: Database Configuration & Python ETL

The `/etl` directory contains the code and documentation for the database configuration and ETL process. Please refer to the [ETL README](/etl/README.md) for detailed information on:

- Database provisioning
- Python ETL script
- Data transformation process
- Reproducible setup instructions (using Docker Compose)

## Section 2: ML Model Deployment

The `/ml_server` directory contains the code and documentation for deploying an ML model as an API endpoint. Please refer to the [ML Server README](/ml_server/README.md) for detailed information on:

- Model selection (e.g., MNIST or Fashion MNIST)
- Deployment environment (cloud provider or local setup)
- API endpoint implementation
- Reproducible deployment instructions
- Usage documentation

## Section 3: Data Engineering Management

The file `Sean Tauber - BPC Project Deck.pdf` in the root directory contains the work plan for implementing ChemBERTa in BPC's workflow. This deck includes:

- Executive summary of the proposed approach
- Modular implementation plan
- Required skill sets
- Deliverables and milestones
- Cost estimates and resource allocation
- Architectural diagrams
- Project timeline (Gantt chart)

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/your-username/bpc-project.git
   cd bpc-project
   ```

2. Follow the instructions in the [ETL README](/etl/README.md) to set up and run the ETL process.

3. Follow the instructions in the [ML Server README](/ml_server/README.md) to deploy and use the ML model API.

4. Review the `Sean Tauber - BPC Project Deck.pdf` for the data engineering management plan.

## Additional Notes

- Ensure you have the necessary prerequisites installed (Docker, Docker Compose, Git, etc.) as specified in each section's README.
- For any questions or issues, please open an issue in this repository or contact the project maintainer.
