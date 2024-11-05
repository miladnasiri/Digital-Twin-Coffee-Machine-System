from digital_twin import PredictiveDigitalTwin
from visualization import EnhancedVisualizer
import time

def run_demonstration():
    print("Starting Digital Twin Demonstration...")
    
    # Initialize system
    twin = PredictiveDigitalTwin()
    visualizer = EnhancedVisualizer()
    
    # Show initial state
    print("\nInitial State:")
    for param, value in twin.physical_state.items():
        print(f"{param}: {value}")
    
    # Run some operations
    operations = [
        ('Make Coffee', {'coffee_level': 80, 'water_level': 75, 'temperature': 85}),
        ('Heavy Usage', {'coffee_level': 60, 'water_level': 55, 'temperature': 90}),
        ('Maintenance', {'cleanliness': 100, 'pressure': 1.0}),
    ]
    
    for operation, values in operations:
        print(f"\nSimulating: {operation}")
        for param, value in values.items():
            twin.update_state(param, value)
        visualizer.plot_state(
            twin.physical_state,
            twin.digital_state,
            twin.history,
            twin.predictor.get_current_predictions() if hasattr(twin, 'predictor') else None,
            twin.history['alerts']
        )
        time.sleep(2)  # Give time to see the changes

if __name__ == "__main__":
    run_demonstration()