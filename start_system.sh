#!/bin/bash
################################################################################
# GRID-SHIELD AI System Launcher (Simplified & Fixed)
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}=========================================="
echo -e " GRID-SHIELD AI SYSTEM LAUNCHER"
echo -e "==========================================${NC}"
echo ""

# Kill existing processes
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:5001 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:5002 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

# Create launch scripts that STAY OPEN
echo -e "${YELLOW}Creating launch scripts...${NC}"

# Grid launch script
cat > "$BASE_DIR/launch_grid.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/virtual_grid"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "⚡ VIRTUAL POWER GRID SIMULATOR"
echo "=========================================="
echo ""

# Run grid simulator
python3 grid_simulator.py

# If it exits, show error and wait
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: Grid simulator exited with code $EXIT_CODE"
fi
echo ""
echo "Press Enter to close this window..."
read
EOF

# Gateway launch script
cat > "$BASE_DIR/launch_gateway.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/cyber_gateway"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "🛡️  CYBERSECURITY GATEWAY"
echo "=========================================="
echo ""

# Run gateway
python3 gateway.py

# If it exits, show error and wait
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: Gateway exited with code $EXIT_CODE"
fi
echo ""
echo "Press Enter to close this window..."
read
EOF

# Admin console launch script
cat > "$BASE_DIR/launch_admin.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run admin console
python3 admin_console.py

# Wait before closing
echo ""
echo "Press Enter to close this window..."
read
EOF

# Attack simulator launch script
cat > "$BASE_DIR/launch_attacker.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "⚠️  ATTACK SIMULATOR"
echo "=========================================="
echo ""

# Run attack simulator
python3 attack_simulator.py

# Wait before closing
echo ""
echo "Press Enter to close this window..."
read
EOF

chmod +x "$BASE_DIR/launch_grid.sh"
chmod +x "$BASE_DIR/launch_gateway.sh"
chmod +x "$BASE_DIR/launch_admin.sh"
chmod +x "$BASE_DIR/launch_attacker.sh"

echo -e "${GREEN}✓ Launch scripts created${NC}"
echo ""

# Launch terminals
echo -e "${CYAN}Launching terminals...${NC}"
echo ""

# Detect terminal emulator
if command -v gnome-terminal &> /dev/null; then
    TERM_CMD="gnome-terminal"
    echo -e "${GREEN}Using: gnome-terminal${NC}"
    
    # Launch Grid
    echo -e "${CYAN}1️⃣  Starting Grid Simulator...${NC}"
    gnome-terminal --title="Grid Simulator (Port 5001)" --wait -- bash "$BASE_DIR/launch_grid.sh" &
    sleep 2
    
    # Launch Gateway
    echo -e "${CYAN}2️⃣  Starting Cybersecurity Gateway...${NC}"
    gnome-terminal --title="Cybersecurity Gateway (Port 5002)" --wait -- bash "$BASE_DIR/launch_gateway.sh" &
    sleep 3
    
    # Launch Admin Console
    echo -e "${CYAN}3️⃣  Starting Admin Console...${NC}"
    gnome-terminal --title="Admin Console" --wait -- bash "$BASE_DIR/launch_admin.sh" &
    sleep 1
    
    # Launch Attack Simulator
    echo -e "${CYAN}4️⃣  Starting Attack Simulator...${NC}"
    gnome-terminal --title="⚠️ Attack Simulator" --wait -- bash "$BASE_DIR/launch_attacker.sh" &
    sleep 1
    
elif command -v xterm &> /dev/null; then
    TERM_CMD="xterm"
    echo -e "${GREEN}Using: xterm${NC}"
    
    # Launch Grid
    echo -e "${CYAN}1️⃣  Starting Grid Simulator...${NC}"
    xterm -title "Grid Simulator (Port 5001)" -hold -e "bash $BASE_DIR/launch_grid.sh" &
    sleep 2
    
    # Launch Gateway
    echo -e "${CYAN}2️⃣  Starting Cybersecurity Gateway...${NC}"
    xterm -title "Cybersecurity Gateway (Port 5002)" -hold -e "bash $BASE_DIR/launch_gateway.sh" &
    sleep 3
    
    # Launch Admin Console
    echo -e "${CYAN}3️⃣  Starting Admin Console...${NC}"
    xterm -title "Admin Console" -hold -e "bash $BASE_DIR/launch_admin.sh" &
    sleep 1
    
    # Launch Attack Simulator
    echo -e "${CYAN}4️⃣  Starting Attack Simulator...${NC}"
    xterm -title "⚠️ Attack Simulator" -hold -e "bash $BASE_DIR/launch_attacker.sh" &
    sleep 1
    
elif command -v konsole &> /dev/null; then
    TERM_CMD="konsole"
    echo -e "${GREEN}Using: konsole${NC}"
    
    # Launch Grid
    echo -e "${CYAN}1️⃣  Starting Grid Simulator...${NC}"
    konsole --title "Grid Simulator (Port 5001)" -e "bash $BASE_DIR/launch_grid.sh" &
    sleep 2
    
    # Launch Gateway
    echo -e "${CYAN}2️⃣  Starting Cybersecurity Gateway...${NC}"
    konsole --title "Cybersecurity Gateway (Port 5002)" -e "bash $BASE_DIR/launch_gateway.sh" &
    sleep 3
    
    # Launch Admin Console
    echo -e "${CYAN}3️⃣  Starting Admin Console...${NC}"
    konsole --title "Admin Console" -e "bash $BASE_DIR/launch_admin.sh" &
    sleep 1
    
    # Launch Attack Simulator
    echo -e "${CYAN}4️⃣  Starting Attack Simulator...${NC}"
    konsole --title "⚠️ Attack Simulator" -e "bash $BASE_DIR/launch_attacker.sh" &
    sleep 1
    
else
    echo -e "${RED}ERROR: No terminal emulator found!${NC}"
    echo -e "${YELLOW}Please install one of: gnome-terminal, xterm, konsole${NC}"
    echo ""
    echo -e "${CYAN}Or run manually:${NC}"
    echo -e "  Terminal 1: ${YELLOW}./launch_grid.sh${NC}"
    echo -e "  Terminal 2: ${YELLOW}./launch_gateway.sh${NC}"
    echo -e "  Terminal 3: ${YELLOW}./launch_admin.sh${NC}"
    echo -e "  Terminal 4: ${YELLOW}./launch_attacker.sh${NC}"
    exit 1
fi

# Wait for servers
echo ""
echo -e "${YELLOW}Waiting for servers to start...${NC}"
sleep 3

# Check server status
echo -e "${YELLOW}Checking server status...${NC}"

if curl -s http://localhost:5001/grid/data > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Grid Simulator is running on port 5001${NC}"
else
    echo -e "${YELLOW}⚠ Grid Simulator may still be starting...${NC}"
fi

if curl -s http://localhost:5002/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Cybersecurity Gateway is running on port 5002${NC}"
else
    echo -e "${YELLOW}⚠ Cybersecurity Gateway may still be starting...${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo -e "✅ SYSTEM LAUNCHED!"
echo -e "==========================================${NC}"
echo ""
echo -e "${CYAN}Four terminal windows are now open:${NC}"
echo -e "  ${GREEN}1.${NC} Grid Simulator (Port 5001)"
echo -e "  ${GREEN}2.${NC} Cybersecurity Gateway (Port 5002)"
echo -e "  ${GREEN}3.${NC} Admin Console"
echo -e "  ${RED}4.${NC} Attack Simulator ${YELLOW}(For demos only!)${NC}"
echo -e "${CYAN}Check each terminal for status.${NC}"
echo ""
echo -e "${YELLOW}To stop all servers:${NC} ./stop_system.sh"
echo ""
