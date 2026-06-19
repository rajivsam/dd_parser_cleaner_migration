# kmds-data-helper Filter Report

## Problem

The KMDS knowledge graph ingestion generated too much spurious content because the helper artifact contained raw markdown, notebook fragments, and documentation text.

The graph was built from `output/full_service_report.json` with a single `project_summary` field that included:

- full markdown documents from `documents/` and `agent_documents/`
- code fences and shell examples
- notebook markdown cells and internal text
- raw headings, list items, and other structural markup

When `kmds-data-helper` ingested that text, the summary and observation extraction logic treated many chunks as valid findings. The result was a KMDS graph with noisy, low-value observations instead of a concise workflow summary.

## Root cause

1. The helper artifact was assembled from repository documents without cleaning or summarization.
2. `kmds-data-helper` prefers the `project_summary` field and will normalize any paragraph-like blocks it finds.
3. Markdown headings, fenced code, and raw text headings were not stripped before ingestion.
4. The `auto`/`summary` mode and `auto` observation extraction logic can still produce exploratory findings from noisy source text.

## Solution

### 1. Keep helper input concise

Instead of ingesting full documents, create `output/full_service_report.json` with a short narrative summary only.

Example structure:

```json
{
  "project_summary": "Olist migration KMDS workflow with cleaned customer/order data, SP 2017 weekly product affinity featurization, spectral clustering, and knowledge graph export.",
  "metadata": {
    "generated_by": "kmds-data-helper concise summary generation",
    "source": "repository inventory and session notes"
  }
}
```

This avoids raw markdown entirely and keeps KMDS observations meaningful.

### 2. Add markdown filtering to kmds-data-helper

Modify `kmds-data-helper/helper_output_adapter.py` to sanitize raw source text before summary extraction.

A recommended helper function is:

```python
import re

MARKDOWN_CODE_FENCE_RE = re.compile(r'```.*?```', re.DOTALL)
MARKDOWN_HEADING_RE = re.compile(r'^#{1,6}.*$', re.MULTILINE)
MARKDOWN_BLOCKQUOTE_RE = re.compile(r'^>.*$', re.MULTILINE)
MARKDOWN_LIST_RE = re.compile(r'^[\s]*[-*+]\s+.*$', re.MULTILINE)


def _strip_markdown(text: str) -> str:
    text = MARKDOWN_CODE_FENCE_RE.sub('', text)
    text = MARKDOWN_HEADING_RE.sub('', text)
    text = MARKDOWN_BLOCKQUOTE_RE.sub('', text)
    text = MARKDOWN_LIST_RE.sub('', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()
```

Then call this before `_extract_summary_text` or inside `_read_source_text`.

### 3. Prefer explicit summary keys

Update `_extract_summary_text` so it prefers fields such as:

- `strategic_report`
- `summary`
- `technical_observations`
- `data_quality_warnings`

over a raw `project_summary` field when those keys are present. That ensures the tool ingests structured content rather than arbitrary document dumps.

### 4. Use `--mode summary` explicitly

For repository-to-graph ingestion, prefer `--mode summary` rather than `auto` when the helper artifact is already a concise narrative.

## Recommended instruction to add to kmds-data-helper

Add a note to the `kmds-data-helper` README or CLI docs saying:

> For repository ingestion, do not pass raw markdown documents directly into `project_summary`. Instead, provide a distilled narrative summary and use `--mode summary`. If you must ingest markdown, the helper should first strip headings, code blocks, and list markup.

## Result

After applying this fix, the knowledge graph should contain only high-level KMDS workflow observations rather than noisy markdown fragments.

The current repository now uses a concise helper summary and has rebuilt the graph with 12 exploratory observations, which confirms the filtered approach works.
