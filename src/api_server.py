from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
from datetime import datetime
import json

from .digital_twin import PredictiveDigitalTwin
from .visualization import EnhancedVisualizer

app = FastAPI(title="Digital Twin API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Digital Twin
twin = PredictiveDigitalTwin()
visualizer = EnhancedVisualizer()

# Data Models
class StateUpdate(BaseModel):
    parameter: str
    value: float
    is_physical: bool = True

class SystemState(BaseModel):
    physical_state: Dict[str, float]
    digital_state: Dict[str, float]
    predictions: Optional[Dict[str, List[float]]]
    alerts: List[Dict]
    health_score: float

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Digital Twin Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .controls { margin-bottom: 20px; }
            .parameter { margin: 10px 0; }
            .plots { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .alerts { margin-top: 20px; padding: 10px; background: #f8f8f8; }
            .health-score { font-size: 24px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Digital Twin Dashboard</h1>
            
            <div class="health-score">
                System Health: <span id="health-score">100%</span>
            </div>
            
            <div class="controls">
                <h2>Controls</h2>
                <div class="parameter">
                    <label>Coffee Level:</label>
                    <input type="range" id="coffee_level" min="0" max="100" step="0.1">
                    <span id="coffee_level_value">100%</span>
                </div>
                <div class="parameter">
                    <label>Water Level:</label>
                    <input type="range" id="water_level" min="0" max="100" step="0.1">
                    <span id="water_level_value">100%</span>
                </div>
                <div class="parameter">
                    <label>Temperature:</label>
                    <input type="range" id="temperature" min="0" max="100" step="0.1">
                    <span id="temperature_value">25°C</span>
                </div>
                <div class="parameter">
                    <label>Pressure:</label>
                    <input type="range" id="pressure" min="0" max="2" step="0.01">
                    <span id="pressure_value">1.0 bar</span>
                </div>
                <div class="parameter">
                    <label>Cleanliness:</label>
                    <input type="range" id="cleanliness" min="0" max="100" step="0.1">
                    <span id="cleanliness_value">100%</span>
                </div>
            </div>
            
            <div class="plots">
                <div id="plot1"></div>
                <div id="plot2"></div>
                <div id="plot3"></div>
                <div id="plot4"></div>
            </div>
            
            <div class="alerts">
                <h2>Alerts</h2>
                <div id="alerts-list"></div>
            </div>
        </div>

        <script>
            function updateState(parameter, value) {
                fetch('/update_state', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        parameter: parameter,
                        value: parseFloat(value),
                        is_physical: true
                    })
                })
                .then(response => response.json())
                .then(updateDashboard);
            }

            function updateDashboard(state) {
                // Update health score
                document.getElementById('health-score').textContent = 
                    state.health_score.toFixed(1) + '%';
                
                // Update parameter values
                for (let param in state.physical_state) {
                    const value = state.physical_state[param];
                    document.getElementById(`${param}_value`).textContent = 
                        formatValue(param, value);
                }
                
                // Update plots
                updatePlots(state);
                
                // Update alerts
                const alertsList = document.getElementById('alerts-list');
                alertsList.innerHTML = state.alerts
                    .slice(-5)
                    .map(alert => `<div>${alert.timestamp}: ${alert.message}</div>`)
                    .join('');
            }

            function formatValue(parameter, value) {
                switch(parameter) {
                    case 'temperature':
                        return value.toFixed(1) + '°C';
                    case 'pressure':
                        return value.toFixed(2) + ' bar';
                    default:
                        return value.toFixed(1) + '%';
                }
            }

            function updatePlots(state) {
                // Implementation depends on your visualization needs
                // Example using Plotly:
                Plotly.newPlot('plot1', [{
                    y: state.physical_state.coffee_level,
                    type: 'line',
                    name: 'Coffee Level'
                }]);
                // Add more plots as needed
            }

            // Initialize controls
            document.querySelectorAll('input[type="range"]').forEach(input => {
                input.addEventListener('change', (e) => {
                    updateState(e.target.id, e.target.value);
                });
            });

            // Initial state update
            fetch('/get_state')
                .then(response => response.json())
                .then(updateDashboard);

            // Poll for updates
            setInterval(() => {
                fetch('/get_state')
                    .then(response => response.json())
                    .then(updateDashboard);
            }, 1000);
        </script>
    </body>
    </html>
    """

@app.get("/get_state", response_model=SystemState)
async def get_state():
    """Get current system state"""
    try:
        return {
            "physical_state": twin.physical_state,
            "digital_state": twin.digital_state,
            "predictions": twin.predictor.get_current_predictions(),
            "alerts": twin.history['alerts'],
            "health_score": twin._calculate_health_score()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_state")
async def update_state(update: StateUpdate):
    """Update system state"""
    try:
        twin.update_state(
            update.parameter,
            update.value,
            update.is_physical
        )
        return await get_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def run_server():
    """Run the API server"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()
