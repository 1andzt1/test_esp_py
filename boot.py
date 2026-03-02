import network
import time
import webrepl

# ---------- WiFi ----------
SSID = "ZYTOBLENERGO"
PASSWORD = "zhuiko12sdtu"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(SSID, PASSWORD)

    timeout = 10
    while timeout > 0:
        if wlan.isconnected():
            break
        time.sleep(1)
        timeout -= 1

if wlan.isconnected():
    print("Connected!")
    print("IP:", wlan.ifconfig()[0])
else:
    print("WiFi connection failed")

# ---------- WebREPL ----------
webrepl.start()