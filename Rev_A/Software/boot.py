"""Expose a USB keyboard, plus the disk and serial console for maintenance."""
import usb_hid
import usb_midi

usb_midi.disable()
usb_hid.enable((usb_hid.Device.KEYBOARD,))
