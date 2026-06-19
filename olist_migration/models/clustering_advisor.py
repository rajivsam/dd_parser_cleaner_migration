import json
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from kmds_modeling.core.model_advisor import ModelAdvisor
from kmds_modeling.core.notebook_utils import build_notebook_resolver


def run_clustering_advisor(config_path: str, target_variable: Optional[str] = None) -> Dict[str, object]:
    config_path = Path(config_path).resolve()
    workspace_root = config_path.parent
    resolver = build_notebook_resolver(str(workspace_root), config_name=config_path.name)

    model_ready = Path(resolver.model_ready_dataset_path)
    if not model_ready.exists():
        raise FileNotFoundError(f"Model-ready dataset not found: {model_ready}")

    if model_ready.suffix == ".parquet":
        df = pd.read_parquet(model_ready)
    elif model_ready.suffix == ".csv":
        df = pd.read_csv(model_ready)
    else:
        raise ValueError(f"Unsupported model-ready dataset type: {model_ready.suffix}")

    advisor = ModelAdvisor(str(config_path))
    profile = advisor.profile_data(df, target=target_variable, entities=None)
    recommendation = advisor.get_recommendation(profile, user_intent="CLUSTERING")

    output_dir = Path(resolver.modeling_output_path) / "advisor"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "clustering_advisor_recommendation.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"recommendation": recommendation, "profile": profile}, f, indent=2)

    return {
        "recommendation": recommendation,
        "profile": profile,
        "output_path": str(out_path),
    }
