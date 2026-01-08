#!/usr/bin/env python3
"""
Raspberry Pi 5 GPIO制御の基本例
LEDの点滅プログラム
"""

from gpiozero import LED
from time import sleep

# GPIO17にLEDを接続
led = LED(17)

def blink_led(times=5, interval=1.0):
    """
    LEDを点滅させる

    Args:
        times: 点滅回数
        interval: 点滅間隔（秒）
    """
    print(f"LED点滅を開始します（{times}回）")

    for i in range(times):
        led.on()
        print(f"LED ON ({i+1}/{times})")
        sleep(interval)

        led.off()
        print(f"LED OFF ({i+1}/{times})")
        sleep(interval)

    print("LED点滅が完了しました")

if __name__ == "__main__":
    try:
        blink_led()
    except KeyboardInterrupt:
        print("\n中断されました")
    finally:
        led.close()
        print("GPIOをクリーンアップしました")
