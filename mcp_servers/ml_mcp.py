"""ML Model MCP Server - provides ML operations."""

from typing import Dict, List, Any, Optional
from ml_models.dataset_finder import get_dataset_finder
from ml_models.trainer import get_trainer
from ml_models.model_manager import get_model_manager
import pandas as pd
import numpy as np
import requests
from pathlib import Path
import tempfile


class MLMCPServer:
    """MCP Server for ML model operations."""
    
    def __init__(self):
        """Initialize ML MCP server."""
        self.dataset_finder = get_dataset_finder()
        self.trainer = get_trainer()
        self.model_manager = get_model_manager()
    
    def find_datasets(
        self,
        task_type: str,
        description: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find datasets for ML training.
        
        Args:
            task_type: Type of task (e.g., "salary_prediction")
            description: Additional description
            
        Returns:
            List of available datasets
        """
        return self.dataset_finder.find_dataset(task_type, description)
    
    def download_dataset(
        self,
        dataset_url: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Download a dataset.
        
        Args:
            dataset_url: URL to dataset
            output_path: Local output path (optional)
            
        Returns:
            Download information
        """
        if output_path is None:
            output_path = str(Path(tempfile.gettempdir()) / "dataset.csv")
        
        # Simple download - in production, would handle different sources
        try:
            response = requests.get(dataset_url, timeout=30)
            if response.status_code == 200:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return {
                    "path": output_path,
                    "downloaded": True,
                }
        except Exception as e:
            return {
                "path": output_path,
                "downloaded": False,
                "error": str(e),
            }
        
        return {"downloaded": False, "error": "Failed to download"}
    
    def train_model(
        self,
        dataset_path: str,
        target_column: str,
        model_name: str,
        task_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Train a model from dataset.
        
        Args:
            dataset_path: Path to dataset CSV
            target_column: Target column name
            model_name: Name for the model
            task_type: Task type (auto-detect if None)
            
        Returns:
            Training results
        """
        # Train model
        results = self.trainer.train_model(
            dataset_path=dataset_path,
            target_column=target_column,
            task_type=task_type
        )
        
        # Save model
        save_info = self.model_manager.save_model(
            model=results["model"],
            model_name=model_name,
            metadata={
                "task_type": results["task_type"],
                "score": results["score"],
                "metric": results["metric"],
                "n_features": results["n_features"],
                "n_samples": results["n_samples"],
                "feature_names": results["feature_names"],
                "target_column": target_column,
            }
        )
        
        return {
            "model_name": model_name,
            "task_type": results["task_type"],
            "score": results["score"],
            "metric": results["metric"],
            "saved": save_info["saved"],
        }
    
    def predict(
        self,
        model_name: str,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make prediction with a trained model.
        
        Args:
            model_name: Name of the model
            features: Feature values
            
        Returns:
            Prediction result
        """
        # Load model
        model = self.model_manager.load_model(model_name)
        metadata = self.model_manager.get_model_metadata(model_name)
        
        # Get feature names
        feature_names = metadata.get("feature_names", list(features.keys()))
        
        # Make prediction
        prediction = self.trainer.predict(model, features, feature_names)
        
        return {
            "model_name": model_name,
            "prediction": prediction,
        }
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all trained models.
        
        Returns:
            List of model information
        """
        return self.model_manager.list_models()
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information
        """
        return self.model_manager.get_model_metadata(model_name)
    
    def create_sample_salary_dataset(self) -> str:
        """
        Create a sample salary prediction dataset.
        
        Returns:
            Path to created dataset
        """
        # Generate sample data
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            "experience_years": np.random.randint(0, 20, n_samples),
            "education_level": np.random.choice(["Bachelor", "Master", "PhD"], n_samples),
            "company_size": np.random.choice(["Small", "Medium", "Large"], n_samples),
            "location": np.random.choice(["Urban", "Suburban", "Rural"], n_samples),
        }
        
        # Generate salary based on features
        base_salary = 30000
        salary = (
            base_salary +
            data["experience_years"] * 2000 +
            (data["education_level"] == "Master").astype(int) * 10000 +
            (data["education_level"] == "PhD").astype(int) * 20000 +
            (data["company_size"] == "Large").astype(int) * 5000 +
            np.random.normal(0, 5000, n_samples)
        )
        data["salary"] = salary.astype(int)
        
        df = pd.DataFrame(data)
        
        # Save to temp file
        output_path = Path(tempfile.gettempdir()) / "salary_dataset.csv"
        df.to_csv(output_path, index=False)
        
        return str(output_path)


# Global instance
_ml_mcp: Optional[MLMCPServer] = None


def get_ml_mcp() -> MLMCPServer:
    """Get or create ML MCP server instance."""
    global _ml_mcp
    if _ml_mcp is None:
        _ml_mcp = MLMCPServer()
    return _ml_mcp

