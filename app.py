import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

latest = {
    "temperature": 0, "humidity": 0, "vibration": 0,
    "current": 0, "voltage": 0, "gas": 0,
    "status": "OFFLINE", "machine": "WAITING FOR NODEMCU",
    "alerts": ["Waiting for ESP8266 sensor data."],
    "time": "--"
}

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/sensors")
def get_sensors():
    return jsonify(latest)

@app.post("/api/sensor-data")
def sensor_data():
    global latest
    data = request.get_json(silent=True) or {}

    def num(name, default=0):
        try:
            return float(data.get(name, default))
        except (TypeError, ValueError):
            return default

    temperature = num("temperature")
    humidity = num("humidity")
    vibration = num("vibration")
    current = num("current")
    voltage = num("voltage")
    gas = num("gas")

    alerts = []
    if temperature > 40: alerts.append("High temperature detected")
    elif temperature > 37: alerts.append("Temperature warning")
    if vibration > 2.5: alerts.append("High vibration detected")
    elif vibration > 1.8: alerts.append("Vibration warning")
    if gas > 200: alerts.append("High gas level detected")
    elif gas > 160: alerts.append("Gas level warning")
    if current > 4.5: alerts.append("High current detected")

    status = "CRITICAL" if any(x in " ".join(alerts) for x in
                               ["High temperature", "High vibration", "High gas", "High current"]) \
             else ("WARNING" if alerts else "NORMAL")

    latest = {
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "vibration": round(vibration, 2),
        "current": round(current, 2),
        "voltage": round(voltage, 2),
        "gas": round(gas, 2),
        "status": status,
        "machine": "STOP REQUIRED" if status == "CRITICAL" else "RUNNING",
        "alerts": alerts,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    return jsonify({"ok": True, "data": latest})

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
