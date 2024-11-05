def test_imports():
    """Test that all necessary imports work"""
    try:
        # Test core imports
        from digital_twin import PredictiveDigitalTwin
        from visualization import EnhancedVisualizer
        import matplotlib.pyplot as plt
        print("✓ Core imports successful")

        # Create instances
        twin = PredictiveDigitalTwin()
        visualizer = EnhancedVisualizer()
        print("✓ Class instantiation successful")

        return True

    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_imports()
    print(f"\nImport test {'passed' if success else 'failed'}")