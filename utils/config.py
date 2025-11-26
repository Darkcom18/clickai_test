"""Configuration loader from environment variables."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE: str = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    
    # GitHub
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME: str = os.getenv("GITHUB_USERNAME", "")
    
    # Google Drive
    GOOGLE_DRIVE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_DRIVE_TOKEN_FILE: str = os.getenv("GOOGLE_DRIVE_TOKEN_FILE", "token.json")
    
    # n8n
    N8N_WEBHOOK_BASE_URL: str = os.getenv("N8N_WEBHOOK_BASE_URL", "")
    N8N_WEBHOOK_TOKEN: str = os.getenv("N8N_WEBHOOK_TOKEN", "")
    
    # Kaggle
    KAGGLE_USERNAME: str = os.getenv("KAGGLE_USERNAME", "")
    KAGGLE_KEY: str = os.getenv("KAGGLE_KEY", "")
    
    # HuggingFace
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # Model Storage
    MODEL_STORAGE_PATH: Path = Path(os.getenv("MODEL_STORAGE_PATH", "ml_models/models"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is required")
        return True
    
    @classmethod
    def ensure_model_storage(cls) -> None:
        """Ensure model storage directory exists."""
        cls.MODEL_STORAGE_PATH.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()

