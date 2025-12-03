"""n8n MCP Server - provides n8n webhook operations."""

from typing import Dict, Any, Optional
import requests
from utils.config import config


class N8NMCPServer:
    """MCP Server for n8n webhook operations."""
    
    def __init__(self):
        """Initialize n8n client."""
        self.base_url = None
        self.token = None
        self.initialized = False
        
        if config.N8N_WEBHOOK_BASE_URL:
            self.base_url = config.N8N_WEBHOOK_BASE_URL.rstrip('/')
            self.token = config.N8N_WEBHOOK_TOKEN
            self.initialized = True
        else:
            print("Warning: N8N_WEBHOOK_BASE_URL not configured. n8n features will be disabled.")
    
    def _check_initialized(self):
        """Check if n8n client is initialized."""
        if not self.initialized:
            raise ValueError(
                "n8n is not configured. Please set N8N_WEBHOOK_BASE_URL in .env file. "
                "See SETUP.md for instructions."
            )
    
    def trigger_workflow(
        self,
        workflow_id: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trigger an n8n workflow via webhook.

        Args:
            workflow_id: Either full webhook URL or workflow ID/path
            data: Data to send to workflow

        Returns:
            Response from workflow
        """
        # Support full URL or relative path
        if workflow_id.startswith(('http://', 'https://')):
            url = workflow_id  # Full URL provided - no config needed
        else:
            self._check_initialized()  # Only check if using relative path
            url = f"{self.base_url}/{workflow_id}"  # Relative path

        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.post(
            url,
            json=data or {},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "success": response.status_code == 200,
        }
    
    def trigger_workflow_with_params(
        self,
        workflow_id: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trigger workflow with query parameters and body.

        Args:
            workflow_id: Either full webhook URL or workflow ID/path
            params: Query parameters
            body: Request body

        Returns:
            Response from workflow
        """
        # Support full URL or relative path
        if workflow_id.startswith(('http://', 'https://')):
            url = workflow_id  # Full URL provided - no config needed
        else:
            self._check_initialized()  # Only check if using relative path
            url = f"{self.base_url}/{workflow_id}"  # Relative path

        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.post(
            url,
            params=params,
            json=body or {},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "success": response.status_code == 200,
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to n8n instance.
        
        Returns:
            Connection status
        """
        self._check_initialized()
        try:
            # Try to access base URL
            response = requests.get(
                self.base_url,
                timeout=5
            )
            return {
                "connected": True,
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
            }


# Global instance
_n8n_mcp: Optional[N8NMCPServer] = None
_last_n8n_url: Optional[str] = None


def get_n8n_mcp() -> N8NMCPServer:
    """Get or create n8n MCP server instance."""
    global _n8n_mcp, _last_n8n_url
    
    # Reload if URL changed (for dynamic credentials from UI)
    current_url = config.N8N_WEBHOOK_BASE_URL
    if _n8n_mcp is None or _last_n8n_url != current_url:
        try:
            _n8n_mcp = N8NMCPServer()
            _last_n8n_url = current_url
        except Exception as e:
            print(f"Warning: Could not initialize n8n MCP: {e}")
            _n8n_mcp = N8NMCPServer()  # Will have initialized=False
            _last_n8n_url = current_url
    
    return _n8n_mcp

