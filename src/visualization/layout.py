# src/visualization/layout.py

from dash import dcc, html, dash_table
from .config import DASHBOARD_TITLE, FEATURE_DESCRIPTIONS, CONTAINER_STYLE, CARD_STYLE
from .utils import create_feature_description_table

def create_header():
    """Create the dashboard header."""
    return html.Div([
        html.H1(
            f"📊 {DASHBOARD_TITLE}",
            style={
                'textAlign': 'center',
                'color': '#ffffff',
                'marginBottom': '30px',
                'fontSize': '2.5em',
                'fontWeight': 'bold'
            }
        )
    ])

def create_year_selector(available_years):
    """Create the year selection dropdown."""
    return html.Div([
        html.Div([
            html.Label(
                "Pilih Tahun:",
                style={
                    'color': '#ffffff',
                    'fontSize': '1.2em',
                    'marginBottom': '10px',
                    'display': 'block'
                }
            ),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(y), "value": y} for y in available_years],
                value=available_years[-1] if available_years else None,
                style={
                    'backgroundColor': '#f5f5f5',
                    'color': '#000000',
                    'border': '1px solid #444'
                }
            ),
        ], style={
            'width': '300px',
            'margin': '0 auto 30px auto'
        })
    ])

def create_chart_card(chart_id, title=None):
    """Create a card container for charts."""
    return html.Div([
        dcc.Graph(id=chart_id)
    ], style=CARD_STYLE)

def create_feature_description_card():
    """Create a card with feature descriptions."""
    table_data = create_feature_description_table(FEATURE_DESCRIPTIONS)
    
    return html.Div([
        html.H3(
            "Keterangan Fitur Biner",
            style={
                'color': '#ffffff',
                'marginBottom': '20px',
                'fontSize': '1.5em'
            }
        ),
        dash_table.DataTable(
            data=[{"Feature": row[0], "Description": row[1]} for row in table_data],
            columns=[
                {"name": "Fitur", "id": "Feature"},
                {"name": "Deskripsi", "id": "Description"}
            ],
            style_cell={
                'backgroundColor': '#2d2d2d',
                'color': '#ffffff',
                'border': '1px solid #444',
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial, sans-serif'
            },
            style_header={
                'backgroundColor': '#1e1e1e',
                'color': '#ffffff',
                'fontWeight': 'bold',
                'border': '1px solid #444'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            }
        )
    ], style=CARD_STYLE)

def create_bmi_statistics_card():
    """Create a card for BMI statistics."""
    return html.Div([
        html.H3(
            "Statistik BMI",
            style={
                'color': '#ffffff',
                'marginBottom': '20px',
                'fontSize': '1.5em'
            }
        ),
        html.Div(id="bmi-stats-table")
    ], style=CARD_STYLE)

def create_main_layout(available_years):
    """Create the main dashboard layout."""
    return html.Div([
        create_header(),
        create_year_selector(available_years),
        
        # Charts in cards
        create_chart_card("trend-diabetes-graph"),
        create_chart_card("dist-pie-graph"),
        create_feature_description_card(),
        
        html.Div([
            html.Div([
                create_chart_card("sex-pie-graph")
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                create_chart_card("age-pie-graph")
            ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ]),
        
        create_chart_card("bmi-density-graph"),
        create_bmi_statistics_card(),
        create_chart_card("correlation-heatmap"),
        
    ], style=CONTAINER_STYLE)

def format_bmi_statistics_table(stats):
    """Format BMI statistics as a table."""
    if not stats:
        return html.Div("No BMI data available", style={'color': '#ffffff'})
    
    table_data = [
        {"Statistik": "Mean (Rata-rata)", "Nilai": f"{stats['mean']:.2f}"},
        {"Statistik": "Standard Deviation", "Nilai": f"{stats['std']:.2f}"},
        {"Statistik": "Skewness", "Nilai": f"{stats['skewness']:.6f}"},
        {"Statistik": "Kurtosis", "Nilai": f"{stats['kurtosis']:.6f}"},
        {"Statistik": "Minimum", "Nilai": f"{stats['min']:.2f}"},
        {"Statistik": "Maximum", "Nilai": f"{stats['max']:.2f}"},
        {"Statistik": "Jumlah Data", "Nilai": f"{stats['count']:,}"}
    ]
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {"name": "Statistik", "id": "Statistik"},
            {"name": "Nilai", "id": "Nilai"}
        ],
        style_cell={
            'backgroundColor': '#2d2d2d',
            'color': '#ffffff',
            'border': '1px solid #444',
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial, sans-serif'
        },
        style_header={
            'backgroundColor': '#1e1e1e',
            'color': '#ffffff',
            'fontWeight': 'bold',
            'border': '1px solid #444'
        }
    )
