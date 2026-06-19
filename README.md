# KMDS Real Dataset Illustrations

This repository is set up to illustrate the KMDS toolkit applied to real datasets with the range of issues normally encountered in practical deployments.

## Purpose

- Show how KMDS tools support real-world data ingestion, cleaning, and structuring
- Demonstrate end-to-end handling of dataset issues such as missing values, quarantine output, and evolving schema semantics
- Provide a second instantiation of a real dataset workflow using the Olist retail dataset and KMDS modeling artifacts

## Contents

- `olist_migration/` — the main dataset project for Olist SP 2017
- `data/` — raw data extracts and prepared artifacts
- `models/` — clustering and profiling implementation plus generated outputs
- `notebooks/` — analysis and modeling notebooks for execution and inspection
- `agent_documents/` — agent-facing instructions and task setup for KMDS workflows
- `documents/` — supporting reports, summaries, and domain analysis notes

## How to use

1. Open `olist_migration/` as the primary workspace.
2. Activate the Python environment in `olist_migration/.venv`.
3. Follow the KMDS project workflow in `olist_migration/copilot_init.md` for cleaning, featurization, modeling, and artifact generation.

## Why this repository exists

This repo is intended as a practical example of KMDS applied to a complex, noisy real dataset. It is not a polished product release; it is a working illustration of KMDS data workflows, from raw data issues to longitudinal modeling and cluster analysis.
