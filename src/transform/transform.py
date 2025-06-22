import os
import yaml
import pandas as pd
import numpy as np
import re
import pandera.pandas as pa
from pathlib import Path
from glob import glob
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer
from src.transform.schema import diabetes_schema
from prefect import task, get_run_logger
from scipy.stats import skew

def load_feature_mapping(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config['standard_features']

def select_and_rename_columns(df, feature_map):
    rename_dict, selected_cols = {}, []
    for std_col, possible_names in feature_map.items():
        for name in possible_names:
            if name in df.columns:
                rename_dict[name] = std_col
                selected_cols.append(name)
                break
    missing = set(feature_map.keys()) - set(rename_dict.values())
    df_selected = df[selected_cols].rename(columns=rename_dict)
    return df_selected, missing

def encode(df):
    df = df.drop_duplicates().dropna()
    df = df[df['Diabetes_01'].isin([1, 2, 3, 4])]
    df['Diabetes_01'] = df['Diabetes_01'].replace({1: 1, 2: 0, 3: 0, 4: 0})

    replacements = {
        'HighBP': ({9}, {1: 0, 2: 1}),
        'HighChol': ({7,9}, {2: 0}),
        'Smoker': ({7,9}, {2: 0}),
        'PhysActivity': ({9}, {2: 0}),
        'Fruits': ({9}, {2: 0}),
        'Veggies': ({9}, {2: 0}),
        'DiffWalk': ({7,9}, {2: 0}),
        'Sex': ({7,9}, {2: 0}),
    }

    for col, (drop_vals, rep_map) in replacements.items():
        if drop_vals:
            df = df[~df[col].isin(drop_vals)]
        df[col] = df[col].replace(rep_map)

    df['BMI'] = df['BMI'] / 100
    df = df[df['Age'] != 14]

    int_cols = ['Diabetes_01', 'HighBP', 'HighChol', 'Smoker', 'PhysActivity',
                'Fruits', 'Veggies', 'DiffWalk', 'Sex', 'Age']
    df[int_cols] = df[int_cols].astype(int)
    return df.reset_index(drop=True)

def undersampling(df, target_counts, label='Diabetes_01', random_state=42):
    sampled = [g.sample(n=target_counts.get(v, len(g)), random_state=random_state)
               for v, g in df.groupby(label)]
    return pd.concat(sampled, ignore_index=True)

def compute_iqr_bounds(df, columns):
    return {
        col: (
            df[col].quantile(0.25) - 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25)),
            df[col].quantile(0.75) + 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))
        ) for col in columns
    }

def apply_iqr_clipping(df, columns, bounds):
    for col, (low, high) in bounds.items():
        df[col] = df[col].clip(low, high)
    return df

def scale_features(df, columns, method='minmax'):
    scaler = MinMaxScaler() if method == 'minmax' else StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def transform_numerical_features(df, columns, method, skew_threshold=0.75):
    # Cek skewness untuk setiap kolom
    for column in columns:
        column_skew = skew(df[column].dropna())
        
        # Jika skewness lebih besar dari threshold, lakukan transformasi
        if abs(column_skew) > skew_threshold:
            print(f"Skewness untuk kolom {column}: {column_skew}. Melakukan transformasi...")

            if method == 'log':
                df[column] = np.log(df[column] + 1)  # Menambahkan 1 untuk menghindari log(0)
            
            elif method in ['box-cox', 'yeo-johnson']:
                transformer = PowerTransformer(method=method)
                df[column] = transformer.fit_transform(df[[column]])
            
            else:
                raise ValueError("Metode tidak dikenali. Pilih antara 'log', 'box-cox', atau 'yeo-johnson'.")
        else:
            print(f"Skewness untuk kolom {column}: {column_skew}. Tidak melakukan transformasi.")
    
    return df

@task
def transform_dataset(input_path, feature_map_path, output_path, year, log_file_path):
    logger = get_run_logger()
    df = pd.read_sas(input_path)
    feature_map = load_feature_mapping(feature_map_path)

    df, missing_features = select_and_rename_columns(df, feature_map)

    if missing_features:
        msg = f"❌ Fitur tidak lengkap untuk {year}: {sorted(list(missing_features))}"
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{msg}\n")
        logger.error(msg)
        return
    else:
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"BRFSS{year}: fitur lengkap\n")

    df = encode(df)

    target_counts = {0.0: 70000, 1.0: df['Diabetes_01'].value_counts().get(1.0, 0)}
    df = undersampling(df, target_counts)

    bounds = compute_iqr_bounds(df, ['BMI'])
    df = apply_iqr_clipping(df, ['BMI'], bounds)

    df = transform_numerical_features(df, ['BMI'], method='box-cox')

    df = scale_features(df, ['BMI'], method='standard')

    df = df.drop_duplicates()

    try:
        diabetes_schema.validate(df, lazy=True)
        logger.info(f"✅ Validasi sukses: BRFSS{year}")
    except pa.errors.SchemaErrors as err:
        validation_log = os.path.join("logs", "validation_summary.log")
        with open(validation_log, "a") as f:
            f.write(f"[GAGAL] BRFSS{year} - {output_path}:\n{err.failure_cases.to_string(index=False)}\n\n")
        logger.error(f"❌ Validasi Pandera gagal untuk {year}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"📁 Disimpan: {output_path}")

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    raw_dir = config["dataset"]["raw_dir"]
    processed_dir = config["dataset"]["processed_dir"]
    feature_map_path = "src/transform/feature_map.yaml"
    log_file_path = "logs/missing_features.log"

    os.makedirs("logs", exist_ok=True)
    open(log_file_path, 'w').close()
    os.makedirs(processed_dir, exist_ok=True)

    for file_path in glob(os.path.join(raw_dir, "*.XPT")):
        match = re.search(r"LLCP(\d{4}).?XPT", os.path.basename(file_path).strip(), re.IGNORECASE)
        if not match:
            print(f"⚠️ File dilewati: {file_path}")
            continue
        year = match.group(1)
        output_file = os.path.join(processed_dir, f"diabetes_01_health_indicators_BRFSS{year}.parquet")
        transform_dataset.fn(file_path, feature_map_path, output_file, year, log_file_path)
