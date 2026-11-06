# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-06

### Added
- Reusable workflow `scan.yml` with five scanners running in parallel: Gitleaks (secrets), Semgrep (SAST), Trivy (dependencies and container image) and Checkov (Dockerfile and IaC).
- CycloneDX SBOM for the scanned image.
- Security gate job with a summary table, per-scanner outputs and `fail-on-findings`.
- SARIF upload to the GitHub Security tab.
- Self-test against an intentionally vulnerable app and its secure counterpart.
- Dependabot configuration for actions, pip and Docker.
- `CONTRIBUTING.md`, issue templates and a pull request template.

### Fixed
- `secure-app` image no longer ships pip. Its vendored urllib3, msgpack and setuptools carried five HIGH CVEs that made the self-test fail.

[Unreleased]: https://github.com/Kemalstudio/secure-ci-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Kemalstudio/secure-ci-kit/releases/tag/v0.1.0
