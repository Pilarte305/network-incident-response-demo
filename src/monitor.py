"""Offline DNS drift simulation. Never connects to or changes network devices."""
import argparse
import csv
import json
from pathlib import Path

APPROVED_DNS = frozenset({"192.0.2.53", "192.0.2.54"})


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def analyze(inventory, observations):
    """Produce reproducible simulated incidents from example input records."""
    observed_by_id = {row["device_id"]: row for row in observations}
    devices, tickets, notifications = [], [], []
    for item in inventory:
        device_id, name = item["device_id"], item["name"]
        observation = observed_by_id.get(device_id)
        if observation is None or observation["reachable"].strip().lower() != "yes":
            status, detail = "UNREACHABLE", "No reachable observation available"
        else:
            resolvers = {v.strip() for v in observation["dns_servers"].split(";") if v.strip()}
            if resolvers and resolvers.issubset(APPROVED_DNS):
                status, detail = "HEALTHY", "Observed DNS resolvers are approved"
            else:
                status, detail = "DNS_MISMATCH", "Observed DNS resolvers need review"
        devices.append({"device_id": device_id, "name": name, "status": status, "detail": detail})
        if status != "HEALTHY":
            ticket_id = f"DEMO-{device_id}"
            tickets.append({"ticket_id": ticket_id, "device_id": device_id, "category": status, "state": "open", "simulated": True})
            notifications.append({"ticket_id": ticket_id, "subject": f"Simulated alert: {name} {status}", "simulated": True})
    return {"mode": "offline_simulation", "devices": devices, "tickets": tickets, "notifications": notifications}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=Path("data/devices.csv"))
    parser.add_argument("--observations", type=Path, default=Path("data/observations.csv"))
    parser.add_argument("--output", type=Path, default=Path("incident-report.json"))
    args = parser.parse_args()
    report = analyze(read_csv(args.inventory), read_csv(args.observations))
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for device in report["devices"]:
        print(f'{device["name"]}: {device["status"]}')
    print(f"Report saved: {args.output}")


if __name__ == "__main__":
    main()
