import frida
import requests
import time
import sys

def on_message(message, data):
    if message["type"] == "send":
        payload = message["payload"]
        dll_name = payload.get("dll")
        function = payload.get("function")

        timestamp = int(time.time())

        post_data = {
            "event_type": "DLL Injection",
            "timestamp": timestamp,
            "image": dll_name,
            "command_line": f"{function}('{dll_name}')",
            "pid": 0,
            "user": "Unknown",
            "integrity_level": "Unknown",
            "detail": f"Suspicious DLL loaded via {function}"
        }

        try:
            r = requests.post("http://localhost:5000/api/malicious", json=post_data)
            if r.status_code == 200:
                print(f"[+] Sent to API: {dll_name}")
            else:
                print(f"[!] Failed to send: {r.status_code}")
        except Exception as e:
            print(f"[!] Error sending POST: {e}")
    elif message["type"] == "error":
        print(f"[!] Frida script error: {message['stack']}")

def start_frida_hooking(target_process="DLL_Injector.exe"):
    print(f"[*] Hooking {target_process} with Frida...")

    session = frida.attach(target_process)
    script = session.create_script("""
    Interceptor.attach(Module.getExportByName("kernel32.dll", "LoadLibraryA"), {
        onEnter: function (args) {
            var dllName = Memory.readCString(args[0]);
            send({
                dll: dllName,
                function: "LoadLibraryA"
            });
        }
    });
    Interceptor.attach(Module.getExportByName("kernel32.dll", "LoadLibraryW"), {
        onEnter: function (args) {
            var dllName = Memory.readUtf16String(args[0]);
            send({
                dll: dllName,
                function: "LoadLibraryW"
            });
        }
    });
    """)
    script.on("message", on_message)
    script.load()

    sys.stdin.read()
