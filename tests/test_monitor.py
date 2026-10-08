import unittest
from src.monitor import analyze


class MonitoringTests(unittest.TestCase):
    def test_detects_healthy_mismatch_and_unreachable(self):
        inventory = [{"device_id": "1", "name": "a"}, {"device_id": "2", "name": "b"}, {"device_id": "3", "name": "c"}]
        observations = [
            {"device_id": "1", "reachable": "yes", "dns_servers": "192.0.2.53"},
            {"device_id": "2", "reachable": "yes", "dns_servers": "203.0.113.53"},
            {"device_id": "3", "reachable": "no", "dns_servers": ""},
        ]
        report = analyze(inventory, observations)
        self.assertEqual([x["status"] for x in report["devices"]], ["HEALTHY", "DNS_MISMATCH", "UNREACHABLE"])
        self.assertEqual(len(report["tickets"]), 2)
        self.assertTrue(all(x["simulated"] for x in report["notifications"]))

    def test_missing_observation_is_unreachable(self):
        report = analyze([{"device_id": "4", "name": "d"}], [])
        self.assertEqual(report["devices"][0]["status"], "UNREACHABLE")

    def test_empty_dns_is_mismatch(self):
        report = analyze([{"device_id": "5", "name": "e"}], [{"device_id": "5", "reachable": "yes", "dns_servers": ""}])
        self.assertEqual(report["devices"][0]["status"], "DNS_MISMATCH")


if __name__ == "__main__":
    unittest.main()
