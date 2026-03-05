import time

LOGIN_WiFi = {
    "ZYTOBLENERGO": "zhuiko12sdtu",
    "MyWiFi24": "LogiUser0",
    }

print (len(LOGIN_WiFi))

for key_ssid, key_password in LOGIN_WiFi.items():
    print(key_ssid, key_password)