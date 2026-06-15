# Repository Guidelines

## Project Structure & Module Organization

This repository maintains Sri Lankan domestic bank and branch data. Root-level `banks.json` is the legacy bank dataset, while `banks.generated.json` is the generated consolidated output. The `data/` directory contains `banks.json` plus branch files named by bank code, such as `data/7010.json`. `scripts/merge-banks.js` reads those files, normalizes names, merges legacy Seylan Bank rows, and writes `banks.generated.json`. Python entry points such as `main.py`, `download.py`, and `lankapay.py` are managed by the Python project configuration in `pyproject.toml`.

## Build, Test, and Development Commands

- `uv sync`: install Python dependencies from `pyproject.toml` and `uv.lock`.
- `uv run python main.py`: run the current Python entry point.
- `uv run python download.py`: run the download/update workflow when refreshing source data.
- `node scripts/merge-banks.js`: regenerate `banks.generated.json` from `data/` and root legacy data.

After changing JSON data, run the merge script and review its summary for missing, empty, invalid, or duplicate branch files.

## Coding Style & Naming Conventions

Use 4-space indentation for Python and JSON output. Keep JavaScript in CommonJS style, matching `scripts/merge-banks.js`, with `const`/`let`, semicolons, and small helper functions. Branch data files must be named `<bankCode>.json` and contain an array of branch records. Preserve field names used by the generated output: `code`, `bankName`, `agentOption`, `bankCountry`, and `countryCode`.

## Testing Guidelines

No formal test suite is currently present. Treat `node scripts/merge-banks.js` as the main validation step for data changes. The command should complete without invalid JSON, unexpected duplicate codes, or missing branch files unless the PR explains why. For Python changes, at minimum run the affected script with `uv run python <script>.py`.

## Commit & Pull Request Guidelines

Recent commits use short, direct messages such as `Update banks.json` or `update with seylan branches`. Keep commit subjects concise and action-oriented. Pull requests should describe the data source or script change, list commands run, and mention generated-file updates such as `banks.generated.json`. Include screenshots only when a review tool or data source UI is relevant.

## Agent-Specific Instructions

Respond in Chinese when coordinating work in this repository. Before coding, present a plan and wait for confirmation.
