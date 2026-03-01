from machine import Pin, PWM, I2C
import uasyncio as asyncio

# LED на GPIO2
led = PWM(Pin(2), freq=1000)

# ---------- I2C OLED ----------
i2c = I2C(0, scl=Pin(27), sda=Pin(26))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

async def breathe_led():
    while True:
        # Збільшуємо яскравість
        for duty in range(0, 1024, 8):
            led.duty(duty)
            await asyncio.sleep_ms(10)
        # Зменшуємо яскравість
        for duty in range(1023, -1, -8):
            led.duty(duty)
            await asyncio.sleep_ms(10)

# Запускаємо асинхронно
async def main():
    asyncio.create_task(breathe_led())
    while True:
        await asyncio.sleep(1)  # тримаємо цикл живим

asyncio.run(main())