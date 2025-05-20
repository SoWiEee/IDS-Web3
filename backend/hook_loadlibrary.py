import frida
import sys
import requests
import datetime

target_process = "DLL_Injector.exe"

# attach to process
session = frida.attach(target_process)

# Hook: LoadLibraryA, LoadLibraryW
script = session.create_script("""
Interceptor.attach(Module.getExportByName("kernel32.dll", "LoadLibraryA"), {
    onEnter: function (args) {
        var dllName = Memory.readCString(args[0]);
        console.log("[LoadLibraryA] Called with:", dllName);
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "LoadLibraryW"), {
    onEnter: function (args) {
        var dllName = Memory.readUtf16String(args[0]);
        console.log("[LoadLibraryW] Called with:", dllName);
    }
});
""")

# Frida response
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] Message from Frida:", message['payload'])
    elif message['type'] == 'error':
        print("[!] Error:", message['stack'])

# 綁定訊息監聽與載入
script.on("message", on_message)
script.load()

print(f"[*] Hooking LoadLibraryA/W in {target_process} ... Press Ctrl+C to stop.")
sys.stdin.read()
