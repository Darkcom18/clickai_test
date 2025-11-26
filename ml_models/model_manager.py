"""Model manager for saving and loading ML models."""

from typing import Optional, Dict, Any
from pathlib import Path
import joblib
import json
from utils.config import config


class ModelManager:
    """Manage ML models - save, load, list."""
    
    def __init__(self):
        """Initialize model manager."""
        self.storage_path = config.MODEL_STORAGE_PATH
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_model(
        self,
        model: Any,
        model_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save a trained model.
        
        Args:
            model: Trained model object
            model_name: Name for the model
            metadata: Additional metadata
            
        Returns:
            Save information
        """
        model_file = self.storage_path / f"{model_name}.joblib"
        metadata_file = self.storage_path / f"{model_name}_metadata.json"
        
        # Save model
        joblib.dump(model, model_file)
        
        # Save metadata
        metadata = metadata or {}
        metadata["model_name"] = model_name
        metadata["model_file"] = str(model_file)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "model_name": model_name,
            "model_file": str(model_file),
            "metadata_file": str(metadata_file),
            "saved": True,
        }
    
    def load_model(self, model_name: str) -> Any:
        """
        Load a saved model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Loaded model
        """
        model_file = self.storage_path / f"{model_name}.joblib"
        if not model_file.exists():
            raise FileNotFoundError(f"Model not found: {model_name}")
        
        return joblib.load(model_file)
    
    def get_model_metadata(self, model_name: str) -> Dict[str, Any]:
        """
        Get model metadata.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model metadata
        """
        metadata_file = self.storage_path / f"{model_name}_metadata.json"
        if not metadata_file.exists():
            return {}
        
        with open(metadata_file, 'r') as f:
            return json.load(f)
    
    def list_models(self) -> list[Dict[str, Any]]:
        """
        List all saved models.
        
        Returns:
            List of model information
        """
        models = []
        for model_file in self.storage_path.glob("*.joblib"):
            model_name = model_file.stem
            metadata = self.get_model_metadata(model_name)
            models.append({
                "name": model_name,
                "file": str(model_file),
                "metadata": metadata,
            })
        return models
    
    def delete_model(self, model_name: str) -> Dict[str, Any]:
        """
        Delete a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Deletion status
        """
        model_file = self.storage_path / f"{model_name}.joblib"
        metadata_file = self.storage_path / f"{model_name}_metadata.json"
        
        deleted = []
        if model_file.exists():
            model_file.unlink()
            deleted.append(str(model_file))
        
        if metadata_file.exists():
            metadata_file.unlink()
            deleted.append(str(metadata_file))
        
        return {
            "model_name": model_name,
            "deleted": deleted,
        }


def get_model_manager() -> ModelManager:
    """Get model manager instance."""
    return ModelManager()

