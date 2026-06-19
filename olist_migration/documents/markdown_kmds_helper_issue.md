# KMDS Helper Markdown Ingestion Issue

## Summary

The current KMDS knowledge graph generation is not ingesting the workspace markdown documents directly. The installed `kmds-data-helper` package in this environment only supports helper-output ingestion (`output/full_service_report.json`) and does not include the upstream repository's server-based analysis path.

## What I observed

- The graph was generated from `output/full_service_report.json` using `kmds-kb`.
- The helper artifact was manually created or replaced with a concise summary.
- The generated KMDS graph contains only the summary text from that helper artifact, not the full markdown content from `documents/`, `agent_documents/`, or notebooks.
- There is no local `kmds_config.yaml` in the workspace, so the upstream server workflow cannot be invoked as-is.

## Why this is a problem

The workspace contains multiple markdown documents and notebooks that should drive the KMDS workflow analysis. Under the current packaged helper workflow, those files are not ingested directly:

- `kmds-kb` only reads `output/full_service_report.json` or other helper artifacts.
- The upstream server-based workflow in the original repo uses a service and FastAPI API to analyze the workspace.
- The installed package does not expose the upstream repo’s `main.py`, `api.py`, or `kmds_config.yaml` server entrypoint.

As a result, the knowledge graph is incomplete and lacks the rich modeling observations from the workspace docs.

## Root cause

1. The installed version is `kmds-data-helper 0.4.0` from the package distribution.
2. That package supports summary ingestion and direct helper file ingestion only.
3. It does not include the server-oriented workflow that can analyze notebooks and docs with `KMDSReportService`.
4. The workspace does not contain the required `kmds_config.yaml` or server launch files.

## Evidence

- The installed package exposes only these entrypoints:
  - `kmds-analyze`
  - `kmds-check`
  - `kmds-init-workspace`
  - `kmds-kb`
- The server-based upstream repo docs mention:
  - `uv run uvicorn api:app --reload`
  - `main.py`
  - `api.py`
  - `kmds_config.yaml`
- These files are not present in the local workspace or in the installed package.

## What was expected

I expected the KMDS helper to:

- ingest markdown files from `documents/`, `agent_documents/`, and notebook text
- generate observations for modeling, featurization, and tooling decisions
- include the actual workspace documentation rather than just a short summary blob

## What actually happened

- The helper only ingested `output/full_service_report.json`.
- That artifact was synthesized manually and did not contain all markdown content.
- The resulting graph shows only 12 observations and misses many modeling docs.

## Recommended next steps

1. Confirm whether you want to use the upstream server workflow from the `kmds-data-helper` repo.
2. If so, install/run the repo version with `main.py`/`api.py` and add `kmds_config.yaml`.
3. If not, patch the current packaged helper to:
   - read markdown docs from `documents/` and `agent_documents/`
   - sanitize markdown and notebook content before ingestion
   - produce a richer helper output JSON that includes the key document sections
4. Prefer `--mode observations` only after the helper can safely normalize document blocks.

## Suggested patch direction

- Add a direct workspace ingestion module to `kmds-data-helper` that scans:
  - `documents/*.md`
  - `agent_documents/*.md`
  - `notebooks/*.ipynb`
- Add sanitization for markdown:
  - remove code fences
  - strip headings and lists
  - collapse repeated whitespace
- Keep the helper output focused on narrative findings, not raw document dumps.

## Immediate action for this repository

For now, the safest path is:

- continue using `output/full_service_report.json` with a curated project summary
- do not rely on raw markdown ingestion until the helper is patched
- add the upstream server workflow only if you want the full repo analysis path
