import json
from typing import Dict, List

MAX_TEMP = 55


class BatteryReport:
    def __init__(self, log: Dict):
        self.log = log

    def state_of_health(self) -> float:
        nominal = self.log.get("nominal_capacity_kwh", 1)
        measured = self.log.get("measured_capacity_kwh", nominal)
        return round((measured / nominal) * 100, 2)

    def cycle_count(self) -> int:
        return len(self.log.get("cycle_history", []))

    def anomalies(self) -> List[str]:
        issues = []

        # Voltage imbalance
        voltages = self.log.get("cell_voltages", [])
        if voltages:
            diff = max(voltages) - min(voltages)
            if diff > 0.05:
                issues.append(f"Voltage imbalance detected: {diff:.2f}V")

        # Overheating
        temps = self.log.get("cell_temperatures", [])
        if temps:
            max_temp = max(temps)
            if max_temp > MAX_TEMP:
                issues.append(f"Critical Overheating: {max_temp:.1f}°C")

        return issues

    def generate_report(self) -> Dict:
        return {
            "vehicle_id": self.log.get("vehicle_id"),
            "state_of_health_%": self.state_of_health(),
            "cycle_count": self.cycle_count(),
            "anomalies": self.anomalies()
        }


if __name__ == "__main__":
    mock_log = {
        "vehicle_id": "EV1234",
        "timestamp": "2025-09-19T07:30:00Z",
        "cell_voltages": [3.95, 3.96, 3.92, 4.10, 3.97],
        "cell_temperatures": [32.1, 33.0, 34.2, 32.8, 32.5],
        "cycle_history": [
            {"cycle_id": 1, "charged_kwh": 50, "discharged_kwh": 49.5},
            {"cycle_id": 2, "charged_kwh": 52, "discharged_kwh": 51.0}
        ],
        "nominal_capacity_kwh": 60,
        "measured_capacity_kwh": 54
    }

    report = BatteryReport(mock_log).generate_report()
    print(json.dumps(report, indent=2))
