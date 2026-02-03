"""
Grid Forwarder Module
Handles safe command forwarding to the Virtual Power Grid Simulator
"""

import requests
from typing import Dict, Any, Optional
import config

class GridForwarder:
    """Forwards validated commands to the grid simulator"""
    
    def __init__(self):
        self.grid_url = f"{config.GRID_BASE_URL}{config.GRID_COMMAND_ENDPOINT}"
        self.timeout = 5  # seconds
    
    def forward_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forward command to grid simulator
        
        Returns:
            {
                "success": bool,
                "response": dict or None,
                "error": str or None
            }
        """
        try:
            # Send POST request to grid simulator
            response = requests.post(
                self.grid_url,
                json=command,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            # Check response status
            if response.status_code == 200:
                try:
                    grid_response = response.json()
                    return {
                        "success": True,
                        "response": grid_response,
                        "error": None
                    }
                except ValueError:
                    return {
                        "success": False,
                        "response": None,
                        "error": "Invalid JSON response from grid"
                    }
            else:
                return {
                    "success": False,
                    "response": None,
                    "error": f"Grid returned status code {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "response": None,
                "error": f"Grid connection timeout after {self.timeout}s"
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "response": None,
                "error": f"Cannot connect to grid at {self.grid_url}. Is the grid simulator running?"
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "error": f"Unexpected error forwarding to grid: {str(e)}"
            }
    
    def check_grid_health(self) -> bool:
        """Check if grid simulator is reachable"""
        try:
            response = requests.get(
                config.GRID_BASE_URL,
                timeout=2
            )
            return response.status_code in [200, 404]  # 404 is ok, means server is up
        except:
            return False
    
    def get_grid_telemetry(self) -> Dict[str, Any]:
        """
        Fetch current grid telemetry for AI analysis
        
        Returns:
            dict: Current grid state or empty dict on error
        """
        try:
            response = requests.get(
                f"{config.GRID_BASE_URL}/grid/data",
                timeout=2
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("grid_state", {})
            return {}
        except:
            return {}

