# vulnerable-app

> ⚠️ **Intentionally vulnerable. Never deploy this.**

A tiny Flask app with one classic bug per endpoint. It exists so the self-test can
prove that every scanner in secure-ci-kit actually finds something.

| Where | Bug | Caught by |
| :--- | :--- | :--- |
| `app.py` | Hardcoded `SECRET_KEY` | Gitleaks |
| `app.py` `/users` | SQL injection (f-string query) | Semgrep |
| `app.py` `/ping` | Command injection (`os.system`) | Semgrep |
| `app.py` `/hello` | Template injection (`render_template_string`) | Semgrep |
| `app.py` `/config` | Unsafe deserialization (`yaml.load`) | Semgrep |
| `app.py` | Flask debug mode on `0.0.0.0` | Semgrep |
| `requirements.txt` | Outdated Flask, Jinja2, PyYAML, requests | Trivy (filesystem) |
| `Dockerfile` | EOL base image, root user, `ADD`, port 22, no healthcheck | Checkov, Trivy (image) |
| `k8s/deployment.yaml` | Privileged container, host network, plain-text password | Checkov |

The fixed version of every bug is in [`../secure-app`](../secure-app).

GitHub's Dependabot will report alerts for this folder. That is expected:
`.github/dependabot.yml` deliberately does not open update PRs for it.
