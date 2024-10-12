#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to the project root directory
cd "$(dirname "$0")/.." || exit

echo -e "${GREEN}Starting ETL service test...${NC}"

# Step 1: Build and start the services
echo -e "${GREEN}Building and starting Docker services...${NC}"
docker-compose -f docker-compose.yaml down -v # Ensure a clean slate
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d

# Check container status
echo -e "${BLUE}Container Status:${NC}"
docker-compose -f docker-compose.yaml ps

# Check ETL service logs
echo -e "${BLUE}ETL Service Logs:${NC}"
docker-compose -f docker-compose.yaml logs etl

# Wait for services to be ready
# echo -e "${GREEN}Waiting for services to be ready...${NC}"
# sleep 30

# Load environment variables
source .env

# Test health endpoint
echo -e "${BLUE}Testing health endpoint:${NC}"
curl -s http://localhost:5001/health
echo

# Check database content
echo -e "${BLUE}Checking database content:${NC}"
docker-compose -f docker-compose.yaml exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT * FROM users LIMIT 5;"

# Step 2: Test different role accesses
echo -e "${BLUE}Testing Analyst Access:${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=analyst" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

echo -e "${BLUE}Testing Manager Access:${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=manager" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

echo -e "${BLUE}Testing Admin Access:${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=admin" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

# Step 3: Run ETL process
echo -e "${GREEN}Running ETL process...${NC}"
curl -s -X POST "http://localhost:5001/etl" -F "role=admin" -F "file=@rawdata/DEM_Challenge_Section1_DATASET.xlsx" -u "$AUTH_USERNAME:$AUTH_PASSWORD"
echo -e "\n"

# Step 4: Display rows after ETL for each role
echo -e "${BLUE}Displaying rows after ETL (Analyst view):${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=analyst" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

echo -e "${BLUE}Displaying rows after ETL (Manager view):${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=manager" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

echo -e "${BLUE}Displaying rows after ETL (Admin view):${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=admin" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

# Step 5: Delete all data
echo -e "${GREEN}Deleting all data...${NC}"
curl -s -X DELETE "http://localhost:5001/delete-all" -F "role=admin" -u "$AUTH_USERNAME:$AUTH_PASSWORD"
echo -e "\n"

# Step 6: Verify deletion for admin role
echo -e "${BLUE}Verifying deletion (Admin view):${NC}"
curl -s -X GET "http://localhost:5001/display-rows?role=admin" -u "$AUTH_USERNAME:$AUTH_PASSWORD" | json_pp
echo -e "\n"

# Step 7: Shut down the services
echo -e "${GREEN}Shutting down Docker services...${NC}"
docker-compose -f docker-compose.yaml down

echo -e "${GREEN}ETL service test completed.${NC}"
