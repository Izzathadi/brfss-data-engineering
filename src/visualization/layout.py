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
                'color': '#333333',
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
                    'color': '#333333',
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
                    'backgroundColor': '#ffffff',
                    'color': '#000000',
                    'border': '1px solid #ddd'
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

def create_data_statistics_card():
    """Create a card for data statistics table."""
    return html.Div([
        html.H3(
            "Statistik Deskriptif Data",
            style={
                'color': '#333333',
                'marginBottom': '20px',
                'fontSize': '1.5em'
            }
        ),
        html.Div(id="data-stats-table")
    ], style=CARD_STYLE)

def create_feature_description_card():
    """Create a card with feature descriptions."""
    table_data = create_feature_description_table(FEATURE_DESCRIPTIONS)
    
    return html.Div([
        html.H3(
            "Keterangan Fitur Biner",
            style={
                'color': '#333333',
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
                'backgroundColor': '#ffffff',
                'color': '#333333',
                'border': '1px solid #ddd',
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial, sans-serif'
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'color': '#333333',
                'fontWeight': 'bold',
                'border': '1px solid #ddd'
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
            "Statistik BMI (Standarized)",
            style={
                'color': '#333333',
                'marginBottom': '20px',
                'fontSize': '1.5em'
            }
        ),
        html.Div(id="bmi-stats-table")
    ], style=CARD_STYLE)

def create_centered_chart_card(chart_id):
    """Create a card container for charts with centered content."""
    return html.Div([
        dcc.Graph(id=chart_id)
    ], style=CARD_STYLE)

def create_main_layout(available_years):
    """Create the main dashboard layout."""
    return html.Div([
        create_header(),
        create_year_selector(available_years),
        
        # Charts in cards
        create_chart_card("trend-diabetes-graph"),
        
        # NEW: Data statistics table
        create_data_statistics_card(),
        
        # NEW: Diabetes comparison bar chart
        create_chart_card("diabetes-comparison-graph"),
        
        create_chart_card("dist-pie-graph"),
        create_feature_description_card(),
        
        # Side by side charts with equal sizing
        html.Div([
            html.Div([
                create_chart_card("sex-pie-graph")
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                create_chart_card("age-pie-graph")
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'width': '100%'}),
        
        create_chart_card("bmi-density-graph"),
        create_bmi_statistics_card(),
        
        # Correlation heatmap in normal card
        create_chart_card("correlation-heatmap"),
        
    ], style=CONTAINER_STYLE)

def format_bmi_statistics_table(stats):
    """Format BMI statistics as a table."""
    if not stats:
        return html.Div("No BMI data available", style={'color': '#333333'})
    
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
            'backgroundColor': '#ffffff',
            'color': '#333333',
            'border': '1px solid #ddd',
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial, sans-serif'
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'color': '#333333',
            'fontWeight': 'bold',
            'border': '1px solid #ddd'
        }
    )

def format_data_statistics_table(stats):
    """Format comprehensive data statistics as a table."""
    if not stats:
        return html.Div("No data available", style={'color': '#333333'})
    
    table_data = []
    
    # Basic information
    table_data.extend([
        {"Kategori": "Informasi Dasar", "Statistik": "Total Baris", "Nilai": f"{stats.get('total_rows', 0):,}"},
        {"Kategori": "Informasi Dasar", "Statistik": "Total Kolom", "Nilai": f"{stats.get('total_columns', 0):,}"},
        {"Kategori": "Informasi Dasar", "Statistik": "Kolom Numerik", "Nilai": f"{stats.get('numeric_columns', 0):,}"},
        {"Kategori": "Informasi Dasar", "Statistik": "Kolom Kategorikal", "Nilai": f"{stats.get('categorical_columns', 0):,}"},
        {"Kategori": "Informasi Dasar", "Statistik": "Ukuran File (KB)", "Nilai": f"{stats.get('file_size_mb', 0):.2f}"},
    ])
    
    # Missing values
    table_data.extend([
        {"Kategori": "Data Hilang", "Statistik": "Total Data Hilang", "Nilai": f"{stats.get('total_missing', 0):,}"},
        {"Kategori": "Data Hilang", "Statistik": "Persentase Data Hilang", "Nilai": f"{stats.get('missing_percentage', 0):.2f}%"},
        {"Kategori": "Data Hilang", "Statistik": "Baris Duplikat", "Nilai": f"{stats.get('duplicate_rows', 0):,}"},
    ])
    
    # Diabetes statistics
    if 'diabetes_cases' in stats:
        table_data.extend([
            {"Kategori": "Diabetes", "Statistik": "Kasus Diabetes", "Nilai": f"{stats.get('diabetes_cases', 0):,}"},
            {"Kategori": "Diabetes", "Statistik": "Kasus Non-Diabetes", "Nilai": f"{stats.get('non_diabetes_cases', 0):,}"},
            {"Kategori": "Diabetes", "Statistik": "Persentase Diabetes", "Nilai": f"{stats.get('diabetes_percentage', 0):.2f}%"},
        ])
    
    # Age statistics
    if 'age_mean' in stats:
        table_data.extend([
            {"Kategori": "Umur", "Statistik": "Rata-rata Kategori Umur", "Nilai": f"{stats.get('age_mean', 0):.2f}"},
            {"Kategori": "Umur", "Statistik": "Median Kategori Umur", "Nilai": f"{stats.get('age_median', 0):.2f}"},
            {"Kategori": "Umur", "Statistik": "Std Dev Kategori Umur", "Nilai": f"{stats.get('age_std', 0):.2f}"},
        ])
    
    # BMI statistics
    if 'bmi_mean' in stats:
        table_data.extend([
            {"Kategori": "BMI", "Statistik": "Rata-rata BMI", "Nilai": f"{stats.get('bmi_mean', 0):.2f}"},
            {"Kategori": "BMI", "Statistik": "Median BMI", "Nilai": f"{stats.get('bmi_median', 0):.2f}"},
            {"Kategori": "BMI", "Statistik": "Std Dev BMI", "Nilai": f"{stats.get('bmi_std', 0):.2f}"},
            {"Kategori": "BMI", "Statistik": "Data BMI Hilang", "Nilai": f"{stats.get('bmi_missing', 0):,}"},
        ])
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {"name": "Kategori", "id": "Kategori"},
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
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{Kategori} = "Informasi Dasar"'},
                'backgroundColor': '#1a4d80',
            },
            {
                'if': {'filter_query': '{Kategori} = "Data Hilang"'},
                'backgroundColor': '#802d2d',
            },
            {
                'if': {'filter_query': '{Kategori} = "Diabetes"'},
                'backgroundColor': '#2d8054',
            },
            {
                'if': {'filter_query': '{Kategori} = "Umur"'},
                'backgroundColor': '#804d2d',
            },
            {
                'if': {'filter_query': '{Kategori} = "BMI"'},
                'backgroundColor': '#5c2d80',
            }
        ],
        merge_duplicate_headers=True
    )