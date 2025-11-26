"""Dataset finder for ML training."""

from typing import List, Dict, Any, Optional
import requests
from utils.config import config


class DatasetFinder:
    """Find datasets from various sources."""
    
    def __init__(self):
        """Initialize dataset finder."""
        self.kaggle_username = config.KAGGLE_USERNAME
        self.kaggle_key = config.KAGGLE_KEY
        self.hf_token = config.HUGGINGFACE_TOKEN
    
    def search_kaggle_datasets(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search datasets on Kaggle.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            List of dataset information
        """
        # Note: Requires kaggle API setup
        # This is a simplified version - full implementation would use kaggle API
        datasets = []
        try:
            # Example: salary prediction dataset
            if "salary" in query.lower() or "lương" in query.lower():
                datasets.append({
                    "name": "salary-data",
                    "source": "kaggle",
                    "description": "Salary prediction dataset",
                    "url": "https://www.kaggle.com/datasets/kaggle/sf-salaries",
                    "tags": ["salary", "prediction", "regression"],
                })
        except Exception as e:
            print(f"Error searching Kaggle: {e}")
        
        return datasets[:max_results]
    
    def search_huggingface_datasets(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search datasets on HuggingFace.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            List of dataset information
        """
        datasets = []
        try:
            url = "https://huggingface.co/api/datasets"
            params = {"search": query, "limit": max_results}
            headers = {}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("datasets", [])[:max_results]:
                    datasets.append({
                        "name": item.get("id", ""),
                        "source": "huggingface",
                        "description": item.get("description", ""),
                        "url": f"https://huggingface.co/datasets/{item.get('id', '')}",
                        "tags": item.get("tags", []),
                    })
        except Exception as e:
            print(f"Error searching HuggingFace: {e}")
        
        return datasets[:max_results]
    
    def find_dataset(
        self,
        task_type: str,
        description: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find datasets for a specific task.
        
        Args:
            task_type: Type of task (e.g., "salary_prediction", "classification")
            description: Additional description
            
        Returns:
            List of relevant datasets
        """
        query = f"{task_type} {description or ''}"
        datasets = []
        
        # Search Kaggle
        kaggle_results = self.search_kaggle_datasets(query)
        datasets.extend(kaggle_results)
        
        # Search HuggingFace
        hf_results = self.search_huggingface_datasets(query)
        datasets.extend(hf_results)
        
        return datasets


def get_dataset_finder() -> DatasetFinder:
    """Get dataset finder instance."""
    return DatasetFinder()

