import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from visualization import EnhancedVisualizer

def create_test_data():
    """Create test data for visualization"""
    physical_state = {
        'coffee_level': 75.0,
        'water_level': 80.0,
        'temperature': 85.0,
        'pressure': 1.2,
        'cleanliness': 90.0
    }
    
    digital_state = {
        'coffee_level': 74.5,
        'water_level': 79.5,
        'temperature': 84.5,
        'pressure': 1.18,
        'cleanliness': 89.5
    }
    
    # Create history
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(10)]
    timestamps.reverse()
    
    history = {
        'physical': {
            param: list(np.linspace(50, val, 10))
            for param, val in physical_state.items()
        },
        'digital': {
            param: list(np.linspace(50, val, 10))
            for param, val in digital_state.items()
        },
        'timestamps': timestamps,
        'alerts': [
            {
                'timestamp': datetime.now(),
                'message': 'Test Alert 1',
                'type': 'warning'
            },
            {
                'timestamp': datetime.now() - timedelta(minutes=1),
                'message': 'Test Alert 2',
                'type': 'critical'
            }
        ]
    }
    
    return physical_state, digital_state, history

def test_visualization():
    """Test visualization functionality"""
    print("Testing visualization system...")
    
    # Create visualizer
    visualizer = EnhancedVisualizer()
    print("✓ Visualizer created")
    
    # Create test data
    physical_state, digital_state, history = create_test_data()
    print("✓ Test data created")
    
    # Test plot_state
    try:
        visualizer.plot_state(
            physical_state=physical_state,
            digital_state=digital_state,
            history=history,
            predictions=None,
            alerts=history['alerts']
        )
        print("✓ Plot state successful")
    except Exception as e:
        print(f"✗ Plot state failed: {str(e)}")
        
    plt.close('all')  # Clean up plots
    
    print("\nVisualization test complete!")

if __name__ == "__main__":
    test_visualization()