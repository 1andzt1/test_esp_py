from machine import Pin, PWM, I2C
import uasyncio as asyncio
from lib import ssd1306

# ---------- LED ----------
led = PWM(Pin(2), freq=1000)

# ---------- I2C OLED ----------
i2c = I2C(0, scl=Pin(27), sda=Pin(26))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- асинхронна задача LED ----------
async def breathe_led():
    duty_history = []  # список останніх значень duty для прокрутки
    max_lines = 7      # 7 рядків для history, перший рядок зайнятий "LED Duty:"
    
    while True:
        # цикл збільшення і зменшення яскравості
        for duty in list(range(0, 1024, 8)) + list(range(1023, -1, -8)):
            led.duty(duty)
            
            # додати поточне значення в історію
            duty_history.append(duty)
            if len(duty_history) > max_lines:
                duty_history.pop(0)  # видаляємо найстаріше

            # малюємо на OLED
            oled.fill(0)
            oled.text("LED Duty:", 0, 0)  # завжди верхній рядок

            # відображаємо історію нижче
            for i, val in enumerate(duty_history):
                oled.text(str(val), 0, 8*(i+1))
            
            oled.show()
            await asyncio.sleep_ms(10)

# ---------- головний цикл ----------
async def main():
    asyncio.create_task(breathe_led())
    while True:
        await asyncio.sleep(1)

# ---------- старт ----------
asyncio.run(main())