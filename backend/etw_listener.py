import win32evtlog
import win32evtlogutil
import win32con
import time
import xml.etree.ElementTree as ET
import requests

def start_etw_listener():
    query = "*[System[Provider[@Name='Microsoft-Windows-Sysmon'] and (EventID=1 or EventID=7)]]"
    #query = "*[System[Provider[@Name='Microsoft-Windows-Sysmon'] and EventID=1]]"
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
                    endpoint = "http://localhost:5000/api/logs"
                    
                    print("[+] Detected process:", payload["image"])


                # Event ID 7 (Image Loaded)
                elif event_id == 7:
                    image_loaded = data.get("ImageLoaded", "").lower()

                    if is_dll_injection(payload, image_loaded):
                        print("[!] DLL Injection detected:", payload["command_line"])
                        payload = {
                            "event_type": "DLL Injection",
                            **base_payload,
                            "detail": f"Suspicious DLL loaded from {image_loaded}"
                        }
                        endpoint = "http://localhost:5000/api/malicious"
                
                
                print(f"[+] Sending event to {endpoint}: {payload}")
                try:
                    r = requests.post(endpoint, json=payload)
                    print("[+] Sent successfully:", r.status_code)
                except Exception as e:
                    print("[-] Failed to send log:", e)


            except Exception as e:
                print("[-] Failed to parse or send event:", e)

        time.sleep(5)


def is_dll_injection(data, image_path):
    suspicious_dlls = ["evil.dll", "injectme.dll"]
    suspicious_paths = ["c:\\temp", "c:\\users\\public"]

    dangerous_targets = ["explorer.exe", "lsass.exe", "svchost.exe"]
    
    process_name = data.get("Image", "").lower()

    # suspicious info
    if any(dll in image_path for dll in suspicious_dlls) or \
       any(p in image_path for p in suspicious_paths):
        return True

    # suspicious inject to process
    if any(target in process_name for target in dangerous_targets):
        return True

    return False


if __name__ == "__main__":
    start_etw_listener()