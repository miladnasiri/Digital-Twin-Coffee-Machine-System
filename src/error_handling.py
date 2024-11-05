from typing import Optional
from datetime import datetime

class DigitalTwinError(Exception):
    """Base class for Digital Twin exceptions"""
    def __init__(self, message: str, timestamp: Optional[datetime] = None):
        self.timestamp = timestamp or datetime.now()
        self.message = message
        super().__init__(f"[{self.timestamp}] {message}")

class ParameterError(DigitalTwinError):
    """Exception for parameter-related errors"""
    def __init__(self, parameter: str, message: str):
        super().__init__(f"Parameter '{parameter}' error: {message}")
        self.parameter = parameter

class StateError(DigitalTwinError):
    """Exception for state-related errors"""
    def __init__(self, state_type: str, message: str):
        super().__init__(f"State error ({state_type}): {message}")
        self.state_type = state_type

class PredictionError(DigitalTwinError):
    """Exception for prediction-related errors"""
    def __init__(self, model_type: str, message: str):
        super().__init__(f"Prediction error ({model_type}): {message}")
        self.model_type = model_type

class CommunicationError(DigitalTwinError):
    """Exception for communication-related errors"""
    def __init__(self, direction: str, message: str):
        super().__init__(f"Communication error ({direction}): {message}")
        self.direction = direction

class ValidationError(DigitalTwinError):
    """Exception for validation-related errors"""
    def __init__(self, context: str, message: str):
        super().__init__(f"Validation error ({context}): {message}")
        self.context = context
