import win32evtlog
import win32evtlogutil
import win32con
import time
import xml.etree.ElementTree as ET
import requests

def start_etw_listener():
    query = "*[System[Provider[@Name='Microsoft-Windows-Sysmon'] and EventID=1]]"
    log_type = "Microsoft-Windows-Sysmon/Operational"
    flags = win32evtlog.EvtQueryReverseDirection | win32evtlog.EvtQueryChannelPath
    handle = win32evtlog.EvtQuery(log_type, flags, query)

    while True:
        try:
            events = win32evtlog.EvtNext(handle, 10)
        except Exception as e:
            print("[!] Failed to get events:", e)
            time.sleep(1)
            continue

        for evt in events:
            try:
                xml_str = win32evtlog.EvtRender(evt, win32evtlog.EvtRenderEventXml)
                root = ET.fromstring(xml_str)

                data = {elem.attrib['Name']: elem.text for elem in root.findall(".//EventData/Data")}

                image = data.get("Image", "")
                command_line = data.get("CommandLine", "")
                pid = data.get("ProcessId", "")

                payload = {
                    "event_type": f"Process Created: {image} {command_line} (PID: {pid})",
                    "timestamp": int(time.time())
                }

                print("[+] Detected process:", payload["event_type"])

                try:
                    r = requests.post("http://localhost:5000/record_event", json=payload)
                    print("[+] Log sent to backend:", r.status_code, r.text)
                except Exception as e:
                    print("[-] Failed to send log:", e)

            except Exception as e:
                print("[-] Failed to parse or send event:", e)

        time.sleep(5)

if __name__ == "__main__":
    start_etw_listener()