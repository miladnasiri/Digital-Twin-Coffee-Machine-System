import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from visualization import EnhancedVisualizer

def run_simple_test():
    """Run a simple visualization test"""
    print("Starting simple visualization test...")
    
    try:
        # Create test data
        now = datetime.now()
        test_data = {
            'physical_state': {
                'coffee_level': 80.0,
                'water_level': 75.0,
                'temperature': 85.0,
                'pressure': 1.2,
                'cleanliness': 90.0
            },
            'digital_state': {
                'coffee_level': 79.0,
                'water_level': 74.0,
                'temperature': 84.0,
                'pressure': 1.18,
                'cleanliness': 89.0
            },
            'history': {
                'physical': {
                    'coffee_level': [80, 85, 90],
                    'water_level': [75, 80, 85],
                    'temperature': [85, 84, 83],
                    'pressure': [1.2, 1.1, 1.0],
                    'cleanliness': [90, 92, 94]
                },
                'digital': {
                    'coffee_level': [79, 84, 89],
                    'water_level': [74, 79, 84],
                    'temperature': [84, 83, 82],
                    'pressure': [1.18, 1.08, 0.98],
                    'cleanliness': [89, 91, 93]
                },
                'timestamps': [now - timedelta(minutes=2), 
                             now - timedelta(minutes=1), 
                             now]
            },
            'alerts': [
                {
                    'timestamp': now,
                    'message': 'Test Alert',
                    'type': 'warning'
                }
            ]
        }
        
        print("Created test data")
        
        # Create visualizer
        viz = EnhancedVisualizer()
        print("Created visualizer")
        
        # Test plot
        viz.plot_state(
            physical_state=test_data['physical_state'],
            digital_state=test_data['digital_state'],
            history=test_data['history'],
            alerts=test_data['alerts']
        )
        print("Successfully created plot!")
        
        plt.show()
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        raise

if __name__ == "__main__":
    run_simple_test()