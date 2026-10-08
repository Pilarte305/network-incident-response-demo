# Network Incident Response Automation — Portfolio Demo

**Python · Network Monitoring · DNS Validation · Incident Response · Logging**

A self-contained demonstration of a network incident-response workflow. This independent portfolio project uses **fictional devices and simulated observations** to show how a monitoring tool can detect unauthorized DNS resolvers, classify incidents, generate helpdesk tickets, and produce an audit trail.

> **Safe by design:** This demo does not connect to hosts, change DNS configurations, send emails, or call real ticketing APIs. It does not contain WGU lab files or solutions.

## What it demonstrates

- Parse a CSV device inventory and a separate set of simulated DNS observations.
- Compare observed resolvers against an approved DNS allowlist.
- Distinguish healthy, misconfigured, and unreachable devices.
- Generate structured incident tickets and notification records.
- Write JSON output for downstream analysis and auditability.
- Exercise the behavior with automated unit tests.

## Workflow

```text
Inventory CSV + Simulated Observations CSV
                    |
                    v
        Validate observed DNS settings
                    |
         +----------+-----------+
         |          |           |
       Healthy   DNS drift   Unreachable
         |          |           |
      Log OK    Ticket +     Ticket +
               notification  notification
                    |           |
                    +-----+-----+
                          v
                JSON incident report
```

## Quick start

Requires **Python 3.10+**. No third-party packages needed.

```bash
python -m src.monitor --inventory data/devices.csv --observations data/observations.csv --output incident-report.json
python -m unittest discover -s tests -v
```

You can inspect `incident-report.json` to see each device's status, simulated ticket records, and notification messages. The project never performs an actual network connection.

## Example output

```text
web-edge: HEALTHY
app-node: DNS_MISMATCH
backup-node: UNREACHABLE
Report saved: incident-report.json
```

## Structure

```text
network-incident-response-demo/
├── README.md
├── src/
│   ├── __init__.py
│   └── monitor.py
├── data/
│   ├── devices.csv
│   └── observations.csv
├── tests/
│   └── test_monitor.py
├── docs/
│   └── DESIGN.md
├── .github/workflows/
│   └── python-tests.yml
├── .gitignore
└── LICENSE
```

## Design choices

The two inputs are intentionally separate: the device inventory describes what should exist, while observations represent what monitoring *might* discover. This avoids implying that the demo performs live scanning. Incident IDs are deterministic for sample runs, and report content is machine-readable for integration into other training projects.

## Security and limitations

- No privileged operations, SSH connections, credential storage, or network writes.
- All IP addresses are reserved for examples (RFC 5737), not active targets.
- No real email or helpdesk integration; records are only simulated.
- A production system would require authenticated sources, secret management, resilient queues, authorization for changes, and safe incident deduplication.

## Skills represented

Python programming, CSV parsing, validation, rule-based detection, structured logging, incident triage, JSON reporting, unit testing, GitHub Actions, and secure demo design.

---

*Independent portfolio demonstration using fictional infrastructure. Not an operational security product or a reproduction of proprietary/course assessment material.*
