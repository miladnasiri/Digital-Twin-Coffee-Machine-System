# src/digital_twin.py

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from .error_handling import DigitalTwinError, ParameterError, StateError
from .prediction import PredictionEngine
from .visualization import Visualizer

@dataclass
class TwinState:
    """Data class for storing twin state information"""
    timestamp: datetime
    parameters: Dict[str, float]
    alerts: List[Dict]
    predictions: Optional[Dict] = None

class DigitalTwin:
    """Enhanced Digital Twin with error handling and improved predictions"""
    
    def __init__(self, 
                 initial_state: Optional[Dict[str, float]] = None,
                 prediction_horizon: int = 20,
                 noise_level: float = 0.1):
        """
        Initialize Digital Twin with enhanced error checking
        
        Args:
            initial_state: Initial parameter values
            prediction_horizon: Steps to predict ahead
            noise_level: Simulation noise level
        """
        try:
            self.physical_state = initial_state or {
                'coffee_level': 100.0,
                'water_level': 100.0,
                'temperature': 25.0,
                'pressure': 1.0,
                'cleanliness': 100.0
            }
            
            self._validate_state(self.physical_state)
            self.digital_state = self.physical_state.copy()
            
            # Initialize components
            self.predictor = PredictionEngine(
                parameters=list(self.physical_state.keys()),
                horizon=prediction_horizon
            )
            self.visualizer = Visualizer()
            
            # Initialize history
            self.history = self._initialize_history()
            
            # System parameters
            self.noise_level = self._validate_noise_level(noise_level)
            self.health_score = 100.0
            
        except Exception as e:
            raise DigitalTwinError(f"Initialization failed: {str(e)}")
    
    def _validate_state(self, state: Dict[str, float]) -> None:
        """Validate state parameters"""
        required_params = {'coffee_level', 'water_level', 'temperature', 
                         'pressure', 'cleanliness'}
        
        if not all(param in state for param in required_params):
            missing = required_params - set(state.keys())
            raise ParameterError(f"Missing required parameters: {missing}")
        
        for param, value in state.items():
            if not isinstance(value, (int, float)):
                raise TypeError(f"Parameter {param} must be numeric, got {type(value)}")
            
            if param in {'coffee_level', 'water_level', 'cleanliness'}:
                if not 0 <= value <= 100:
                    raise ValueError(f"{param} must be between 0 and 100")
            elif param == 'temperature':
                if not 0 <= value <= 100:
                    raise ValueError("Temperature must be between 0 and 100°C")
            elif param == 'pressure':
                if not 0 <= value <= 2:
                    raise ValueError("Pressure must be between 0 and 2 bar")
    
    def update_state(self, 
                    parameter: str, 
                    value: float, 
                    is_physical: bool = True) -> TwinState:
        """
        Update state with enhanced error handling and validation
        
        Args:
            parameter: Parameter to update
            value: New value
            is_physical: Whether update is for physical twin
        
        Returns:
            TwinState: Updated state information
        """
        try:
            # Validate parameter
            if parameter not in self.physical_state:
                raise ParameterError(f"Invalid parameter: {parameter}")
            
            # Validate value
            self._validate_parameter_value(parameter, value)
            
            # Update state
            if is_physical:
                self.physical_state[parameter] = value
                # Apply Kalman filter
                self._kalman_update(parameter, value)
            else:
                self.digital_state[parameter] = value
                # Apply feedback
                self._apply_feedback(parameter, value)
            
            # Update predictions and history
            self._update_history()
            predictions = self.predictor.predict(self.history)
            
            # Check for alerts
            alerts = self._check_alerts()
            
            return TwinState(
                timestamp=datetime.now(),
                parameters=self.physical_state.copy(),
                predictions=predictions,
                alerts=alerts
            )
            
        except Exception as e:
            raise StateError(f"State update failed for {parameter}: {str(e)}")
    
    def get_health_metrics(self) -> Dict[str, float]:
        """Calculate system health metrics"""
        try:
            return {
                'health_score': self._calculate_health_score(),
                'prediction_accuracy': self._calculate_prediction_accuracy(),
                'state_sync_quality': self._calculate_sync_quality()
            }
        except Exception as e:
            raise DigitalTwinError(f"Health metrics calculation failed: {str(e)}")
    
    def visualize_state(self, 
                       include_predictions: bool = True,
                       include_alerts: bool = True) -> None:
        """Visualize current state with enhanced graphics"""
        try:
            self.visualizer.plot_state(
                physical_state=self.physical_state,
                digital_state=self.digital_state,
                history=self.history,
                predictions=self.predictor.get_current_predictions(),
                alerts=self.history['alerts'] if include_alerts else None
            )
        except Exception as e:
            raise DigitalTwinError(f"Visualization failed: {str(e)}")
    
    def _calculate_health_score(self) -> float:
        """Calculate overall system health score"""
        weights = {
            'coffee_level': 0.2,
            'water_level': 0.2,
            'cleanliness': 0.2,
            'temperature': 0.2,
            'pressure': 0.2
        }
        
        score = 0.0
        for param, weight in weights.items():
            value = self.physical_state[param]
            if param == 'temperature':
                score += weight * (1 - abs(value - 25) / 75)
            elif param == 'pressure':
                score += weight * (1 - abs(value - 1) / 1)
            else:
                score += weight * (value / 100)
        
        return max(0, min(100, score * 100))
    
    def _calculate_prediction_accuracy(self) -> float:
        """Calculate accuracy of previous predictions"""
        return self.predictor.calculate_accuracy(self.history)
    
    def _calculate_sync_quality(self) -> float:
        """Calculate synchronization quality between physical and digital twins"""
        differences = []
        for param in self.physical_state:
            physical_val = self.physical_state[param]
            digital_val = self.digital_state[param]
            max_val = 100 if param != 'pressure' else 2
            diff_percent = abs(physical_val - digital_val) / max_val * 100
            differences.append(diff_percent)
        
        return 100 - np.mean(differences)
