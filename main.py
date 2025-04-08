from fastapi import FastAPI, Request
from datetime import datetime
import csv
import os

app = FastAPI()

LOG_PATH = "alert_log.csv"
os.makedirs("data", exist_ok=True)
log_file = os.path.join("data", LOG_PATH)

# Create the log file with header if it doesn't exist
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "event_type", "raw_payload"])

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        event_type = payload.get("type", "unknown")
        now = datetime.utcnow().isoformat()

        # Log to CSV
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, event_type, str(payload)])

        print(f"✅ Alert received: {event_type}")
        return {"status": "ok", "received": event_type}

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return {"status": "error", "detail": str(e)}

# ✅ Add this to handle GET requests (Render health check or browser hit)
@app.get("/webhook")
def webhook_health_check():
    print("🧠 GET /webhook ping received.")
    return {"status": "alive", "message": "Irrixa webhook endpoint is online."}
