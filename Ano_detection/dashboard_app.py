from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re

app = Flask(__name__)

# Configuration
CHART_DIRECTORY = 'chart'
DATA_PATH = './data/CMaps/'

# Load data for chart generation
def load_data():
    """Load the engine data for chart generation"""
    try:
        # Load training data
        df = pd.read_csv(f'{DATA_PATH}train_FD001.txt', delim_whitespace=True, header=None)
        columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]
        df.columns = columns
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Global data variable
engine_data = load_data()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    charts = get_chart_list()
    return render_template('dashboard.html', charts=charts)

@app.route('/charts')
def get_chart_list():
    """Get list of available charts"""
    charts = []
    if os.path.exists(CHART_DIRECTORY):
        for filename in os.listdir(CHART_DIRECTORY):
            if filename.endswith(('.html', '.png', '.jpg', '.jpeg')):
                charts.append({
                    'name': filename,
                    'path': filename,
                    'type': filename.split('.')[-1]
                })
    return charts

@app.route('/chart/<filename>')
def serve_chart(filename):
    """Serve chart files"""
    return send_from_directory(CHART_DIRECTORY, filename)

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    """Generate chart based on user prompt"""
    try:
        prompt = request.json.get('prompt', '')
        chart_path = process_prompt_and_generate_chart(prompt)
        
        if chart_path:
            return jsonify({
                'success': True,
                'chart_path': chart_path,
                'message': f'Chart generated successfully: {chart_path}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not generate chart from prompt'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating chart: {str(e)}'
        })

def process_prompt_and_generate_chart(prompt):
    """Process user prompt and generate appropriate chart"""
    prompt = prompt.lower()
    
    # Extract sensor and engine information from prompt
    sensor_match = re.search(r'sensor[_\s]*(\d+)', prompt)
    engine_match = re.search(r'engine[_\s]*(\d+)', prompt)
    
    if sensor_match and engine_match:
        sensor_num = int(sensor_match.group(1))
        engine_id = int(engine_match.group(1))
        return generate_sensor_chart(sensor_num, engine_id)
    elif sensor_match:
        sensor_num = int(sensor_match.group(1))
        return generate_sensor_overview_chart(sensor_num)
    elif engine_match:
        engine_id = int(engine_match.group(1))
        return generate_engine_overview_chart(engine_id)
    else:
        # Default chart
        return generate_default_chart()

def generate_sensor_chart(sensor_num, engine_id):
    """Generate chart for specific sensor and engine"""
    if engine_data is None:
        return None
    
    # Filter data for specific engine
    engine_df = engine_data[engine_data['engine_id'] == engine_id]
    
    if engine_df.empty:
        return None
    
    sensor_col = f'sensor_{sensor_num}'
    if sensor_col not in engine_df.columns:
        return None
    
    # Create Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=engine_df['cycle'],
        y=engine_df[sensor_col],
        mode='lines+markers',
        name=f'Sensor {sensor_num}',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title=f'Sensor {sensor_num} Data for Engine {engine_id}',
        xaxis_title='Cycle',
        yaxis_title=f'Sensor {sensor_num} Value',
        template='plotly_white',
        width=800,
        height=500
    )
    
    # Save chart
    filename = f'sensor_{sensor_num}_engine_{engine_id}.html'
    filepath = os.path.join(CHART_DIRECTORY, filename)
    fig.write_html(filepath)
    
    return filename

def generate_sensor_overview_chart(sensor_num):
    """Generate overview chart for a sensor across multiple engines"""
    if engine_data is None:
        return None
    
    sensor_col = f'sensor_{sensor_num}'
    if sensor_col not in engine_data.columns:
        return None
    
    # Sample first 5 engines for overview
    sample_engines = engine_data['engine_id'].unique()[:5]
    
    fig = go.Figure()
    
    for engine_id in sample_engines:
        engine_df = engine_data[engine_data['engine_id'] == engine_id]
        fig.add_trace(go.Scatter(
            x=engine_df['cycle'],
            y=engine_df[sensor_col],
            mode='lines',
            name=f'Engine {engine_id}',
            opacity=0.7
        ))
    
    fig.update_layout(
        title=f'Sensor {sensor_num} Overview (First 5 Engines)',
        xaxis_title='Cycle',
        yaxis_title=f'Sensor {sensor_num} Value',
        template='plotly_white',
        width=800,
        height=500
    )
    
    filename = f'sensor_{sensor_num}_overview.html'
    filepath = os.path.join(CHART_DIRECTORY, filename)
    fig.write_html(filepath)
    
    return filename

def generate_engine_overview_chart(engine_id):
    """Generate overview chart for a specific engine showing multiple sensors"""
    if engine_data is None:
        return None
    
    engine_df = engine_data[engine_data['engine_id'] == engine_id]
    
    if engine_df.empty:
        return None
    
    # Select key sensors for overview
    key_sensors = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4']
    
    fig = go.Figure()
    
    for sensor in key_sensors:
        if sensor in engine_df.columns:
            fig.add_trace(go.Scatter(
                x=engine_df['cycle'],
                y=engine_df[sensor],
                mode='lines',
                name=sensor.replace('_', ' ').title()
            ))
    
    fig.update_layout(
        title=f'Engine {engine_id} - Key Sensors Overview',
        xaxis_title='Cycle',
        yaxis_title='Sensor Values',
        template='plotly_white',
        width=800,
        height=500
    )
    
    filename = f'engine_{engine_id}_overview.html'
    filepath = os.path.join(CHART_DIRECTORY, filename)
    fig.write_html(filepath)
    
    return filename

def generate_default_chart():
    """Generate a default chart"""
    if engine_data is None:
        return None
    
    # Engine lifespan distribution
    engine_cycles = engine_data.groupby('engine_id')['cycle'].max()
    
    fig = go.Figure(data=[go.Histogram(x=engine_cycles, nbinsx=20)])
    fig.update_layout(
        title='Engine Lifespan Distribution',
        xaxis_title='Engine Lifespan (cycles)',
        yaxis_title='Frequency',
        template='plotly_white',
        width=800,
        height=500
    )
    
    filename = 'engine_lifespan_distribution.html'
    filepath = os.path.join(CHART_DIRECTORY, filename)
    fig.write_html(filepath)
    
    return filename

if __name__ == '__main__':
    # Ensure chart directory exists
    os.makedirs(CHART_DIRECTORY, exist_ok=True)
    app.run(debug=True, port=5001)