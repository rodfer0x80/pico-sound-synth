import machine
import utime

def blink(led_pin):
    while True:
        led_pin.value(1)
        utime.sleep(3)
        led_pin.value(0)
        utime.sleep(3)
    return 0

def main():
    led_pin = machine.Pin(25, Pin.OUT)
    blink(led_pin)
    return 0

if __name__ == '__main__':
    main()
