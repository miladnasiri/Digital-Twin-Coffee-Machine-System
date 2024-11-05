import pytest
import numpy as np
from datetime import datetime
from src.digital_twin import PredictiveDigitalTwin
from src.error_handling import DigitalTwinError, ParameterError

@pytest.fixture
def digital_twin():
    return PredictiveDigitalTwin()

def test_initialization(digital_twin):
    """Test proper initialization of digital twin"""
    assert digital_twin.physical_state['coffee_level'] == 100.0
    assert digital_twin.physical_state['water_level'] == 100.0
    assert digital_twin.physical_state['temperature'] == 25.0
    assert digital_twin.physical_state['pressure'] == 1.0
    assert digital_twin.physical_state['cleanliness'] == 100.0

def test_parameter_update(digital_twin):
    """Test parameter update functionality"""
    digital_twin.update_state('coffee_level', 80.0)
    assert digital_twin.physical_state['coffee_level'] == 80.0
    assert len(digital_twin.history['physical']['coffee_level']) == 2

def test_invalid_parameter():
    """Test error handling for invalid parameters"""
    twin = PredictiveDigitalTwin()
    with pytest.raises(ParameterError):
        twin.update_state('invalid_param', 50.0)

def test_prediction_generation(digital_twin):
    """Test prediction generation"""
    digital_twin.update_state('coffee_level', 80.0)
    predictions = digital_twin.predictor.predict(digital_twin.history)
    assert 'predictions' in predictions
    assert 'coffee_level' in predictions['predictions']

def test_alert_generation(digital_twin):
    """Test alert generation"""
    digital_twin.update_state('coffee_level', 15.0)
    assert len(digital_twin.history['alerts']) > 0
    assert 'WARNING' in digital_twin.history['alerts'][-1]['message']

def test_health_score(digital_twin):
    """Test health score calculation"""
    score = digital_twin._calculate_health_score()
    assert 0 <= score <= 100

def test_parameter_validation(digital_twin):
    """Test parameter validation"""
    with pytest.raises(ValueError):
        digital_twin.update_state('temperature', 150.0)
    with pytest.raises(ValueError):
        digital_twin.update_state('pressure', 3.0)

def test_bidirectional_sync(digital_twin):
    """Test bidirectional synchronization"""
    digital_twin.update_state('coffee_level', 80.0, is_physical=True)
    assert abs(digital_twin.digital_state['coffee_level'] - 80.0) < 5.0

def test_prediction_accuracy(digital_twin):
    """Test prediction accuracy metrics"""
    for i in range(5):
        digital_twin.update_state('coffee_level', 100 - i*10)
    metrics = digital_twin.predictor.get_accuracy_metrics(digital_twin.history)
    assert 'coffee_level' in metrics
    assert 'mape' in metrics['coffee_level']
