# secure-app

The fixed version of [`../vulnerable-app`](../vulnerable-app): same endpoints, every bug fixed.
The self-test requires this folder to pass **all** scanners with zero findings.

| Bug in vulnerable-app | Fix here |
| :--- | :--- |
| Hardcoded `SECRET_KEY` | Read from the environment; the app refuses to start without it |
| SQL injection | Parameterized query (`?` placeholder) |
| Command injection in `/ping` | No shell: input must be a public IP address, checked with a TCP connect |
| Template injection in `/hello` | Input returned as JSON data, never rendered |
| `yaml.load` deserialization | `request.get_json()`: plain data only |
| Debug mode on `0.0.0.0` | gunicorn in the container; dev server on localhost with debug off |
| Outdated dependencies | Current versions, all pinned, updated by Dependabot |
| EOL base image, root user, `ADD`, port 22 | Supported Alpine image pinned by digest, non-root user, `COPY`, port 8000 only |
| No healthcheck | `HEALTHCHECK` on `/health` |

## Run it

```bash
docker build -t secure-app .
docker run --rm -p 8000:8000 -e SECRET_KEY="$(openssl rand -hex 32)" secure-app
curl http://localhost:8000/health
```
