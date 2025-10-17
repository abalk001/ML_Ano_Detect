import pandas as pd
import plotly.graph_objects as go
import os

# Load the engine data
DATA_PATH = './data/CMaps/'
df = pd.read_csv(f'{DATA_PATH}train_FD001.txt', sep='\s+', header=None)
columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]
df.columns = columns

# Filter data for engine 5
engine_df = df[df['engine_id'] == 5]

if not engine_df.empty and 'sensor_3' in engine_df.columns:
    # Create Plotly chart for sensor 3 in engine 5
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=engine_df['cycle'],
        y=engine_df['sensor_3'],
        mode='lines+markers',
        name='Sensor 3',
        line=dict(color='red', width=2),
        marker=dict(size=4, color='darkred')
    ))
    
    # Add trend line
    import numpy as np
    z = np.polyfit(engine_df['cycle'], engine_df['sensor_3'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=engine_df['cycle'],
        y=p(engine_df['cycle']),
        mode='lines',
        name='Trend Line',
        line=dict(color='blue', width=1, dash='dash')
    ))
    
    # Calculate some statistics
    max_val = engine_df['sensor_3'].max()
    min_val = engine_df['sensor_3'].min()
    mean_val = engine_df['sensor_3'].mean()
    
    fig.update_layout(
        title=f'Sensor 3 Data for Engine 5<br><sub>Max: {max_val:.3f} | Min: {min_val:.3f} | Mean: {mean_val:.3f}</sub>',
        xaxis_title='Cycle',
        yaxis_title='Sensor 3 Value',
        template='plotly_white',
        width=800,
        height=500,
        hovermode='x unified'
    )
    
    # Add annotations for key points
    fig.add_annotation(
        x=engine_df['cycle'].iloc[-1],
        y=engine_df['sensor_3'].iloc[-1],
        text=f"Final Value: {engine_df['sensor_3'].iloc[-1]:.3f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red"
    )
    
    # Save chart
    chart_dir = 'chart'
    os.makedirs(chart_dir, exist_ok=True)
    filename = 'sensor_3_engine_5.html'
    filepath = os.path.join(chart_dir, filename)
    fig.write_html(filepath)
    
    print(f"✅ Chart generated successfully: {filename}")
    print(f"📊 Engine 5 - Sensor 3 Analysis:")
    print(f"   • Total cycles: {len(engine_df)}")
    print(f"   • Sensor 3 range: {min_val:.3f} to {max_val:.3f}")
    print(f"   • Average value: {mean_val:.3f}")
    print(f"   • Final value: {engine_df['sensor_3'].iloc[-1]:.3f}")
    
else:
    print("❌ Error: Engine 5 data not found or sensor_3 column missing")