"""Task initialization template for an Olist clustering model."""

from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def load_modeling_config(config_path: str) -> Dict:
    """Load the modeling config for the clustering task."""
    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_feature_matrix(model_ready_path: str) -> pd.DataFrame:
    """Load the preprocessed week-product matrix from the featurization outputs."""
    path = Path(model_ready_path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def run_clustering_task(config_path: str, output_dir: Optional[str] = None):
    """Entry point for the clustering task in the Olist workspace."""
    config = load_modeling_config(config_path)
    working_dir = config["data"]["working_dir"]
    model_ready_path = Path(working_dir) / "data" / config["data"]["model_ready_data_file"]
    df = load_feature_matrix(str(model_ready_path))

    # 1. Ensure the dataset uses a week index and product columns.
    if "woy" not in df.columns:
        raise ValueError("The dataset must contain a 'woy' column for weekly clustering.")

    feature_df = df.drop(columns=["woy"])

    # 2. Apply the spectral co-clustering pipeline.
    from models.spectral_clustering import run_spectral_clustering

    results = run_spectral_clustering(
        config_path=config_path,
        output_dir=output_dir,
    )

    return results


if __name__ == "__main__":
    import sys

    config_path = sys.argv[1] if len(sys.argv) > 1 else "modeling_config.yaml"
    print(run_clustering_task(config_path))
