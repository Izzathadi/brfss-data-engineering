import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data(processed_dir):
    data_frames = []
    for file in os.listdir(processed_dir):
        if file.endswith(".parquet"):
            df = pd.read_parquet(os.path.join(processed_dir, file))
            year = int(file.split("BRFSS")[-1].split(".")[0])
            df["Year"] = year
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

def save_static_charts(processed_dir, output_dir="visualizations"):
    os.makedirs(output_dir, exist_ok=True)
    df = load_data(processed_dir)

    binary_features = ["Diabetes_01", "HighBP", "HighChol", "Fruits", "Veggies"]

    for year in sorted(df["Year"].unique()):
        dff = df[df["Year"] == year]

        # Distribusi
        counts = {col: dff[col].value_counts(normalize=True).get(1, 0) for col in binary_features}
        fig_dist = px.bar(x=list(counts.keys()), y=list(counts.values()),
                          labels={"x": "Fitur", "y": "Proporsi Positif"},
                          title=f"Distribusi Positif Fitur - {year}")
        fig_dist.write_image(os.path.join(output_dir, f"distribution_{year}.png"))

        # Korelasi
        corr = dff[binary_features].corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                             title=f"Korelasi Fitur - {year}")
        fig_corr.write_image(os.path.join(output_dir, f"correlation_{year}.png"))

    # Tren
    grouped = df.groupby("Year")[binary_features].mean().reset_index()
    fig_trend = go.Figure()
    for col in binary_features:
        fig_trend.add_trace(go.Scatter(x=grouped["Year"], y=grouped[col],
                                       mode='lines+markers', name=col))
    fig_trend.update_layout(title="Tren Tahunan Fitur Kesehatan",
                            xaxis_title="Tahun", yaxis_title="Proporsi Positif")
    fig_trend.write_image(os.path.join(output_dir, f"trend_overall.png"))
