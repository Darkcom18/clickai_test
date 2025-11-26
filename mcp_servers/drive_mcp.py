"""Google Drive MCP Server - provides Drive operations."""

from typing import Dict, List, Any, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import os
import io
from pathlib import Path
from utils.config import config


class DriveMCPServer:
    """MCP Server for Google Drive operations."""
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    def __init__(self):
        """Initialize Google Drive client."""
        self.creds = None
        self.service = None
        self.initialized = False
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        creds_file = Path(config.GOOGLE_DRIVE_CREDENTIALS_FILE)
        token_file = Path(config.GOOGLE_DRIVE_TOKEN_FILE)
        
        if not creds_file.exists():
            print(f"Warning: Google Drive credentials file not found: {creds_file}")
            print("Google Drive features will be disabled. See SETUP.md for instructions.")
            return
        
        try:
            # Load existing token
            if token_file.exists():
                self.creds = Credentials.from_authorized_user_file(str(token_file), self.SCOPES)
            
            # Refresh or get new token
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(creds_file), self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                
                # Save token
                with open(token_file, 'w') as token:
                    token.write(self.creds.to_json())
            
            self.service = build('drive', 'v3', credentials=self.creds)
            self.initialized = True
        except Exception as e:
            print(f"Warning: Failed to initialize Google Drive client: {e}")
            print("Google Drive features will be disabled.")
    
    def _check_initialized(self):
        """Check if Drive client is initialized."""
        if not self.initialized:
            raise ValueError(
                "Google Drive is not configured. Please setup credentials. "
                "See SETUP.md for instructions."
            )
    
    def list_files(
        self,
        query: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        List files in Google Drive.
        
        Args:
            query: Search query (e.g., "name contains 'test'")
            max_results: Maximum number of results
            
        Returns:
            List of file information
        """
        self._check_initialized()
        if query:
            query_str = query
        else:
            query_str = "trashed=false"
        
        results = self.service.files().list(
            q=query_str,
            pageSize=max_results,
            fields="files(id, name, mimeType, size, modifiedTime, webViewLink)"
        ).execute()
        
        files = []
        for file in results.get('files', []):
            files.append({
                "id": file.get('id'),
                "name": file.get('name'),
                "mimeType": file.get('mimeType'),
                "size": file.get('size'),
                "modifiedTime": file.get('modifiedTime'),
                "url": file.get('webViewLink'),
            })
        return files
    
    def upload_file(
        self,
        file_path: str,
        folder_id: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to Google Drive.
        
        Args:
            file_path: Local file path
            folder_id: Target folder ID (optional)
            name: File name in Drive (optional, uses original name)
            
        Returns:
            File information
        """
        self._check_initialized()
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_metadata = {
            'name': name or file_path_obj.name
        }
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(
            str(file_path_obj),
            resumable=True
        )
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return {
            "id": file.get('id'),
            "name": file.get('name'),
            "url": file.get('webViewLink'),
        }
    
    def download_file(self, file_id: str, output_path: str) -> Dict[str, Any]:
        """
        Download a file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            output_path: Local output path
            
        Returns:
            Download information
        """
        self._check_initialized()
        request = self.service.files().get_media(fileId=file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path_obj, 'wb') as f:
            f.write(file_content.getvalue())
        
        return {
            "file_id": file_id,
            "output_path": str(output_path_obj),
            "size": len(file_content.getvalue()),
        }
    
    def create_folder(self, name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a folder in Google Drive.
        
        Args:
            name: Folder name
            parent_id: Parent folder ID (optional)
            
        Returns:
            Folder information
        """
        self._check_initialized()
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()
        
        return {
            "id": folder.get('id'),
            "name": folder.get('name'),
            "url": folder.get('webViewLink'),
        }


# Global instance
_drive_mcp: Optional[DriveMCPServer] = None


def get_drive_mcp() -> DriveMCPServer:
    """Get or create Drive MCP server instance."""
    global _drive_mcp
    if _drive_mcp is None:
        try:
            _drive_mcp = DriveMCPServer()
        except Exception as e:
            print(f"Warning: Could not initialize Drive MCP: {e}")
            _drive_mcp = DriveMCPServer()  # Will have initialized=False
    return _drive_mcp

