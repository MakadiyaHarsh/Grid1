# Cybersecurity Gateway Configuration
# Grid connection and security parameters

# Grid Simulator Connection
GRID_HOST = "localhost"
GRID_PORT = 5001
GRID_COMMAND_ENDPOINT = "/grid/command"
GRID_BASE_URL = f"http://{GRID_HOST}:{GRID_PORT}"

# Security Thresholds
RISK_THRESHOLD = 0.70  # Commands with risk > 0.70 will be blocked
ANOMALY_THRESHOLD = 0.60  # Anomaly score threshold for attack detection

# Cyber Rule Boundaries
VOLTAGE_MIN = 0.90  # per unit
VOLTAGE_MAX = 1.10  # per unit
FREQUENCY_MIN = 49.0  # Hz
FREQUENCY_MAX = 51.0  # Hz

# Valid Breaker States
VALID_BREAKER_STATES = ["ON", "OFF"]

# Attack Detection Parameters
REPLAY_WINDOW_SECONDS = 5  # Time window for replay attack detection
REPLAY_COUNT_THRESHOLD = 3  # Number of identical commands to trigger replay detection
MAX_COMMAND_HISTORY = 100  # Maximum commands to keep in memory

# Gateway Server Configuration
GATEWAY_HOST = "0.0.0.0"
GATEWAY_PORT = 5002

# AI Engine Configuration
AI_RISK_WEIGHT = 1.2  # AI risk scores are weighted higher (multiplier)
AI_ENABLED = True     # Enable/disable AI analysis

# Logging Configuration
LOG_LEVEL = "INFO"
ENABLE_COLOR_LOGS = True

