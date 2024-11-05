from src.digital_twin import PredictiveDigitalTwin
from src.visualization import EnhancedVisualizer
import time

def test_system():
    """Test if the system is working properly"""
    print("Initializing Digital Twin...")
    twin = PredictiveDigitalTwin()
    
    print("Creating visualizer...")
    visualizer = EnhancedVisualizer()
    
    print("Testing state updates...")
    parameters = ['coffee_level', 'water_level', 'temperature', 'pressure', 'cleanliness']
    for param in parameters:
        print(f"Testing {param}...")
        twin.update_state(param, 50.0)
        
    print("System test complete!")
    return twin, visualizer

if __name__ == "__main__":
    twin, visualizer = test_system()
    print("\nCurrent State:")
    print("Physical:", twin.physical_state)
    print("Digital:", twin.digital_state)
