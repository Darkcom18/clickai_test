"""Configuration loader from environment variables and Streamlit secrets."""

import os
from pathlib import Path
from typing import Optional

# Try to import streamlit for secrets (only works in Streamlit environment)
try:
    import streamlit as st
    USE_STREAMLIT_SECRETS = True
except ImportError:
    USE_STREAMLIT_SECRETS = False
    from dotenv import load_dotenv
    # Load .env file (for local development)
    load_dotenv()


def get_secret(key: str, default: str = "") -> str:
    """Get secret from Streamlit secrets or environment variable."""
    if USE_STREAMLIT_SECRETS:
        try:
            # Try to get from Streamlit secrets
            secrets = st.secrets
            # Handle nested secrets (e.g., st.secrets["DEEPSEEK_API_KEY"])
            if hasattr(secrets, key):
                return getattr(secrets, key)
            # Or try as dict
            if isinstance(secrets, dict) and key in secrets:
                return secrets[key]
        except (AttributeError, KeyError, TypeError):
            pass
    
    # Fallback to environment variable
    return os.getenv(key, default)


class Config:
    """Application configuration."""
    
    # DeepSeek API
    DEEPSEEK_API_KEY: str = get_secret("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE: str = get_secret("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    
    # GitHub
    GITHUB_TOKEN: str = get_secret("GITHUB_TOKEN", "")
    GITHUB_USERNAME: str = get_secret("GITHUB_USERNAME", "")
    
    # Google Drive
    GOOGLE_DRIVE_CREDENTIALS_FILE: str = get_secret("GOOGLE_DRIVE_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_DRIVE_TOKEN_FILE: str = get_secret("GOOGLE_DRIVE_TOKEN_FILE", "token.json")
    
    # n8n
    N8N_WEBHOOK_BASE_URL: str = get_secret("N8N_WEBHOOK_BASE_URL", "")
    N8N_WEBHOOK_TOKEN: str = get_secret("N8N_WEBHOOK_TOKEN", "")
    
    # Kaggle
    KAGGLE_USERNAME: str = get_secret("KAGGLE_USERNAME", "")
    KAGGLE_KEY: str = get_secret("KAGGLE_KEY", "")
    
    # HuggingFace
    HUGGINGFACE_TOKEN: str = get_secret("HUGGINGFACE_TOKEN", "")
    
    # Model Storage
    MODEL_STORAGE_PATH: Path = Path(get_secret("MODEL_STORAGE_PATH", "ml_models/models"))
    
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

