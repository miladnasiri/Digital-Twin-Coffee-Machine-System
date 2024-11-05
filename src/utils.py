import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import logging

def setup_logging():
    """Configure logging for the digital twin system"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('digital_twin.log'),
            logging.StreamHandler()
        ]
    )

def validate_parameters(parameters: Dict[str, float]) -> bool:
    """Validate parameter values"""
    try:
        for param, value in parameters.items():
            if param in ['coffee_level', 'water_level', 'cleanliness']:
                if not 0 <= value <= 100:
                    return False
            elif param == 'temperature':
                if not 0 <= value <= 100:
                    return False
            elif param == 'pressure':
                if not 0 <= value <= 2:
                    return False
        return True
    except Exception as e:
        logging.error(f"Parameter validation failed: {str(e)}")
        return False

def calculate_moving_average(data: List[float], window: int = 5) -> np.ndarray:
    """Calculate moving average of data"""
    return np.convolve(data, np.ones(window)/window, mode='valid')

def calculate_rate_of_change(data: List[float], time_delta: float = 1.0) -> np.ndarray:
    """Calculate rate of change"""
    return np.diff(data) / time_delta

def save_state(state: Dict, filename: str) -> bool:
    """Save state to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(state, f, default=str)
        return True
    except Exception as e:
        logging.error(f"State save failed: {str(e)}")
        return False

def load_state(filename: str) -> Optional[Dict]:
    """Load state from file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"State load failed: {str(e)}")
        return None

def calculate_system_health(state: Dict[str, float], 
                          thresholds: Dict[str, float]) -> float:
    """Calculate overall system health score"""
    scores = []
    for param, value in state.items():
        threshold = thresholds.get(param, 0)
        if param in ['coffee_level', 'water_level', 'cleanliness']:
            scores.append(value / 100)
        elif param == 'temperature':
            scores.append(1 - abs(value - 25) / 75)
        elif param == 'pressure':
            scores.append(1 - abs(value - 1) / 1)
    
    return np.mean(scores) * 100

def format_time_series(data: List[float], 
                      timestamps: List[datetime]) -> Dict[str, List]:
    """Format time series data for visualization"""
    return {
        'values': data,
        'timestamps': [t.strftime('%Y-%m-%d %H:%M:%S') for t in timestamps]
    }

def interpolate_missing_values(data: List[float], 
                             max_gap: int = 3) -> np.ndarray:
    """Interpolate missing values in time series"""
    data = np.array(data)
    mask = np.isnan(data)
    
    if not mask.any():
        return data
        
    return np.interp(
        np.arange(len(data)),
        np.arange(len(data))[~mask],
        data[~mask]
    )
