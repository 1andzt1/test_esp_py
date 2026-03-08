print("--Start main.py--")
from machine import I2C, Pin, PWM
import network
import time
from lib.bme280_int import BME280
import ssd1306
from requests import get


# ---------- Wi-Fi конфіг ----------
LOGIN_WiFi = {
    "ZYTOBLENERGO": "zhuiko12sdtu",
    "MyWiFi24": "LogiUser0",
    }
print(LOGIN_WiFi)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ---------- Підключення до Wi-Fi ----------
def connect_wifi(ssid, password, timeout=10):
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    print("Connecting to:", ssid)
    wlan.connect(ssid, password)

for key_ssid, key_password in LOGIN_WiFi.items():
    connect_wifi(key_ssid, key_password)
    time.sleep(3)
    if wlan.isconnected:
        print("Connected to:", key_ssid)
        break
    else:
        print("Failed to connect to Wi-Fi:", key_ssid)


# ---------- I2C ----------
i2c = I2C(0, scl=Pin(27), sda=Pin(26))

# ---------- OLED ----------
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- LED ----------
led = PWM(Pin(2))
led.freq(1000)


def get_Local_ip():
    if wlan.isconnected():
        return "L:{}".format(wlan.ifconfig()[0])
    else:
        return "L:not connection"

def get_Global_ip():
    if wlan.isconnected():
        ip = get('https://api.ipify.org').content.decode('utf8')
        return "G:{}".format(ip)

# ---------- BME280 ----------
try:
    bme = BME280(i2c=i2c)
    sensor_ok = True
except Exception as e:
    sensor_ok = False
    sensor_error = str(e)

# ---------- LED breathing ----------
duty = 0
step = 5000 # крок для 16-bit

# ---------- MAIN LOOP ----------
while True:

    # LED breathing
    duty += step
    if duty >= 65535 or duty <= 0:
        step = -step

    # обмеження діапазону
    if duty < 0:
        duty = 0
    if duty > 65535:
        duty = 65535

    led.duty_u16(duty)


    oled.fill(0)

    # --- IP рядок ---

    oled.text(get_Local_ip(), 0, 0)
    oled.text(get_Global_ip(), 0, 9)

    # --- BME280 ---
    if sensor_ok:
        try:
            temp, press, hum = bme.read_compensated_data()

            temp = temp / 100        # °C
            press = press / 25600    # hPa
            hum = hum / 1024         # %

            oled.text("T: {:.1f} C".format(temp), 0, 38)

            oled.text("P: {:.1f} hPa".format(press), 0, 47)
            oled.text("H: {:.1f} %".format(hum), 0, 56)

        except Exception as e:
            oled.text("Sensor read err", 0, 24)

    else:
        oled.text("Sensor init err", 0, 24)

    oled.show()
    time.sleep(0.2)