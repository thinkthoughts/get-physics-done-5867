# Get Physics Done 5867 (GPD-5867)

### Physics workflow fork for open research verification

[![CI](https://github.com/psi-oss/get-physics-done/actions/workflows/test.yml/badge.svg)](https://github.com/psi-oss/get-physics-done/actions/workflows/test.yml)\
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/psi-oss/get-physics-done/blob/main/LICENSE)\
[![Python
3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)\
[![npm](https://img.shields.io/npm/v/get-physics-done)](https://www.npmjs.com/package/get-physics-done)\
![arXiv workflow](https://img.shields.io/badge/arXiv-workflow_5867-blue)

**Get Physics Done 5867 (GPD-5867)** is a research-workflow fork of\
**Get Physics Done (GPD)** from Physical Superintelligence PBC.

This fork focuses on **open verification workflows around physics
papers**, especially arXiv research discussions and reproducible
derivations.

Primary research loop:

observe → verify → revise

Research discussions and artifacts are tracked through:

#arXiv5867

------------------------------------------------------------------------

# Who This Is For

GPD-5867 is intended for:

-   physicists exploring new arXiv results\
-   researchers verifying derivations or numerical claims\
-   collaborators documenting research artifacts\
-   open scientific discussion tied to reproducible workflows

The fork keeps GPD's structured research system while adding a
**lightweight public research layer**.

------------------------------------------------------------------------

# Quick Start

Install GPD:

``` bash
npx -y get-physics-done
```

Open your runtime:

    claude
    gemini
    codex
    opencode

Run help:

    /gpd:help

Start a project:

    /gpd:new-project

Or map existing research:

    /gpd:map-research

Typical loop:

    new-project → plan-phase → execute-phase → verify-work

------------------------------------------------------------------------

# Differences From Upstream

`get-physics-done-5867` keeps the core GPD workflow but adds a
lightweight public research layer centered around physics papers and
verification loops.

### arXiv-first workflow

Research discussions are organized around new papers and tracked with:

    #arXiv5867

### Public verification loop

Research progresses through:

    observe → verify → revise

Engineering analogue:

    rough consensus + running code

### Diagram-first explanation

Concepts are often communicated using simple geometric anchors.

Example reference geometry:

    cosθ = 1/√2
    θ = 45°

### Open research discussion

This fork encourages public physics discussion tied to reproducible
artifacts stored in the repository.

------------------------------------------------------------------------

# Example Workflow

A typical cycle begins with a new physics paper.

### Identify a paper

    arXiv:2603.01575

### Create a workspace

    papers/
      2603.01575/
        summary.md
        key-equations.md
        verification.py
        diagrams/

### Run workflow

    /gpd:map-research
    /gpd:plan-phase 1
    /gpd:execute-phase 1
    /gpd:verify-work 1

### Record the loop

    observe → verify → revise

### Produce artifacts

Typical outputs include:

-   derivation notes\
-   verification scripts\
-   numerical checks\
-   diagrams\
-   manuscript drafts

### Publish

    /gpd:write-paper
    /gpd:arxiv-submission

------------------------------------------------------------------------

# Example Result

Example artifact produced through the workflow.

Paper:

    arXiv:2603.01575

Reference geometry:

    cosθ = 1/√2
    θ = 45°

Artifacts:

    papers/2603.01575/
      summary.md
      key-equations.md
      verification.py
      diagrams/

Verification typically includes:

-   dimensional analysis\
-   limiting cases\
-   numerical convergence\
-   comparison with literature

------------------------------------------------------------------------

# Active Papers

  arXiv        Topic                                  Status
  ------------ -------------------------------------- ---------
  2603.01575   intersubjective observables            mapping
  2603.04792   gravitational-wave signal extraction   review
  2603.xxxxx   music & neurocognition metaphor        notes

Each paper gets a structured workspace:

    papers/
      arxiv-id/
        summary.md
        key-equations.md
        verification.py
        diagrams/

Research proceeds through:

    observe → verify → revise

------------------------------------------------------------------------

# Original Project

This fork builds on:

**Get Physics Done (GPD)**\
https://github.com/psi-oss/get-physics-done

Developed by **Physical Superintelligence PBC**.

GPD-5867 extends the workflow for open research verification through
**AntiviolentIntelligence.ai**, inspired by **Cantor's diagonal
argument** as a model for iterative discovery and verification.

------------------------------------------------------------------------

# System Requirements

-   Node.js with `npm` / `npx`
-   Python 3.11+
-   Network access to npm and GitHub
-   One supported runtime:

```{=html}
<!-- -->
```
    Claude Code
    Gemini CLI
    Codex
    OpenCode

------------------------------------------------------------------------

# License

Apache License 2.0

See the LICENSE file.

------------------------------------------------------------------------

# Citation

If GPD contributes to published research, please cite the upstream
project:

``` bibtex
@software{physical_superintelligence_2026_gpd,
  author = {{Physical Superintelligence PBC}},
  title = {Get Physics Done (GPD)},
  version = {1.1.0},
  year = {2026},
  url = {https://github.com/psi-oss/get-physics-done},
  license = {Apache-2.0}
}
```
