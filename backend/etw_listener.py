import win32evtlog
import win32evtlogutil
import win32con
import time
import xml.etree.ElementTree as ET
import requests

def send_payload(endpoint, payload):
    try:
        r = requests.post(endpoint, json=payload)
        if r.status_code == 200:
            print("[+] Payload sent successfully")
        else:
            print(f"[!] Failed to send payload: {r.status_code} {r.text}")
    except Exception as e:
        print("[!] Exception when sending payload:", e)

def listen_sysmon():
    query = "*[System[Provider[@Name='Microsoft-Windows-Sysmon'] and (EventID=1)]]"
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

                ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
                event_id = int(root.find('./ns:System/ns:EventID', ns).text)

                data = {d.attrib['Name']: d.text for d in root.findall('.//ns:Data', ns)}
                timestamp = int(time.time())

                # general payload
                base_payload = {
                    "timestamp": timestamp,
                    "image": data.get("Image", ""),
                    "command_line": data.get("CommandLine", ""),
                    "pid": data.get("ProcessId", ""),
                    "user": data.get("User", ""),
                    "integrity_level": data.get("IntegrityLevel", "")
                }

                # Event ID 1 (Process Created)
                if event_id == 1:
                    payload = {
                        "event_type": "Process Created",
                        **base_payload
                    }

                    print("[+] Detected process:", payload["image"])
                    endpoint = "http://localhost:5000/api/logs"
                    send_payload(endpoint, payload)
                    
            except Exception as e:
                print("[-] Failed to parse or send event:", e)

        time.sleep(5)


def listen_security_log():
    logtype = 'Security'
    query = "*[System[Provider[@Name='Microsoft-Windows-Security-Auditing'] and EventID=4624]]"
    flags = win32evtlog.EvtQueryReverseDirection | win32evtlog.EvtQueryChannelPath

    try:
        hand = win32evtlog.EvtQuery(logtype, flags, query)
    except Exception as e:
        print("[!] Failed to query Security log:", e)
        return
    
    seen_records = set()

    while True:
        try:
            events = win32evtlog.EvtNext(hand, 10)
        except Exception as e:
            print("[!] Failed to read Security log:", e)
            time.sleep(1)
            continue

        if not events:
            time.sleep(1)
            continue

        for event in events:
            try:
                xml_str = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
                root = ET.fromstring(xml_str)
                ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}

                event_id = int(root.find('./ns:System/ns:EventID', ns).text)
                record_id = int(root.find('./ns:System/ns:EventRecordID', ns).text)

                if record_id in seen_records:
                    continue
                seen_records.add(record_id)

                if event_id == 4624:
                    timestamp = int(time.time())
                    data = {d.attrib['Name']: d.text for d in root.findall('.//ns:Data', ns)}

                    payload = {
                        "event_type": "Logon",
                        "timestamp": timestamp,
                        "image": data.get("ProcessName", ""),
                        "command_line": data.get("LogonProcessName", ""),
                        "pid": int(data.get("ProcessId", ""), 16),
                        "user": data.get("TargetUserName", ""),
                        "integrity_level": data.get("ImpersonationLevel", ""),
                        "detail": data.get("LogonType", "")
                    }

                    print("[+] Detected Logon event:", payload["user"])
                    endpoint = "http://localhost:5000/api/malicious"
                    send_payload(endpoint, payload)

            except Exception as e:
                print("[!] Failed to parse Logon event:", e)

        time.sleep(1)


def listen_sysmon_registry():
    logtype = 'Microsoft-Windows-Sysmon/Operational'
    query = "*[System[Provider[@Name='Microsoft-Windows-Sysmon'] and (EventID=13 or EventID=14)]]"
    flags = win32evtlog.EvtQueryReverseDirection | win32evtlog.EvtQueryChannelPath

    try:
        hand = win32evtlog.EvtQuery(logtype, flags, query)
    except Exception as e:
        print("[!] Failed to query Sysmon log:", e)
        return

    seen_records = set()

    while True:
        try:
            events = win32evtlog.EvtNext(hand, 10)
        except Exception as e:
            print("[!] Failed to read Sysmon log:", e)
            time.sleep(1)
            continue

        if not events:
            time.sleep(1)
            continue

        for event in events:
            try:
                xml_str = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
                root = ET.fromstring(xml_str)
                ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}

                record_id = int(root.find('./ns:System/ns:EventRecordID', ns).text)

                if record_id in seen_records:
                    continue
                seen_records.add(record_id)

                timestamp = int(time.time())
                data = {d.attrib['Name']: d.text for d in root.findall('.//ns:Data', ns)}

                payload = {
                    "event_type": "Registry " + data.get("EventType", ""),
                    "timestamp": timestamp,
                    "command_line": data.get("TargetObject", ""),
                    "image": data.get("Image", ""),
                    "user": data.get("User", ""),
                    "pid": data.get("ProcessID", ""),
                    "integrity_level": data.get("ImpersonationLevel", ""),
                    "detail": data.get("Details", "")
                }

                print("[+] Registry Event Detected:", payload["command_line"])
                endpoint = "http://localhost:5000/api/malicious"
                send_payload(endpoint, payload)

            except Exception as e:
                print("[!] Failed to parse Sysmon event:", e)

        time.sleep(1)

if __name__ == "__main__":
    print("[*] Started Sysmon and Security Log listeners")