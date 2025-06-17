import os
import re
import subprocess
import sys
from pathlib import Path

from prefect import flow, get_run_logger, task

from src.extract.extract import load_config, extract_dataset
from src.transform.transform import transform_dataset
from src.visualization.static_charts import save_static_charts

def get_latest_year(raw_dir):
    files = os.listdir(raw_dir)
    years = []
    for f in files:
        match = re.search(r"LLCP(\d{4})\.XPT", f, re.IGNORECASE)
        if match:
            years.append(int(match.group(1)))
    return max(years) if years else None

@task
def run_dash_server():
    """
    Menjalankan server Dash dashboard dengan penanganan kesalahan dan logging yang tepat.
    Fungsi ini dirancang untuk portabilitas, memungkinkan project dijalankan dari direktori manapun.
    """
    try:
        # 1. Menentukan root proyek secara dinamis untuk portabilitas
        # Path(__file__) -> /home/izzat/projects/capstone-data-engineering/src/flow/pipeline.py
        # .parent.parent.parent -> /home/izzat/projects/capstone-data-engineering/
        project_root = Path(__file__).parent.parent.parent 
        
        # 2. Menentukan jalur absolut ke direktori visualisasi
        # Dari project_root, masuk ke src/visualization
        viz_dir = project_root / "src" / "visualization"
        app_path = viz_dir / "app.py"
        
        # 3. Memeriksa apakah file app.py ada
        if not app_path.exists():
            raise FileNotFoundError(f"Dashboard app not found at: {app_path}")
        
        print("Starting BRFSS Diabetes Dashboard...")
        print(f"Dashboard will be available at: http://localhost:8050")
        print("Press Ctrl+C to stop the dashboard")
        
        # 4. Menjalankan dashboard sebagai modul Python
        # Menggunakan `-m` memungkinkan Python untuk menemukan modul di dalam struktur paket
        # `src.visualization.app` adalah jalur modul relatif terhadap project_root
        # `cwd=project_root` mengatur direktori kerja untuk subprocess ke root proyek,
        # sehingga `src` dapat ditemukan sebagai paket level atas.
        process = subprocess.Popen([
            sys.executable, "-m", "src.visualization.app" 
        ], cwd=project_root) # Penting: Atur CWD ke root proyek
        
        # 5. Menunggu proses selesai atau diinterupsi
        try:
            process.wait() # Menunggu subprocess selesai
        except KeyboardInterrupt:
            # Menangani interupsi keyboard (Ctrl+C) untuk mematikan dashboard
            print("\nShutting down dashboard...")
            process.terminate() # Mengirim sinyal TERM ke subprocess
            process.wait()      # Menunggu subprocess benar-benar berhenti
        finally:
            # Tidak perlu lagi mengubah kembali CWD, karena CWD aplikasi utama tidak diubah.
            # Subprocess memiliki CWD-nya sendiri.
            pass
            
    except FileNotFoundError as fnfe:
        # Penanganan khusus untuk FileNotFoundError
        print(f"ERROR: {fnfe}")
        raise # Meneruskan exception agar Prefect atau sistem lain dapat menanganinya
    except Exception as e:
        # Penanganan umum untuk error lainnya selama menjalankan dashboard
        print(f"ERROR running dashboard: {e}")
        raise # Meneruskan exception

@task
def setup_dashboard_environment():
    """
    Setup the dashboard environment and check dependencies.
    """
    try:
        import dash
        import plotly
        import pandas as pd
        import numpy as np
        from scipy.stats import gaussian_kde
        print("✓ All dashboard dependencies are available")
        
        # Check if processed data directory exists
        processed_dir = Path("data/processed")
        if not processed_dir.exists():
            print(f"⚠️  Warning: Processed data directory not found: {processed_dir}")
            print("   Make sure to run data processing tasks before starting the dashboard")
        else:
            parquet_files = list(processed_dir.glob("*.parquet"))
            if parquet_files:
                print(f"✓ Found {len(parquet_files)} processed data files")
            else:
                print("⚠️  Warning: No parquet files found in processed data directory")
                
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("Please install required packages: pip install dash plotly pandas numpy scipy")
        raise

@task
def generate_static_visualizations(processed_dir: str):
    save_static_charts(processed_dir)

@flow
def etl_pipeline(config_path: str = "config.yaml"):
    logger = get_run_logger()

    # 1. Load Config
    config = load_config(config_path)
    start_year = config["dataset"]["start_year"]
    url_template = config["dataset"]["url_template"]
    raw_dir = config["dataset"]["raw_dir"]
    processed_dir = config["dataset"]["processed_dir"]
    feature_map_path = "src/transform/feature_map.yaml"
    log_file_path = "logs/missing_features.log"

    os.makedirs("logs", exist_ok=True)
    open(log_file_path, 'w').close()
    os.makedirs(processed_dir, exist_ok=True)

    # Deteksi tahun terakhir yang sudah ada
    latest = get_latest_year(raw_dir)
    start_year = (latest + 1) if latest else config["dataset"]["start_year"]
    year = start_year

    logger.info(f"🚀 Memulai ETL dari tahun: {year}")

    # 2. Extract & Transform Loop
    while True:
        url = url_template.format(year=year)
        logger.info(f"🔍 Mengecek tahun: {year}")
        path = extract_dataset(url=url, output_dir=raw_dir)

        if path is None:
            logger.warning(f"❌ Tidak ada data untuk tahun {year}, berhenti.")
            break

        match = re.search(r"LLCP(\d{4})", os.path.basename(path), re.IGNORECASE)
        if not match:
            logger.warning(f"⚠️ File tidak cocok pola: {path}")
            year += 1
            continue

        year_str = match.group(1)
        output_file = os.path.join(processed_dir, f"diabetes_01_health_indicators_BRFSS{year_str}.parquet")

        try:
            transform_dataset(
                input_path=path,
                feature_map_path=feature_map_path,
                output_path=output_file,
                year=year_str,
                log_file_path=log_file_path
            )
        except KeyError as e:
            logger.error(str(e))
            with open(log_file_path, "a") as f:
                f.write(f"[{year_str}] Transform Error: {e}\n")

        year += 1

    # Visualization tasks
    setup_dashboard_environment()
    run_dash_server()

if __name__ == "__main__":
    etl_pipeline()
