"""Auto trainer for ML models."""

from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class AutoTrainer:
    """Automatically train ML models based on dataset and task."""
    
    def __init__(self):
        """Initialize trainer."""
        self.label_encoders = {}
    
    def detect_task_type(self, df: pd.DataFrame, target_column: str) -> str:
        """
        Detect task type (regression or classification).
        
        Args:
            df: DataFrame
            target_column: Target column name
            
        Returns:
            Task type: 'regression' or 'classification'
        """
        target = df[target_column]
        
        # Check if target is numeric
        if pd.api.types.is_numeric_dtype(target):
            # Regression
            return "regression"
        else:
            # Classification
            return "classification"
    
    def prepare_data(
        self,
        df: pd.DataFrame,
        target_column: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for training.
        
        Args:
            df: DataFrame
            target_column: Target column name
            
        Returns:
            X (features), y (target)
        """
        # Drop missing values
        df = df.dropna()
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Encode categorical features
        for col in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        # Encode target if needed
        if not pd.api.types.is_numeric_dtype(y):
            le = LabelEncoder()
            y = le.fit_transform(y)
            self.label_encoders[target_column] = le
        
        return X, y
    
    def train_model(
        self,
        dataset_path: str,
        target_column: str,
        task_type: Optional[str] = None,
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """
        Train a model from dataset.
        
        Args:
            dataset_path: Path to dataset CSV file
            target_column: Target column name
            task_type: Task type ('regression' or 'classification'), auto-detect if None
            test_size: Test set size ratio
            
        Returns:
            Training results
        """
        # Load dataset
        df = pd.read_csv(dataset_path)
        
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Detect task type if not provided
        if task_type is None:
            task_type = self.detect_task_type(df, target_column)
        
        # Prepare data
        X, y = self.prepare_data(df, target_column)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Select and train model
        if task_type == "regression":
            # Try Random Forest first, fallback to Linear Regression
            try:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                score = r2_score(y_test, y_pred)
                metric_name = "r2_score"
            except:
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                score = r2_score(y_test, y_pred)
                metric_name = "r2_score"
        else:  # classification
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            metric_name = "accuracy"
        
        return {
            "model": model,
            "task_type": task_type,
            "score": float(score),
            "metric": metric_name,
            "n_features": len(X.columns),
            "n_samples": len(df),
            "feature_names": list(X.columns),
        }
    
    def predict(
        self,
        model: Any,
        features: Dict[str, Any],
        feature_names: list[str]
    ) -> Any:
        """
        Make prediction with trained model.
        
        Args:
            model: Trained model
            features: Feature values as dictionary
            feature_names: List of feature names in order
            
        Returns:
            Prediction result
        """
        # Create feature vector
        feature_vector = []
        for name in feature_names:
            value = features.get(name, 0)
            # Encode if needed
            if name in self.label_encoders:
                try:
                    value = self.label_encoders[name].transform([str(value)])[0]
                except:
                    value = 0
            feature_vector.append(value)
        
        # Make prediction
        prediction = model.predict([feature_vector])[0]
        
        # Decode if needed
        if hasattr(model, 'classes_') and hasattr(model, 'predict_proba'):
            # Classification model
            return {
                "prediction": int(prediction),
                "probability": float(model.predict_proba([feature_vector])[0].max()),
            }
        else:
            # Regression model
            return {
                "prediction": float(prediction),
            }


def get_trainer() -> AutoTrainer:
    """Get trainer instance."""
    return AutoTrainer()

