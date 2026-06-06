---
description: Quick guide for creating and verifying the mamba/conda environment for this Jupyter Book v2 site, installing Python, MyST, and Node.js dependencies in one step.
---

# Environment installation workflow

Use the repo-local `environment.yml` with **mamba**. This installs Python, Jupyter Book 2 / MyST, and **Node.js** in one shot.

## Create the environment

```bash
mamba env create -f environment.yml
mamba activate hywebv2
```

## Verify the toolchain

```bash
python --version
myst --version
jupyter-book --version
node --version
```

## Update an existing environment

```bash
mamba env update -n hywebv2 -f environment.yml --prune
```

## Notes

- A separate system-wide Node.js install is **not** required for this project if the environment was created from `environment.yml`.
- Run all book build commands from inside the activated `hyweb` environment.
