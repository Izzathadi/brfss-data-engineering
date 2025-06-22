# src/visualization/app.py

from dash import Dash, Input, Output, html
from .data_loader import load_data, get_available_years
from .layout import create_main_layout, format_bmi_statistics_table, format_data_statistics_table
from .charts import (
    create_diabetes_trend_chart,
    create_binary_features_chart,
    create_sex_pie_chart,
    create_age_pie_chart,
    create_bmi_density_chart,
    create_correlation_heatmap,
    create_data_statistics_table,
    create_diabetes_comparison_chart
)
from .config import DASHBOARD_TITLE, DASHBOARD_PORT, CONTAINER_STYLE
import dash

app = dash.Dash(__name__)

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="background-color: #f8f9fa;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Initialize the Dash app
app.title = DASHBOARD_TITLE

# Load data
try:
    df = load_data()
    available_years = get_available_years(df)
    print(f"Dashboard initialized with data from years: {available_years}")
except Exception as e:
    print(f"Error loading data: {e}")
    df = None
    available_years = []

# Set up the layout
if df is not None and available_years:
    app.layout = create_main_layout(available_years)
else:
    # Error layout if data cannot be loaded
    app.layout = create_error_layout()

def create_error_layout():
    """Create an error layout when data cannot be loaded."""
    return html.Div([
        html.H1("❌ Error Loading Dashboard", style={'textAlign': 'center', 'color': 'red'}),
        html.P("Could not load BRFSS data. Please check if the data files exist in the processed directory.",
               style={'textAlign': 'center', 'color': 'black', 'fontSize': '1.2em'})
    ], style=CONTAINER_STYLE)

# Callback for diabetes trend chart
@app.callback(
    Output("trend-diabetes-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_diabetes_trend(_):
    """Update diabetes trend chart (shows all years regardless of selected year)."""
    if df is None:
        return {}
    return create_diabetes_trend_chart(df)

# NEW: Callback for data statistics table
@app.callback(
    Output("data-stats-table", "children"),
    Input("year-dropdown", "value")
)
def update_data_statistics(year):
    """Update data statistics table for selected year."""
    if df is None or year is None:
        return "No data available"
    
    stats = create_data_statistics_table(df, year)
    return format_data_statistics_table(stats)

# NEW: Callback for diabetes comparison bar chart
@app.callback(
    Output("diabetes-comparison-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_diabetes_comparison(year):
    """Update diabetes comparison bar chart for selected year."""
    if df is None or year is None:
        return {}
    return create_diabetes_comparison_chart(df, year)

# Callback for binary features distribution
@app.callback(
    Output("dist-pie-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_distribution_pie(year):
    """Update binary features distribution chart."""
    if df is None or year is None:
        return {}
    return create_binary_features_chart(df, year)

# Callback for sex distribution
@app.callback(
    Output("sex-pie-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_sex_pie(year):
    """Update sex distribution pie chart."""
    if df is None or year is None:
        return {}
    return create_sex_pie_chart(df, year)

# Callback for age distribution
@app.callback(
    Output("age-pie-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_age_pie(year):
    """Update age distribution pie chart."""
    if df is None or year is None:
        return {}
    return create_age_pie_chart(df, year)

# Callback for BMI density chart
@app.callback(
    Output("bmi-density-graph", "figure"),
    Input("year-dropdown", "value")
)
def update_bmi_density(year):
    """Update BMI density chart."""
    if df is None or year is None:
        return {}
    fig, _ = create_bmi_density_chart(df, year)
    return fig

# Callback for BMI statistics table
@app.callback(
    Output("bmi-stats-table", "children"),
    Input("year-dropdown", "value")
)
def update_bmi_statistics(year):
    """Update BMI statistics table."""
    if df is None or year is None:
        return "No data available"
    
    _, stats = create_bmi_density_chart(df, year)
    return format_bmi_statistics_table(stats)

# Callback for correlation heatmap
@app.callback(
    Output("correlation-heatmap", "figure"),
    Input("year-dropdown", "value")
)
def update_correlation(year):
    """Update correlation heatmap."""
    if df is None or year is None:
        return {}
    return create_correlation_heatmap(df, year)

if __name__ == "__main__":
    if df is not None:
        print(f"Starting dashboard on port {DASHBOARD_PORT}")
        print(f"Available years: {available_years}")
        app.run(debug=True, port=DASHBOARD_PORT)
    else:
        print("Cannot start dashboard: No data loaded")
        print("Please ensure the processed data files exist in the data/processed directory")