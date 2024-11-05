# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
import ipywidgets as widgets
from IPython.display import display, clear_output

class EnhancedVisualizer:
    """Enhanced visualization system for digital twin with larger plots"""
    
    def __init__(self):
        # Set style with enhanced visuals
        sns.set_style("darkgrid")
        self.colors = {
            'physical': '#1f77b4',  # Blue
            'digital': '#ff7f0e',   # Orange
            'prediction': '#2ca02c', # Green
            'alert': '#d62728',     # Red
            'health': '#9467bd'     # Purple
        }
        
        # Configure default plot settings
        plt.rcParams.update({
            'figure.figsize': (24, 16),
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 12,
            'lines.linewidth': 2
        })
    
    def plot_state(self,
                  physical_state: Dict[str, float],
                  digital_state: Dict[str, float],
                  history: Dict,
                  predictions: Optional[Dict] = None,
                  alerts: Optional[List] = None) -> None:
        """
        Create enhanced visualization of system state with larger plots
        """
        # Create figure with larger size
        fig = plt.figure(figsize=(24, 16))
        
        # Create grid with better spacing
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.7], hspace=0.3, wspace=0.2)
        
        # Parameter plots with enhanced visibility
        for i, param in enumerate(physical_state.keys()):
            if i < 4:  # First four parameters
                ax = fig.add_subplot(gs[i//2, i%2])
            else:  # Last parameter gets wider plot
                ax = fig.add_subplot(gs[-1, 0])
            self._plot_parameter(ax, param, history, predictions)
        
        # Alerts in larger format
        ax_alerts = fig.add_subplot(gs[-1, 1])
        self._plot_alerts(ax_alerts, alerts)
        
        plt.tight_layout()
        plt.show()
    
    def _plot_parameter(self, ax, parameter: str, history: Dict, 
                       predictions: Optional[Dict]) -> None:
        """Enhanced parameter plotting with better visibility"""
        # Historical data with thicker lines
        times = history['timestamps']
        ax.plot(times, history['physical'][parameter], 
                label='Physical', color=self.colors['physical'],
                linewidth=2.5)
        ax.plot(times, history['digital'][parameter], 
                label='Digital', color=self.colors['digital'], 
                linestyle='--', linewidth=2.5)
        
        # Enhanced predictions
        if predictions and parameter in predictions:
            pred_times = [times[-1] + timedelta(minutes=x) 
                         for x in range(len(predictions[parameter]))]
            
            # Prediction line
            ax.plot(pred_times, predictions[parameter], 
                   label='Prediction', color=self.colors['prediction'], 
                   linestyle=':', linewidth=2.5)
            
            # Enhanced confidence intervals
            if 'confidence' in predictions:
                ax.fill_between(pred_times,
                              predictions['confidence'][parameter]['lower'],
                              predictions['confidence'][parameter]['upper'],
                              color=self.colors['prediction'], 
                              alpha=0.2,
                              label='Confidence Interval')
        
        # Enhanced styling
        title = parameter.replace('_', ' ').title()
        ax.set_title(title, pad=20, fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Parameter-specific formatting with enhanced ranges
        if parameter in ['coffee_level', 'water_level', 'cleanliness']:
            ax.set_ylim(-5, 105)  # Slightly expanded range
            ax.set_ylabel('Percentage (%)', fontsize=14)
        elif parameter == 'temperature':
            ax.set_ylim(15, 100)  # Appropriate temperature range
            ax.set_ylabel('Temperature (°C)', fontsize=14)
        elif parameter == 'pressure':
            ax.set_ylim(0, 2.5)  # Appropriate pressure range
            ax.set_ylabel('Pressure (bar)', fontsize=14)
        
        # Enhanced legend
        ax.legend(loc='upper right', framealpha=0.95, shadow=True)
        
        # Better tick formatting
        ax.tick_params(axis='both', which='major', labelsize=12)
    
    def _plot_alerts(self, ax, alerts: Optional[List]) -> None:
        """Enhanced alert visualization"""
        ax.set_title('System Alerts & Warnings', fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        if alerts:
            recent_alerts = alerts[-5:]  # Last 5 alerts
            alert_texts = []
            
            for alert in recent_alerts:
                time_str = alert['timestamp'].strftime('%H:%M:%S')
                alert_type = alert.get('type', 'INFO')
                color = 'red' if alert_type == 'critical' else 'orange' if alert_type == 'warning' else 'blue'
                
                alert_texts.append(f"[{time_str}] {alert['message']}")
            
            alert_text = '\n\n'.join(alert_texts)
            ax.text(0.05, 0.95, alert_text,
                   transform=ax.transAxes,
                   verticalalignment='top',
                   fontsize=13,
                   bbox=dict(facecolor='white', 
                            alpha=0.8,
                            edgecolor='gray',
                            boxstyle='round,pad=1'))
    
    def create_interactive_dashboard(self, twin) -> None:
        """Create enhanced interactive dashboard"""
        # Create styled controls
        controls = {}
        for param in twin.physical_state:
            max_val = 2 if param == 'pressure' else 100
            controls[param] = widgets.FloatSlider(
                description=param,
                value=twin.physical_state[param],
                min=0,
                max=max_val,
                step=0.1,
                style={'description_width': '120px'},
                layout=widgets.Layout(width='600px'),
                continuous_update=False
            )
        
        # Styled buttons
        btn_style = {'button_color': '#4CAF50', 'font_weight': 'bold'}
        update_btn = widgets.Button(
            description="Update System",
            style=btn_style,
            layout=widgets.Layout(width='200px')
        )
        reset_btn = widgets.Button(
            description="Reset System",
            style={'button_color': '#f44336', 'font_weight': 'bold'},
            layout=widgets.Layout(width='200px')
        )
        
        # Status indicator
        status = widgets.HTML(
            value='<h3>System Status: <span style="color: green;">Operational</span></h3>'
        )
        
        def update_status():
            health = twin.get_health_score() if hasattr(twin, 'get_health_score') else 100
            color = 'green' if health > 80 else 'orange' if health > 50 else 'red'
            status.value = f'<h3>System Status: <span style="color: {color};">Health: {health:.1f}%</span></h3>'
        
        def on_update(b):
            clear_output(wait=True)
            for param, control in controls.items():
                twin.update_state(param, control.value)
            update_status()
            self.plot_state(
                twin.physical_state,
                twin.digital_state,
                twin.history,
                twin.predictor.get_current_predictions() if hasattr(twin, 'predictor') else None,
                twin.history['alerts']
            )
            display(widgets.VBox([
                status,
                widgets.HBox([update_btn, reset_btn]),
                *controls.values()
            ]))
        
        def on_reset(b):
            clear_output(wait=True)
            twin.__init__()
            update_status()
            self.plot_state(
                twin.physical_state,
                twin.digital_state,
                twin.history
            )
            display(widgets.VBox([
                status,
                widgets.HBox([update_btn, reset_btn]),
                *controls.values()
            ]))
        
        update_btn.on_click(on_update)
        reset_btn.on_click(on_reset)
        
        # Initial display
        display(widgets.VBox([
            status,
            widgets.HBox([update_btn, reset_btn]),
            *controls.values()
        ]))
        self.plot_state(
            twin.physical_state,
            twin.digital_state,
            twin.history
        )

# Usage example:
# visualizer = EnhancedVisualizer()
# visualizer.create_interactive_dashboard(twin)
