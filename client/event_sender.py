import win32evtlog
import requests
import time
import datetime

# Event Type
WATCHED_EVENT_IDS = {
    4624: "登入成功",
    4625: "登入失敗",
    4720: "帳號建立",
    4672: "特殊權限登入"
}

def send_event(event_id, timestamp):
    url = 'http://localhost:5000/record_event'
    data = {
        "event_type": f"Security:{WATCHED_EVENT_IDS.get(event_id, 'Unknown')}",
        "timestamp": timestamp
    }
    try:
        r = requests.post(url, json=data)
        print(f"[+] Sent: {event_id} at {timestamp}")
    except Exception as e:
        print(f"[-] Error sending: {e}")

def read_security_logs():
    server = 'localhost'
    log_type = 'Security'
    hand = win32evtlog.OpenEventLog(server, log_type)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    seen_events = set()  # prevent duplicate send

    print("[*] Monitoring Windows Security Events...")

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            time.sleep(5)
            continue

        for event in events:
            if event.EventID in WATCHED_EVENT_IDS:
                event_key = (event.RecordNumber, event.EventID)
                if event_key not in seen_events:
                    timestamp = int(event.TimeGenerated.timestamp())
                    send_event(event.EventID, timestamp)
                    seen_events.add(event_key)
        time.sleep(2)

if __name__ == "__main__":
    read_security_logs()
