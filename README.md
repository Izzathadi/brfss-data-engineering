# BRFSS Data Engineering Pipeline

BRFSS Data Engineering is an end-to-end ELT and analytics pipeline for the Behavioral Risk Factor Surveillance System (BRFSS) dataset, focusing on diabetes classification detection. This project automates data extraction, transformation, validation, and visualization, providing interactive dashboards for data analysis.

---

## 📊 Dashboard Preview

<p align="center">
  <img src="images/dashboard.png" alt="Dashboard Preview" width="500"/>
</p>

---

## Features

- **Automated ELT Pipeline**: Download, extract, store, and process BRFSS data for multiple years using [Prefect](https://www.prefect.io/) with scheduling.
- **Data Validation**: Schema validation using [Pandera](https://pandera.readthedocs.io/).
- **Interactive Dashboard**: Explore trends, distributions, and correlations with [Dash](https://dash.plotly.com/).
- **Configurable**: Easily adjust years, features, and data sources via `config.yaml`.

---

## Project Structure

```
brfss-data-engineering/
│
├── README.md                   # Project documentation
├── config.yaml                 # Main pipeline configuration (years, dirs, URLs)
├── prefect.yaml                # Prefect deployment and scheduling config
├── requirements.txt            # Python dependencies
│
├── data/
│   ├── raw/                    # Downloaded raw BRFSS .XPT files
│   └── processed/              # Processed .parquet files
│
├── images/
│   └── dashboard.png           # Dashboard preview image
│
├── logs/
│   ├── missing_features.log    # Log of missing features during transform
│   └── validation_summary.log  # Data validation summary log
│
└── src/
    ├── __init__.py             # Marks src as a Python package
    ├── extract/
    │   └── extract.py          # Download, extract, and config loading functions
    ├── flow/
    │   └── pipeline.py         # Main Prefect ELT pipeline and dashboard runner
    ├── transform/
    │   ├── transform.py        # Data cleaning, feature engineering, validation
    │   ├── schema.py           # Pandera schema for data validation
    │   └── feature_map.yaml    # Feature mapping for column selection/renaming
    └── visualization/
        ├── app.py              # Dash app entrypoint
        ├── charts.py           # Chart/figure generation functions
        ├── config.py           # Dashboard config (title, port, features)
        ├── data_loader.py      # Load processed data for dashboard
        ├── layout.py           # Dashboard layout and UI components
        └── utils.py            # Functions for statistics, formatting, and dashboard utilities

```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Izzathadi/brfss-data-engineering.git
cd brfss-data-engineering
```

### 2. Install Dependencies

It is recommended to use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure the Pipeline

Edit `config.yaml` to set the desired years and data directories:

```yaml
dataset:
  start_year: 2015
  url_template: "https://www.cdc.gov/brfss/annual_data/{year}/files/LLCP{year}XPT.zip"
  raw_dir: "data/raw/"
  processed_dir: "data/processed/"
```

### 4. Start Prefect Server

Start the Prefect server locally:

```bash
prefect server start
```

In a new terminal, set the Prefect API URL:

```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

Monitoring the Prefect dashboard at [http://127.0.0.1:4200/dashboard](http://127.0.0.1:4200/dashboard):

### 5. Create a Prefect Worker

Create a Prefect worker (if not already created):

```bash
prefect work-pool create --type process "my-work-pool"
```

### 6. Deploy and Run the ELT Pipeline

Deploy the pipeline:

```bash
prefect deploy
```

Start the work-pool:

```bash
prefect worker start --pool "my-work-pool"
```

Then run the deployment:

```bash
prefect deployment run 'elt-pipeline/brfss-yearly'
```

- Processed data will be saved in `data/processed/`.
- Logs are written to `logs/`.

### 7. Launch the Dashboard

After the ELT process is complete, the dashboard will be available at [http://localhost:8050](http://localhost:8050):

---

## References

- [CDC BRFSS Data](https://www.cdc.gov/brfss/annual_data/annual_data.htm)
- [Prefect Documentation](https://docs.prefect.io/)
- [Dash by Plotly](https://dash.plotly.com/)
- [Pandera](https://pandera.readthedocs.io/)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

