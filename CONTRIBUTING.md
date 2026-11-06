# Contributing to secure-ci-kit

Thanks for helping! Bug reports, false-positive reports, docs fixes and new features are all welcome.

## Reporting

- **Bug or false positive:** open an issue with the workflow snippet you use, a link to the failing run (or the job summary), and what you expected.
- **Vulnerability in the kit itself:** do not open a public issue. See [SECURITY.md](SECURITY.md).
- **Idea:** open an issue first for anything bigger than a small fix, so we can agree on the approach before you write code.

Good places to start are issues labelled [`good first issue`](https://github.com/Kemalstudio/secure-ci-kit/labels/good%20first%20issue) and the [Roadmap](README.md#roadmap).

## How the repository is laid out

| Path | What it is |
| :--- | :--- |
| `.github/workflows/scan.yml` | The reusable workflow that users call. This is the product. |
| `.github/workflows/self-test.yml` | Runs `scan.yml` against both example apps on every push, PR and Monday. |
| `examples/vulnerable-app` | One classic bug per endpoint. Every scanner **must** find something here. |
| `examples/secure-app` | The same app with every bug fixed. The gate **must** pass with zero findings. |

## Making a change

1. Fork the repository and create a branch from `main`.
2. Make your change. If you touch `scan.yml`, keep the rules in [The kit follows its own advice](README.md#the-kit-follows-its-own-advice):
   - pin new actions by full commit SHA and new container images by digest, with the version in a comment or tag;
   - give each job only the permissions it needs;
   - pass inputs to shell scripts through `env:`, never with `${{ }}` inside `run:`;
   - a scanner that crashes must make the gate fail, never look like a clean result.
3. If you add or change a scanner, update **both** examples:
   - add a bug to `vulnerable-app` that the scanner catches, and list it in its README;
   - make sure `secure-app` still has zero findings.
4. Update `README.md` (inputs, outputs, tables) and add a line under `## [Unreleased]` in `CHANGELOG.md`.
5. Open a pull request. The self-test runs on it automatically and must be green.

### Checking locally

Lint the workflows the same way CI does:

```bash
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.12 -color
```

Run a single scanner on an example (see [Run the scanners locally](README.md#run-the-scanners-locally) for the others):

```bash
docker run --rm -v "$PWD:/src" -w /src semgrep/semgrep:1.181.0 semgrep scan --config p/default examples/secure-app
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `ci:`, `chore:`. Keep the subject line short and in the imperative mood ("add", not "added").

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
