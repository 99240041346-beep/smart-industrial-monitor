# Smart Industrial Monitor — Public Deployment

This version is designed for a public cloud URL, not localhost.

## Deploy to Render
Render's current Flask deployment uses:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`

You can connect the repository to Render as a Python Web Service.

## Files
- `app.py` — Flask API + website
- `templates/index.html` — live dashboard
- `requirements.txt` — dependencies
- `render.yaml` — Render configuration
- `esp8266/industrial_monitor.ino` — NodeMCU example

## NodeMCU
After deployment, copy the public Render URL into:
`SERVER_URL = "https://YOUR-APP.onrender.com/api/sensor-data";`

The NodeMCU and the public Render server do NOT need to be on the same Wi-Fi network. The ESP8266 only needs internet access.

## SMS
The website contains a recipient-number field. To send actual SMS alerts, connect the Flask alert handler to a provider such as Twilio and store provider credentials as Render environment variables. Twilio recommends environment variables for production credentials.

## Security
Do not put Twilio Account SID/Auth Token in HTML or ESP8266 firmware.
For a real industrial deployment, add authentication/API keys to the NodeMCU endpoint, HTTPS certificate validation, rate limiting, and persistent storage.
