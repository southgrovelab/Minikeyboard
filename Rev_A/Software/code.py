import time
import board
import digitalio
import keypad
import usb_hid

# GPIO, modifierare, tangentkod
# Modifierare 0x05 = vänster Ctrl + vänster Alt
BUTTONS = (
    (board.GP2, 0x00, 0x29),  # Esc
    (board.GP4, 0x00, 0x2B),  # Tab
    (board.GP6, 0x00, 0x28),  # Enter
    (board.GP8, 0x05, 0x4C),  # Ctrl + Alt + Delete
)

keyboard = next(
    device for device in usb_hid.devices
    if device.usage_page == 0x01 and device.usage == 0x06
)

released = bytes(8)
report = bytearray(8)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Knappar mellan respektive GPIO och GND.
# Interna pull-up-motstånd och filtrering av kontaktstudsar.
keys = keypad.Keys(
    tuple(button[0] for button in BUTTONS),
    value_when_pressed=False,
    pull=True,
    interval=0.005,
    debounce_threshold=5,
)

time.sleep(1)
keyboard.send_report(released)
keys.events.clear()
led.value = True

try:
    while True:
        event = keys.events.get()

        if event is not None and event.pressed:
            _, modifiers, keycode = BUTTONS[event.key_number]
            report[0] = modifiers
            report[2] = keycode

            try:
                # Modifierare och tangent skickas tillsammans.
                keyboard.send_report(report)
                time.sleep(0.02)
            finally:
                # Släpp alla tangenter, inklusive Ctrl och Alt.
                keyboard.send_report(released)

        time.sleep(0.001)

finally:
    keyboard.send_report(released)
    keys.deinit()
    led.value = False
