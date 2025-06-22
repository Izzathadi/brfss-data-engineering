# src/visualization/charts.py

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import gaussian_kde
from .utils import calculate_bmi_statistics, format_age_labels, format_correlation_values, calculate_data_statistics
from .config import BINARY_FEATURES
import os

def create_diabetes_trend_chart(df):
    """
    Create diabetes trend chart showing cases per year with line chart.
    """
    # Group by year and calculate diabetes cases
    diabetes_trend = df.groupby("Year")["Diabetes_01"].sum().reset_index()
    
    # Only show years that have data
    diabetes_trend = diabetes_trend[diabetes_trend["Diabetes_01"] > 0]
    
    fig = px.line(
        diabetes_trend, 
        x="Year", 
        y="Diabetes_01",
        title="Tren Kasus Diabetes per Tahun",
        labels={"Diabetes_01": "Jumlah Kasus Diabetes"},
        markers=True,  # Add markers to the line
        text="Diabetes_01"  # Show values on markers
    )
    
    # Customize the chart
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        texttemplate='%{text}',
        textposition='top center'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
        title_font_size=20,
        xaxis=dict(
            tickmode='array',
            tickvals=diabetes_trend["Year"].tolist(),
            gridcolor='rgba(128,128,128,0.3)'
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.3)',
            rangemode='tozero'  # Start y-axis from 0
        ),
        height=500
    )
    
    return fig

def create_data_statistics_table(df, year):
    """
    Create comprehensive data statistics for the selected year.
    """
    dff = df[df["Year"] == year]
    parquet_path = os.path.join(
        "data", "processed", f"diabetes_01_health_indicators_BRFSS{year}.parquet"
    )
    stats = calculate_data_statistics(dff, parquet_path=parquet_path)
    return stats

def create_diabetes_comparison_chart(df, year):
    """
    Create bar chart comparing diabetes vs non-diabetes cases for selected year.
    """
    dff = df[df["Year"] == year]
    
    # Count diabetes cases
    diabetes_counts = dff["Diabetes_01"].value_counts().sort_index()
    labels = ["Tidak Diabetes", "Diabetes"]
    values = [diabetes_counts.get(0, 0), diabetes_counts.get(1, 0)]
    colors = ['#2E86AB', '#A23B72']  # Blue for non-diabetes, Red for diabetes
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            text=values,
            texttemplate='%{text:,}',
            textposition='outside',
            marker_color=colors,
            name="Jumlah Kasus",
            width=0.4  # Make bars narrower (default is 0.8)
        )
    ])
    
    fig.update_layout(
        title=f"Perbandingan Kasus Diabetes vs Non-Diabetes - {year}",
        xaxis_title="Status Diabetes",
        yaxis_title="Jumlah Kasus",
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
        title_font_size=20,
        height=500,
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.3)',
            rangemode='tozero'
        ),
        xaxis=dict(gridcolor='rgba(128,128,128,0.3)'),
        showlegend=False
    )
    
    # Add percentage annotations with more spacing
    total = sum(values)
    if total > 0:
        percentages = [f"{(val/total)*100:.1f}%" for val in values]
        for i, (label, value, pct) in enumerate(zip(labels, values, percentages)):
            fig.add_annotation(
                x=i,
                y=value + max(values) * 0.15,
                text=pct,
                showarrow=False,
                font=dict(color='black', size=14)
            )
    
    return fig

def create_binary_features_chart(df, year):
    """
    Create binary features distribution chart with multiple rows and larger pie charts.
    """
    dff = df[df["Year"] == year]
    
    # Calculate number of rows and columns for subplot arrangement
    n_features = len(BINARY_FEATURES)
    n_cols = 3  # 3 columns per row
    n_rows = (n_features + n_cols - 1) // n_cols  # Calculate required rows
    
    # Create subplots with minimal spacing for maximum pie chart size
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        specs=[[{"type": "pie"} for _ in range(n_cols)] for _ in range(n_rows)],
        subplot_titles=BINARY_FEATURES,
        vertical_spacing=0.08,  # Minimal vertical spacing
        horizontal_spacing=0.02  # Minimal horizontal spacing
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
                hole=0.2,  # Further reduced hole size for even larger pie
                textinfo='percent+label',
                textposition='inside',
                showlegend=False,
                textfont=dict(size=14)  # Even larger text
            ),
            row=row, col=col_pos
        )
    
    fig.update_layout(
        title=f"Distribusi Proporsi Fitur Biner - {year}",
        height=350 * n_rows + 100,  # Increased height even more
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
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
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
        title_font_size=20,
        height=600  # Increased height to match age chart
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
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
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
        title=f"Distribusi Kurva KDE BMI (Standarized) - {year}",
        xaxis_title="BMI",
        yaxis_title="Kepadatan",
        showlegend=False,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='black'),
        title_font_size=20,
        height=500,
        xaxis=dict(gridcolor='rgba(128,128,128,0.3)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.3)')
    )
    
    # Calculate statistics
    stats = calculate_bmi_statistics(bmi_data)
    
    return fig, stats

def create_correlation_heatmap(df, year):
    """
    Create correlation heatmap with appropriate correlation method for mixed data types.
    Uses Spearman correlation which is suitable for:
    - Numeric data (BMI)
    - Ordinal categorical data (Age: 1-13)
    - Binary categorical data (HighBP, HighChol, etc.: 0,1)
    """
    dff = df[df["Year"] == year]
    
    # Define the 11 features explicitly
    feature_columns = [
        'Diabetes_01', 'HighBP', 'HighChol', 'BMI', 'Smoker', 
        'PhysActivity', 'Fruits', 'Veggies', 'DiffWalk', 'Sex', 'Age'
    ]
    
    # Filter to only include available columns
    available_cols = [col for col in feature_columns if col in dff.columns]
    
    if len(available_cols) < 2:
        # Return empty figure if insufficient data
        fig = go.Figure()
        fig.update_layout(
            title=f"Insufficient data for correlation analysis - {year}",
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black'),
            height=500
        )
        return fig
    
    # Select data for correlation analysis
    corr_data = dff[available_cols].copy()
    
    # Remove rows with any missing values for correlation calculation
    corr_data = corr_data.dropna()
    
    if len(corr_data) == 0:
        # Return empty figure if no complete cases
        fig = go.Figure()
        fig.update_layout(
            title=f"No complete cases for correlation analysis - {year}",
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black'),
            height=500
        )
        return fig
    
    # Calculate Spearman correlation (appropriate for mixed ordinal/binary/continuous data)
    try:
        corr = corr_data.corr(method='spearman')
        corr_formatted = format_correlation_values(corr)
        
        # Create better feature labels for display
        feature_labels = {
            'Diabetes_01': 'Diabetes',
            'HighBP': 'Tekanan Darah Tinggi',
            'HighChol': 'Kolesterol Tinggi', 
            'BMI': 'BMI',
            'Smoker': 'Merokok',
            'PhysActivity': 'Aktivitas Fisik',
            'Fruits': 'Konsumsi Buah',
            'Veggies': 'Konsumsi Sayuran',
            'DiffWalk': 'Kesulitan Berjalan',
            'Sex': 'Jenis Kelamin',
            'Age': 'Kategori Umur'
        }
        
        # Rename columns and index for better display
        display_labels = [feature_labels.get(col, col) for col in corr_formatted.columns]
        corr_display = corr_formatted.copy()
        corr_display.columns = display_labels
        corr_display.index = display_labels
        
        # Create heatmap
        fig = px.imshow(
            corr_display,
            zmin=-1,
            zmax=1,
            color_continuous_scale="RdBu_r",  # Reversed colorscale for better interpretation
            text_auto=True,
            title=f"Matriks Korelasi Antar Fitur - {year}",
            aspect="auto"
        )
        
        # Update layout for better visualization
        fig.update_layout(
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black', size=12),
            title_font_size=20,
            title_x=0.5,  # Center the title
            height=800,  # Increased height for better readability
            width=900,   # Fixed width
            margin=dict(l=150, r=150, t=100, b=100),  # More margin for labels
            xaxis=dict(
                side='bottom',
                tickangle=45,  # Rotate x-axis labels for better readability
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                side='left',
                tickfont=dict(size=10)
            )
        )
        
        # Update text format and appearance
        fig.update_traces(
            texttemplate='%{z:.3f}',  # Show 3 decimal places for better readability
            textfont=dict(size=10),
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Korelasi: %{z:.6f}<extra></extra>'
        )
        
        # Add colorbar title
        fig.update_coloraxes(
            colorbar_title="Koefisien Korelasi<br>Spearman",
            colorbar_title_font_size=12
        )
        
    except Exception as e:
        # Fallback figure in case of error
        fig = go.Figure()
        fig.update_layout(
            title=f"Error calculating correlation: {str(e)}",
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            font=dict(color='black'),
            height=500
        )
    
    return fig