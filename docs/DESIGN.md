# Technical design

## Scope

This is a deterministic, offline demo of incident triage. It intentionally does not contact devices, send notifications, or modify resolver settings.

## Detection rules

1. Missing or unreachable observation -> `UNREACHABLE`.
2. Reachable observation with at least one DNS resolver and all resolvers approved -> `HEALTHY`.
3. Any other reachable observation -> `DNS_MISMATCH`.

Each non-healthy device produces one simulated ticket and one simulated notification. All output is JSON so it can be inspected independently.

## Future improvements

A production implementation would include signed/authenticated telemetry, schema validation, rate limiting, retries, ticket deduplication, secure secrets, and change approvals before remediation.
