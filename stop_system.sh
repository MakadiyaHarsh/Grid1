#!/bin/bash
################################################################################
# GRID-SHIELD AI System Stopper
# Stops all running servers and cleans up processes
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================="
echo -e " GRID-SHIELD AI SYSTEM STOPPER"
echo -e "==========================================${NC}"
echo ""

# Function to kill process on port
kill_port() {
    local port=$1
    local name=$2
    
    if lsof -ti:$port > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping $name on port $port...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✓ $name stopped${NC}"
    else
        echo -e "${CYAN}ℹ $name not running on port $port${NC}"
    fi
}

# Stop Grid Simulator (Port 5001)
kill_port 5001 "Virtual Grid Simulator"

# Stop Cybersecurity Gateway (Port 5002)
kill_port 5002 "Cybersecurity Gateway"

# Clean up temporary launch scripts
echo ""
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -f /tmp/grid_launch.sh
rm -f /tmp/gateway_launch.sh
rm -f /tmp/admin_launch.sh
echo -e "${GREEN}✓ Cleanup complete${NC}"

echo ""
echo -e "${GREEN}=========================================="
echo -e "✅ ALL SERVERS STOPPED"
echo -e "==========================================${NC}"
echo ""
echo -e "${CYAN}Note:${NC} Terminal windows may still be open."
echo -e "      You can close them manually."
echo ""
