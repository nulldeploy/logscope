# logscope

> A terminal-native log analysis tool — parse, analyze, and watch log files in real time, without writing a single grep pipeline.

[![CI/CD](https://github.com/nulldeploy/logscope/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nulldeploy/logscope/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Why logscope?

Debugging a misbehaving service usually starts the same way: SSH into a box, run `tail -f app.log | grep ERROR`, squint at unformatted text, and manually count how many times the same exception fired. **logscope** replaces that ad-hoc workflow with three focused commands that do it properly — colorized output, aggregated statistics, and a live-following watch mode.

No database. No web server. Just a fast, single-purpose CLI that reads files and gets out of your way.

```bash
$ logscope stats --file app.log

Total lines : 1,240
ERROR       : 87
WARN        : 203
INFO        : 950

Top errors:
  42x  Connection timeout to db:5432
  18x  Failed to fetch /api/users
   9x  Permission denied: /var/log/app
```

---

## Features

| Command          | What it does                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| `logscope parse` | Reads a log file and prints it with color-coded severity levels. Filter by level or keyword.                 |
| `logscope stats` | Aggregates a log file into a summary: total lines, severity breakdown, and the most frequent error messages. |
| `logscope watch` | Tails a file in real time, applying the same filtering and coloring — a smarter `tail -f`.                   |
| `logscope serve` | Exposes a `/health` endpoint over HTTP, for container orchestration and uptime checks.                       |

---

## Quick start

### Run locally

```bash
git clone https://github.com/nulldeploy/logscope.git
cd logscope
pip install -r requirements.txt

python logscope.py parse --file app.log --level ERROR
python logscope.py stats --file app.log
python logscope.py watch --file app.log --grep "timeout"
```

### Run with Docker

```bash
docker pull ghcr.io/nulldeploy/logscope:latest
docker run -v $(pwd)/logs:/app/logs ghcr.io/nulldeploy/logscope:latest python logscope.py stats --file /app/logs/app.log
```

### Run the HTTP service

```bash
docker compose up -d
curl http://localhost:5000/health
```

---

## Usage examples

**Parse with level filtering:**

```bash
logscope parse --file app.log --level ERROR
```

**Parse with keyword search:**

```bash
logscope parse --file app.log --grep "timeout"
```

**Get a statistical summary:**

```bash
logscope stats --file app.log
```

**Watch a log live, filtered to one severity:**

```bash
logscope watch --file app.log --level ERROR
```

---

## Architecture

The codebase is split by responsibility — each module does exactly one thing, which keeps the CLI layer thin and the core logic independently testable.

```
logscope/
├── cli/                # One file per subcommand; argparse wiring lives here
│   ├── parse.py
│   ├── stats.py
│   └── watch.py
├── core/
│   ├── reader.py        # Opens a file, yields lines — no parsing logic
│   ├── parser.py        # Extracts level / timestamp / message from a raw line via regex
│   ├── analyzer.py      # Aggregates parsed lines into statistics (Counter-based)
│   └── watcher.py        # Polls a file for new bytes and streams matches
├── utils/
│   └── colors.py        # Severity → color mapping for terminal output
├── serve.py              # Minimal Flask app exposing /health
├── logscope.py           # Entry point — dispatches to cli/ subcommands
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

**Design principle:** `core/` has no knowledge of the CLI, and the CLI has no knowledge of how parsing works internally. `reader.py` only reads, `parser.py` only parses, `analyzer.py` only aggregates — each one is replaceable and testable in isolation.

---

## Tech stack

| Layer                | Choice                       | Why                                                                     |
| -------------------- | ---------------------------- | ----------------------------------------------------------------------- |
| CLI framework        | `argparse`                   | Standard library — zero extra dependencies for a CLI tool               |
| Output formatting    | `rich`                       | Color, tables, and live-updating output without hand-rolling ANSI codes |
| Statistics           | `collections.Counter`        | Built-in, O(n) frequency counting — no need for a heavier data tool     |
| Parsing              | `re`                         | Log lines are semi-structured text; regex is the right-sized tool here  |
| HTTP health endpoint | `Flask`                      | Lightweight enough that it doesn't outweigh the CLI it's attached to    |
| Containerization     | `Docker` (multi-stage build) | Reproducible runtime, small final image, no system Python pollution     |
| CI/CD                | `GitHub Actions`             | Lint → test → build → push to GHCR on every push to `main`              |

---

## Deployment

logscope ships with a production-oriented Docker setup:

- **Multi-stage Dockerfile** — dependencies are installed into an isolated `/install` prefix in a builder stage, then copied into a `python:3.12-slim` runtime image. The final image carries no compiler toolchain, no pip cache, and no build-time cruft.
- **Non-root user** — the application runs as an unprivileged `appuser`, not root, limiting the blast radius of any container-level compromise.
- **Built-in healthcheck** — Docker's `HEALTHCHECK` polls `/health` every 15 seconds, so orchestrators (or a plain `docker ps`) can tell at a glance whether the service is actually serving traffic, not just running.
- **CI/CD pipeline** — every push to `main` runs linting (`ruff`) and tests (`pytest`), then builds and pushes a tagged image to GitHub Container Registry (`ghcr.io`).

```dockerfile
# Builder stage — installs dependencies into an isolated prefix
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage — slim image, only what's needed to run
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
RUN useradd -r -s /bin/false appuser
HEALTHCHECK --interval=15s --timeout=10s --start-period=5s --retries=2 \
    CMD python -c 'import urllib.request; urllib.request.urlopen("http://localhost:5000/health")' || exit 1
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 5000
CMD ["python", "logscope.py", "serve"]
```

For full server provisioning — nginx, SSL via Let's Encrypt, systemd service management — see the companion [`logscope-infra`](https://github.com/nulldeploy/logscope-infra) repository, which automates the entire setup with Ansible.

---

## Roadmap

- [ ] JSON-formatted log input support
- [ ] Configurable output templates
- [ ] Export `stats` output to CSV/JSON
- [ ] Prometheus metrics endpoint alongside `/health`

---

## License

MIT — see [LICENSE](LICENSE) for details.
