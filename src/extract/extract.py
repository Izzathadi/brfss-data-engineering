
# src/extract/extract.py

import os
import yaml
import requests
from tqdm import tqdm
from zipfile import ZipFile
from prefect import task, get_run_logger

@task
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 404:
        return False
    
    total = int(response.headers.get('content-length', 0))
    with open(save_path, 'wb') as file, tqdm(
        desc=f"Downloading {os.path.basename(save_path)}",
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    return True

def extract_zip(zip_path, extract_to):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

@task
def extract_dataset(url: str, output_dir: str) -> str:
    """
    Mengunduh dan mengekstrak satu file ZIP dari URL.
    Return: path ke file .XPT hasil ekstraksi.
    """
    logger = get_run_logger()

    os.makedirs(output_dir, exist_ok=True)
    year_match = os.path.basename(url)
    year = ''.join(filter(str.isdigit, year_match))

    zip_filename = f"LLCP{year}XPT.zip"
    zip_path = os.path.join(output_dir, zip_filename)

    logger.info(f"⬇️  Downloading: {url}")
    success = download_file(url, zip_path)

    if not success:
        logger.warning(f"❌ File tidak ditemukan: {url}")
        return None

    try:
        logger.info(f"📦 Extracting: {zip_filename}")
        extract_zip(zip_path, output_dir)

        for filename in os.listdir(output_dir):
            new_name = filename.strip()
            if filename != new_name:
                os.rename(os.path.join(output_dir, filename), os.path.join(output_dir, new_name))
                logger.info(f"✏️ Rename: '{filename}' -> '{new_name}'")

        if os.path.exists(zip_path):
            os.remove(zip_path)
            logger.info(f"🧹 Deleted ZIP: {zip_filename}")

        # Return XPT path
        xpt_files = [f for f in os.listdir(output_dir) if f.lower().endswith(".xpt") and year in f]
        if xpt_files:
            return os.path.join(output_dir, xpt_files[0])
        else:
            logger.warning(f"⚠️ Tidak ada file .xpt ditemukan untuk {year}")
            return None

    except Exception as e:
        logger.error(f"⚠️ Gagal mengekstrak {zip_filename}: {e}")
        return None
