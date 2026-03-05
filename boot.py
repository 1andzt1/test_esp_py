import network
import time
import webrepl


# ---------- Wi-Fi конфіг ----------
PRIMARY_SSID = "ZYTOBLENERGO"
PRIMARY_PASSWORD = "zhuiko12sdtu"

SECONDARY_SSID = "MyWiFi24"
SECONDARY_PASSWORD = "LogiUser0"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ---------- Підключення до Wi-Fi ----------
def connect_wifi(ssid, password, timeout=10):
    print("Connecting to:", ssid)

    # якщо вже підключений — роз'єднати
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    wlan.connect(ssid, password)

    while timeout > 0:
        if wlan.isconnected():
            print("Connected:", wlan.ifconfig()[0])
            return True
        else:
            time.sleep(1)
            timeout -= 1

        print(f"Not connected: {PRIMARY_SSID} and {SECONDARY_SSID}")
        return False





if not connect_wifi(PRIMARY_SSID, PRIMARY_PASSWORD):
    print("Primary failed, trying backup...")

    # пробуємо додаткову wifi
    connect_wifi(SECONDARY_SSID, SECONDARY_PASSWORD)



# ---------- Запуск WebREPL ----------
try:
    webrepl.start()
except Exception as e:
    print("WebREPL error:", e)