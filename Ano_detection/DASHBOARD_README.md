# Engine Analytics Dashboard

## Overview
This is an AI-powered dashboard that generates visualizations based on natural language prompts. The system uses an LLM (you, the assistant) to interpret user requests and create appropriate charts.

## Features
- **Natural Language Chart Generation**: Users can request charts using plain English
- **Interactive Visualizations**: Charts are generated using Plotly for interactivity
- **Chart Storage**: All generated charts are stored in the `chart/` directory
- **Real-time Dashboard**: Web interface that displays all generated charts

## Architecture

### Components
1. **dashboard_app.py**: Main Flask application with chart generation logic
2. **chart/**: Directory containing generated visualization files
3. **templates/dashboard.html**: Web interface for the dashboard
4. **server.py**: Original ML prediction API (separate from dashboard)
5. **client.py**: Client for the ML prediction API

### How It Works
1. User enters a prompt like "plot sensor 1 in engine 2"
2. The Flask app processes the prompt and extracts relevant information
3. Based on the prompt, the appropriate chart generation function is called
4. Chart is saved as an HTML file in the `chart/` directory
5. Dashboard refreshes to show the new chart

## Usage

### Starting the Dashboard
```bash
cd /home/dora/Desktop/ML_Ano_Detect/Ano_detection
python dashboard_app.py
```

The dashboard will be available at: `http://127.0.0.1:5001`

### Example Prompts
- "plot sensor 1 in engine 2" → Generates a line chart of sensor 1 data for engine 2
- "show me sensor 3 overview" → Shows sensor 3 across multiple engines
- "engine 5 overview" → Displays key sensors for engine 5
- "show engine lifespan distribution" → Creates a histogram of engine lifespans

### Supported Chart Types
1. **Sensor-Engine Specific**: Charts for a specific sensor in a specific engine
2. **Sensor Overview**: Charts showing a sensor across multiple engines
3. **Engine Overview**: Charts showing multiple sensors for one engine
4. **Default Charts**: General analytics like lifespan distribution

## File Structure
```
/home/dora/Desktop/ML_Ano_Detect/Ano_detection/
├── dashboard_app.py          # Main dashboard application
├── server.py                 # ML prediction API
├── client.py                 # API client
├── chart/                    # Generated charts directory
│   ├── README.md
│   └── *.html               # Generated Plotly charts
├── templates/
│   └── dashboard.html       # Dashboard web interface
├── data/CMaps/              # Engine sensor data
└── requirements.txt         # Python dependencies
```

## Adding New Chart Types

To add new chart types, modify the `process_prompt_and_generate_chart()` function in `dashboard_app.py`:

1. Add regex patterns to detect new prompt types
2. Create new chart generation functions
3. Return the filename of the generated chart

Example:
```python
def generate_custom_chart():
    # Your chart generation logic here
    fig = go.Figure(...)
    fig.write_html('custom_chart.html')
    return 'custom_chart.html'
```

## LLM Integration
As an LLM, you can:
1. Analyze user prompts to determine what visualization they want
2. Modify the chart generation functions to create better visualizations
3. Add new chart types by updating the prompt processing logic
4. Improve the natural language understanding

## Dependencies
- Flask: Web framework
- Plotly: Interactive visualizations
- Pandas: Data manipulation
- NumPy: Numerical operations
- Matplotlib: Static plotting (optional)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Testing the System
1. Start the dashboard: `python dashboard_app.py`
2. Open browser to `http://127.0.0.1:5001`
3. Try example prompts to generate charts
4. Check the `chart/` directory to see generated files
5. Charts should appear on the dashboard automatically

## Next Steps
- Add more sophisticated prompt parsing
- Support for more complex visualizations
- Integration with the ML prediction model
- User authentication and chart sharing
- Export capabilities for generated charts