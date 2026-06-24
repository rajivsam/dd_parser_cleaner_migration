# Olist Migration with KMDS - A Step-by-Step Guide

This guide shows the main KMDS workflow for the Olist migration project, from repository setup through featurization, modeling, and KMDS knowledge graph generation.

## 1. Repository Setup

- Work from the repository root: `/home/rajiv/programming/kmds_migration/olist_migration`
- The workspace contains:
  - `config.yaml` and `customer_config.yaml` for KMDS parser/cleaner config
  - `featurizer_config.yaml` for the SP 2017 feature pipeline
  - `modeling_config.yaml` for clustering model runtime settings
  - `data/` raw CSVs and prepared artifacts
  - `documents/` project documentation
  - `agent_documents/` KMDS-guided modeling and clustering instructions
  - `models/` spectral clustering implementation and outputs

## 2. Project Initialization

- Use `copilot_init.md` as the session initialization reference.
- Ensure the virtual environment is activated from the repository root:

```bash
source .venv/bin/activate
```

- If dependencies are missing, install them in the environment:

```bash
pip install -r requirements.txt
pip install pyarrow
pip install kmds-modeling
```

## 3. Install KMDS & Dependencies

- Confirm `kmds-ui`, `kmds-modeling`, and `kmds-data-helper` are available in `.venv`.
- The core pipeline depends on:
  - `dd-parser-cleaner` / `classify-entities`
  - `clean-dataset`
  - `kmds-kb`
  - `kmds-workbench`

## 4. Workspace Initialization

- Validate that `config.yaml` exists in the root and is the active KMDS workspace config.
- `customer_config.yaml` is used for the customer-specific cleaner workflow.
- The main repository workflow uses the raw Olist CSV files in `data/`.

## 5. File Location and Artifact Placement

- The key outputs are placed under `data/`, `models/`, and `output/`.
- Important files and artifacts:
  - `data/SP_2017_freq_prod_weekly_sales_prepared.csv`
  - `data/SP_2017_weekly_revenue_prepared.csv`
  - `data/olist_daily_orders_prepared.csv`
  - `data/dd_cleaner/olist_customers_dataset_clean.csv`
  - `models/week_clusters.csv`
  - `models/product_clusters.csv`
  - `models/spectral_gap.csv`
  - `models/spectral_clustering_summary.md`
  - `output/full_service_report.json`
  - `data/kmds/project_knowledge_graph.xml`

## 6. Provisional Configuration Bootstrap

- `featurizer_config.yaml` defines the SP 2017 feature pipeline stages.
- `modeling_config.yaml` defines the clustering input artifacts, algorithm settings, and output targets.
- `customer_config.yaml` isolates the customer metadata cleaner workstream.
- Use `config.yaml` for the main orders + modeling workflow.

## 7. Parser Handshake Filters

- Run `classify-entities` with the appropriate config to generate parser handshake metadata.
- Customer workflow command:

```bash
.venv/bin/classify-entities --config customer_config.yaml
```

- Orders workflow command:

```bash
.venv/bin/classify-entities --config config.yaml
```

- The handshake phase produces entity assignments and field metadata needed to drive cleaner decisions.

## 8. Clean Dataset

- Execute the cleaner to generate validated, prepared datasets.
- Customer cleaner command:

```bash
.venv/bin/clean-dataset --config customer_config.yaml --action full
```

- Orders cleaner command:

```bash
.venv/bin/clean-dataset --config config.yaml --action full
```

- Verify the results and artifacts in `data/dd_cleaner/` and `documents/dd_cleaner/`.

## 9. Notebook Analysis

- Use the notebooks to inspect pipeline outputs and modeling decisions.
- Relevant notebooks:
  - `notebooks/modeling_spectral_clustering.ipynb`
  - `notebooks/modeling_clustering_advisor.ipynb`

- These notebooks expose the modeling workflow, data preparation, and cluster result visualizations.

## 10. Metadata Review

- Review the metadata that feeds the feature advisor and model advisor.
- Use the customer and orders parser/cleaner outputs to confirm data quality and entity assignments.
- Ensure the featurization plan matches the intended unsupervised, graph-oriented analysis.

## 11. Modeling Guidance

### 11.1 Olist Methodology

Use the documents in `documents/` and `agent_documents/` to frame the analysis:

- `documents/olist_featurization_pipeline.md` defines the feature-building pipeline.
- `documents/olist_temporal_affinity_analytics_for_SP.md` describes the business rationale and KMDS methodology.
- `documents/rationale_for_spectral_clustering.md` explains the spectral co-clustering decision.
- `documents/modeling_results_observations.md` summarizes the cluster outcomes and business impact.

### 11.2 Model selection rationale

- The pipeline builds a week-product affinity matrix for São Paulo, 2017.
- The raw frequency matrix is normalized with TF-IDF-style scaling to reduce dominance from evergreen products.
- A bipartite spectral embedding is computed from the normalized week-product affinity graph.
- KMeans is applied to the joint week/product spectral embedding to generate co-clusters.

### 11.3 Advisor integration

- The model advisor confirms the unsupervised clustering intent and supports spectral co-clustering.
- Use the advisor output as a design guardrail rather than a rigid rule.

## 12. Feature Pipeline Execution

- Run the featurization script:

```bash
python featurization_scripts/featurization.py
```

- Confirm key prepared artifacts exist:
  - `data/olist_daily_orders_prepared.csv`
  - `data/SP_2017_orders_filtered_prepared.csv`
  - `data/SP_2017_weekly_revenue_prepared.csv`
  - `data/SP_2017_freq_prod_weekly_sales_prepared.csv`

- The goal is to produce the exact SP 2017 weekly product affinity matrix used by the clustering workflow.

## 13. Modeling Execution

- Execute the spectral clustering workflow from the repository:

```bash
.venv/bin/python -c "from models.spectral_clustering import run_spectral_clustering; print(run_spectral_clustering('modeling_config.yaml', output_dir='models'))"
```

- Inspect model outputs:
  - `models/week_clusters.csv`
  - `models/product_clusters.csv`
  - `models/spectral_gap.csv`
  - `models/cluster_counts.csv`
  - `models/week_embeddings.csv`
  - `models/product_embeddings.csv`

- Review `models/spectral_clustering_summary.md` for analysis notes.

## 14. KMDS Helper Output

- Build the helper artifact required for KMDS ingestion:

```bash
python - <<'PY'
from pathlib import Path, json
workspace = Path('.')
helper = {
    'project_summary': 'Generated by KMDS helper integration script.',
    'metadata': {'generated_by': 'kmds-data-helper', 'source': 'repo artifacts'}
}
(workspace / 'output' / 'full_service_report.json').write_text(json.dumps(helper, indent=2), encoding='utf-8')
PY
```

- The helper output is the summary input for `kmds-data-helper` ingestion.

## 15. Knowledge Graph Generation

- Generate the KMDS RDF knowledge graph:

```bash
.venv/bin/kmds-kb --workspace . \
  --project-file data/kmds/project_knowledge_graph.xml \
  --workflow-name olist_migration_kmds \
  --mode auto \
  --workflow-type application
```

- Confirm the output file exists at `data/kmds/project_knowledge_graph.xml`.

## 16. KMDS Visualization

- Start the KMDS UI if needed:

```bash
.venv/bin/kmds-workbench
```

- Open `http://127.0.0.1:8050` to inspect the project knowledge graph and workflow artifacts.

## 17. Practical Next Steps

- Validate the cluster structure against calendar events and São Paulo seasonality.
- Link product clusters to merchandising and inventory strategies.
- Expand the workflow to additional regions beyond SP 2017.
- Improve the helper artifact with richer document summaries and notebook observations.

## 18. Artifact Inventory

- `config.yaml`
- `customer_config.yaml`
- `featurizer_config.yaml`
- `modeling_config.yaml`
- `documents/olist_featurization_pipeline.md`
- `documents/olist_temporal_affinity_analytics_for_SP.md`
- `documents/rationale_for_spectral_clustering.md`
- `documents/modeling_results_observations.md`
- `data/SP_2017_freq_prod_weekly_sales_prepared.csv`
- `models/week_clusters.csv`
- `models/product_clusters.csv`
- `data/kmds/project_knowledge_graph.xml`
- `output/full_service_report.json`
