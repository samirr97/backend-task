# 🔋 EV Battery Health Report

This module processes **EV diagnostic logs** and generates a simple **battery health report**.  
It’s meant as a starting point for analyzing EV battery performance and detecting issues.  

---

## 📌 Features
- Calculate **Battery State of Health (SOH)** in %  
- Count **charge/discharge cycles**  
- Detect **anomalies**:
  - Voltage imbalance between cells  
  - Overheating cells  

---

## 📝 Example Log Schema

A sample diagnostic log looks like this:

```json
{
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
```

---

## ⚙️ How It Works

1. **SOH (State of Health)**  
   \[
   SOH = \frac{\text{Measured Capacity}}{\text{Nominal Capacity}} \times 100
   \]

   Example: 54 ÷ 60 × 100 = **90%**

2. **Cycle Count**  
   The number of entries in `cycle_history`.

3. **Anomalies**  
   - **Voltage imbalance** → flag if max-min > `0.05V`  
   - **Overheating** → warning if >45°C, critical if >55°C  

---

## 🚀 Usage

```bash
python battery_report.py
```

Example output:

```json
{
  "vehicle_id": "EV1234",
  "state_of_health_%": 90.0,
  "cycle_count": 2,
  "anomalies": [
    "Voltage imbalance detected: 0.18V"
  ]
}
```
---

## 🏗️ Future / Production Considerations
If this were a production system:
- **API Integration**: expose an endpoint (`/battery/report`) for garages to upload logs.  
- **Database Flow**:  
  - Store raw logs in a time-series DB (InfluxDB, TimescaleDB).  
- **Edge Cases**:  
  - Handle missing/invalid data (e.g., negative voltage).  
  - Stream processing for very large logs.  
- **Scalability**:  
  - Process logs asynchronously with message queues (Kafka, RabbitMQ).  

---
