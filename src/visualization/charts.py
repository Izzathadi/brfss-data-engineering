# src/visualization/charts.py

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import gaussian_kde
from .utils import calculate_bmi_statistics, format_age_labels, format_correlation_values
from .config import BINARY_FEATURES

def create_diabetes_trend_chart(df):
    """
    Create diabetes trend chart showing cases per year.
    """
    # Group by year and calculate diabetes cases
    diabetes_trend = df.groupby("Year")["Diabetes_01"].sum().reset_index()
    
    # Only show years that have data
    diabetes_trend = diabetes_trend[diabetes_trend["Diabetes_01"] > 0]
    
    fig = px.bar(
        diabetes_trend, 
        x="Year", 
        y="Diabetes_01",
        title="Tren Kasus Diabetes per Tahun",
        labels={"Diabetes_01": "Jumlah Kasus Diabetes"},
        text="Diabetes_01"  # Show values on bars
    )
    
    # Customize the chart
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        width=0.6  # Make bars narrower
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20,
        xaxis=dict(
            tickmode='array',
            tickvals=diabetes_trend["Year"].tolist(),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
        height=500
    )
    
    return fig

def create_binary_features_chart(df, year):
    """
    Create binary features distribution chart with multiple rows.
    """
    dff = df[df["Year"] == year]
    
    # Calculate number of rows and columns for subplot arrangement
    n_features = len(BINARY_FEATURES)
    n_cols = 3  # 3 columns per row
    n_rows = (n_features + n_cols - 1) // n_cols  # Calculate required rows
    
    # Create subplots
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        specs=[[{"type": "pie"} for _ in range(n_cols)] for _ in range(n_rows)],
        subplot_titles=BINARY_FEATURES,
        vertical_spacing=0.15,
        horizontal_spacing=0.05
    )
    
    for i, col in enumerate(BINARY_FEATURES):
        row = i // n_cols + 1
        col_pos = i % n_cols + 1
        
        counts = dff[col].value_counts().to_dict()
        labels = ["Tidak", "Ya"]
        values = [counts.get(0, 0), counts.get(1, 0)]
        
        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                name=col,
                hole=0.4,
                textinfo='percent+label',
                textposition='inside',
                showlegend=False
            ),
            row=row, col=col_pos
        )
    
    fig.update_layout(
        title=f"Distribusi Proporsi Fitur Biner - {year}",
        height=200 * n_rows + 100,  # Adjust height based on number of rows
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20
    )
    
    return fig

def create_sex_pie_chart(df, year):
    """
    Create sex distribution pie chart.
    """
    dff = df[df["Year"] == year]
    counts = dff["Sex"].value_counts()
    labels = ["Pria" if val == 1 else "Wanita" for val in counts.index]
    
    fig = px.pie(
        names=labels, 
        values=counts.values,
        title=f"Proporsi Jenis Kelamin - {year}",
        hole=0.3
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20,
        height=500
    )
    
    return fig

def create_age_pie_chart(df, year):
    """
    Create age distribution pie chart with proper labels.
    """
    dff = df[df["Year"] == year]
    counts = dff["Age"].value_counts()
    
    # Format labels with descriptions
    labels, values = format_age_labels(counts)
    
    fig = px.pie(
        names=labels,
        values=values,
        title=f"Distribusi Umur - {year}",
        hole=0.3
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20,
        height=600,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    return fig

def create_bmi_density_chart(df, year):
    """
    Create BMI density chart with KDE curve and statistics.
    """
    dff = df[df["Year"] == year]
    bmi_data = dff["BMI"].dropna()
    
    if len(bmi_data) == 0:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(title=f"No BMI data available for {year}")
        return fig, {}
    
    # Calculate KDE
    kde = gaussian_kde(bmi_data, bw_method=0.3)
    x_values = np.linspace(bmi_data.min(), bmi_data.max(), 1000)
    y_values = kde(x_values)
    
    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name="KDE Kurva BMI",
        line=dict(color='royalblue', width=3),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title=f"Distribusi Kurva KDE BMI - {year}",
        xaxis_title="BMI",
        yaxis_title="Kepadatan",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20,
        height=500,
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
    )
    
    # Calculate statistics
    stats = calculate_bmi_statistics(bmi_data)
    
    return fig, stats

def create_correlation_heatmap(df, year):
    """
    Create correlation heatmap with formatted values.
    """
    dff = df[df["Year"] == year]
    
    # Get numeric columns excluding Year
    numeric_cols = dff.select_dtypes(include='number').columns
    if "Year" in numeric_cols:
        numeric_cols = numeric_cols.drop("Year")
    
    # Calculate correlation matrix
    corr = dff[numeric_cols].corr()
    corr_formatted = format_correlation_values(corr)
    
    fig = px.imshow(
        corr_formatted,
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu",
        text_auto=True,
        title=f"Korelasi Antar Fitur - {year}",
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=20,
        height=700,  # Make it larger
        width=900
    )
    
    # Update text format to show max 6 decimal places
    fig.update_traces(texttemplate='%{z:.6f}')
    
    return fig
