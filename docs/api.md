# Digital Twin System API Documentation

## Table of Contents
1. [Core Components](#core-components)
2. [Digital Twin Class](#digital-twin-class)
3. [Visualization System](#visualization-system)
4. [Prediction Engine](#prediction-engine)
5. [Error Handling](#error-handling)
6. [Utilities](#utilities)

## Core Components

### PredictiveDigitalTwin

The main class representing the digital twin system.

```python
twin = PredictiveDigitalTwin(
    initial_state=None,
    prediction_horizon=20,
    noise_level=0.1
)
```

#### Parameters:
- `initial_state` (dict, optional): Initial parameter values
- `prediction_horizon` (int): Number of steps to predict ahead
- `noise_level` (float): Simulation noise level

#### Main Methods:

```python
# Update state
twin.update_state(parameter, value, is_physical=True)

# Get health metrics
metrics = twin.get_health_metrics()

# Get current predictions
predictions = twin.get_predictions()
```

### Example Usage:
```python
# Initialize digital twin
twin = PredictiveDigitalTwin()

# Update coffee level
twin.update_state('coffee_level', 80.0)

# Get system health
health = twin.get_health_metrics()
```

## Visualization System

### EnhancedVisualizer

Interactive visualization system for the digital twin.

```python
visualizer = EnhancedVisualizer()
```

#### Main Methods:

```python
# Create interactive dashboard
visualizer.create_interactive_dashboard(twin)

# Plot current state
visualizer.plot_state(
    physical_state,
    digital_state,
    history,
    predictions,
    alerts
)
```

### Example Usage:
```python
# Create visualizer
visualizer = EnhancedVisualizer()

# Create dashboard
visualizer.create_interactive_dashboard(twin)
```

## Prediction Engine

### PredictionEngine

Advanced prediction system for the digital twin.

```python
predictor = PredictionEngine(
    parameters=['coffee_level', 'water_level', 'temperature', 'pressure', 'cleanliness'],
    horizon=20
)
```

#### Main Methods:

```python
# Generate predictions
predictions = predictor.predict(history)

# Get accuracy metrics
metrics = predictor.get_accuracy_metrics(history)
```

### Example Usage:
```python
# Generate predictions
predictions = predictor.predict(twin.history)

# Check accuracy
metrics = predictor.get_accuracy_metrics(twin.history)
```

## Error Handling

### Exception Classes

```python
# Base exception
DigitalTwinError

# Specific exceptions
ParameterError
StateError
PredictionError
CommunicationError
ValidationError
```

### Example Usage:
```python
try:
    twin.update_state('invalid_param', 50.0)
except ParameterError as e:
    print(f"Parameter error: {e}")
```

## Utilities

### Common Functions

```python
# Validate parameters
validate_parameters(parameters: Dict[str, float]) -> bool

# Calculate system health
calculate_system_health(state: Dict[str, float], thresholds: Dict[str, float]) -> float

# Save/Load state
save_state(state: Dict, filename: str) -> bool
load_state(filename: str) -> Optional[Dict]
```

### Example Usage:
```python
# Save current state
save_state(twin.physical_state, 'twin_state.json')

# Load saved state
state = load_state('twin_state.json')
```

## State Dictionary Format

The standard format for state dictionaries:

```python
state = {
    'coffee_level': float,  # 0-100
    'water_level': float,   # 0-100
    'temperature': float,   # 0-100 °C
    'pressure': float,      # 0-2 bar
    'cleanliness': float    # 0-100
}
```

## Parameter Ranges and Units

| Parameter    | Range | Unit | Description |
|-------------|-------|------|-------------|
| coffee_level | 0-100 | %    | Coffee bean level |
| water_level  | 0-100 | %    | Water tank level |
| temperature  | 0-100 | °C   | System temperature |
| pressure     | 0-2   | bar  | System pressure |
| cleanliness  | 0-100 | %    | System cleanliness |

## Alerts and Warnings

Alert dictionary format:
```python
alert = {
    'timestamp': datetime,
    'parameter': str,
    'message': str,
    'type': str,  # 'warning' or 'critical'
    'value': float
}
```

## Historical Data Format

History dictionary format:
```python
history = {
    'physical': {
        'param_name': [values],
        ...
    },
    'digital': {
        'param_name': [values],
        ...
    },
    'timestamps': [datetime_objects],
    'alerts': [alert_dictionaries]
}
```

## Bidirectional Communication

The system supports bidirectional updates:
1. Physical → Digital: Use `is_physical=True`
2. Digital → Physical: Use `is_physical=False`

Example:
```python
# Update physical state
twin.update_state('temperature', 85.0, is_physical=True)

# Update digital state
twin.update_state('temperature', 80.0, is_physical=False)
```

## Real-time Monitoring

To enable real-time monitoring:

```python
# Create interactive dashboard
visualizer = EnhancedVisualizer()
visualizer.create_interactive_dashboard(twin)

# Enable automatic updates
twin.enable_real_time_monitoring(interval=1.0)  # 1 second interval
```

## Health Metrics

Health score calculation includes:
- Parameter values within ranges
- Prediction accuracy
- System stability
- Alert frequency

Access health metrics:
```python
health_metrics = twin.get_health_metrics()
print(f"System Health: {health_metrics['health_score']}%")
```
