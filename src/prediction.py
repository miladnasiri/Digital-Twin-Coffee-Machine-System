import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

class PredictionEngine:
    """Advanced prediction engine for digital twin system"""
    
    def __init__(self, parameters: List[str], horizon: int = 20):
        self.parameters = parameters
        self.horizon = horizon
        self.models = {param: LinearRegression() for param in parameters}
        self.scalers = {param: StandardScaler() for param in parameters}
        self.confidence_level = 0.95
        
    def predict(self, history: Dict) -> Dict[str, np.ndarray]:
        """Generate predictions for all parameters"""
        predictions = {}
        confidence_intervals = {}
        
        for param in self.parameters:
            try:
                pred, conf = self._predict_parameter(param, history)
                predictions[param] = pred
                confidence_intervals[param] = conf
            except Exception as e:
                logging.error(f"Prediction failed for {param}: {str(e)}")
                continue
        
        return {
            'predictions': predictions,
            'confidence_intervals': confidence_intervals,
            'timestamp': datetime.now()
        }
    
    def _predict_parameter(self, 
                         parameter: str, 
                         history: Dict) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """Generate prediction for a single parameter"""
        # Prepare data
        X = self._prepare_features(history, parameter)
        y = np.array(history['physical'][parameter])
        
        if len(X) < 2:
            raise ValueError("Insufficient data for prediction")
        
        # Scale data
        X_scaled = self.scalers[parameter].fit_transform(X)
        
        # Fit model
        self.models[parameter].fit(X_scaled, y)
        
        # Generate future features
        future_X = self._generate_future_features(X[-1:], self.horizon)
        future_X_scaled = self.scalers[parameter].transform(future_X)
        
        # Make prediction
        predictions = self.models[parameter].predict(future_X_scaled)
        
        # Calculate confidence intervals
        confidence = self._calculate_confidence_intervals(
            model=self.models[parameter],
            X=future_X_scaled,
            y_hist=y,
            X_hist=X_scaled
        )
        
        return predictions, confidence
    
    def _prepare_features(self, history: Dict, parameter: str) -> np.ndarray:
        """Prepare feature matrix for prediction"""
        values = np.array(history['physical'][parameter])
        n = len(values)
        
        features = []
        for i in range(n):
            feat = [
                values[i],  # Current value
                np.mean(values[max(0, i-5):i+1]),  # Moving average
                np.std(values[max(0, i-5):i+1]),   # Moving std
                i / n  # Normalized time
            ]
            features.append(feat)
        
        return np.array(features)
    
    def _generate_future_features(self, 
                                last_features: np.ndarray, 
                                steps: int) -> np.ndarray:
        """Generate feature matrix for future predictions"""
        future_features = []
        current_features = last_features[-1].copy()
        
        for i in range(steps):
            next_features = current_features.copy()
            next_features[-1] = (len(last_features) + i + 1) / (len(last_features) + steps)
            future_features.append(next_features)
            current_features = next_features.copy()
        
        return np.array(future_features)
    
    def _calculate_confidence_intervals(self,
                                     model: LinearRegression,
                                     X: np.ndarray,
                                     y_hist: np.ndarray,
                                     X_hist: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate confidence intervals for predictions"""
        # Calculate prediction variance
        y_pred_hist = model.predict(X_hist)
        mse = np.mean((y_hist - y_pred_hist) ** 2)
        std_dev = np.sqrt(mse)
        
        # Calculate intervals
        z_score = 1.96  # 95% confidence interval
        predictions = model.predict(X)
        margin = z_score * std_dev
        
        return {
            'lower': predictions - margin,
            'upper': predictions + margin
        }
    
    def get_accuracy_metrics(self, history: Dict) -> Dict[str, float]:
        """Calculate prediction accuracy metrics"""
        metrics = {}
        
        for param in self.parameters:
            try:
                y_true = np.array(history['physical'][param])
                y_pred = np.array(history['digital'][param])
                
                mse = np.mean((y_true - y_pred) ** 2)
                mae = np.mean(np.abs(y_true - y_pred))
                mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                
                metrics[param] = {
                    'mse': mse,
                    'mae': mae,
                    'mape': mape
                }
            except Exception as e:
                logging.error(f"Metric calculation failed for {param}: {str(e)}")
                continue
        
        return metrics
