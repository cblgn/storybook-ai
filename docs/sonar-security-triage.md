# Initial Sonar security triage

Snapshot: main `032e482`, analysis `7e871ea8-49a5-420d-b842-f212f2d0e645` on 2026-09-16. All 18 findings were VULNERABILITY / legacy MAJOR (the newer security impact is HIGH), not Security Hotspots. There were no application-code or test findings. Main `8092abf` automatic reanalysis closed them after fixes; no manual resolution, suppression or false-positive classification was used.

| Rule | File | Line | Description | Area / remediation |
|---|---|---|---|---|
| `githubactions:S7637` | `.github/workflows/ci.yml` | 27 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/ci.yml` | 53 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/ci.yml` | 83 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/ci.yml` | 87 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/security.yml` | 26 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/security.yml` | 46 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/sonar.yml` | 27 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/sonar.yml` | 33 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S7637` | `.github/workflows/sonar.yml` | 46 | Use full commit SHA hash for this dependency. | GitHub Actions: pin the verified upstream full SHA |
| `githubactions:S8541` | `.github/workflows/ci.yml` | 32 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/ci.yml` | 33 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/ci.yml` | 34 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/ci.yml` | 35 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/ci.yml` | 86 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/security.yml` | 29 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/sonar.yml` | 30 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `githubactions:S8541` | `.github/workflows/sonar.yml` | 32 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |
| `shell:S8541` | `scripts/dev.sh` | 41 | Omitting "--no-build" can lead to the execution of setup scripts. Make sure it is safe here. | Build configuration: reject new dependency source builds with `--no-build` |

## Root causes and prioritization

1. **CI supply chain (9 findings, S7637):** mutable third-party action references allow upstream tag changes to alter executed code. Full verified commit pins address this risk; Dependabot updates them through review.
2. **Dependency build execution (9 findings, S8541):** installation from source distributions can run dependency build hooks. `--no-build` rejects new third-party source builds. Commands already using `--no-sync` do not install dependencies; adding the flag there is defense in depth, not evidence of a separate exploitable vulnerability. uv may use cached wheels and builds the reviewed first-party editable project.
3. **Application vulnerabilities, dependency advisories, lower-risk findings and Security Hotspots:** none in this snapshot. No human classification or false-positive decision was needed.

These are configuration fixes, not changes to application behavior. The analysis does not prove that the application is free of vulnerabilities. The CI migration retains workflow/script scanning so these security surfaces are not silently omitted.
