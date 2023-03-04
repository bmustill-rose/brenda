import board
import busio
from digitalio import DigitalInOut
import displayio
import simpleio

from adafruit_bitmap_font import bitmap_font
from adafruit_button import Button
import adafruit_requests as requests
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
import adafruit_touchscreen

import screensaver
from secrets import secrets

def play_sound_sequence(sequence):
 for note in sequence:
  simpleio.tone(board.A0, note[0], note[1])

def debounce(ts):
 while ts.touch_point:
  pass

print("booted")

font = bitmap_font.load_font('/fonts/Verdana-Bold-18.bdf')

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
print("Connecting to WiFi")
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)
print("Getting config and parsing JSON")
with wifi.get(f"{secrets['server_url']}/ui") as resp:
 ui_config = resp.json()
print("got JSON")

d = board.DISPLAY
ts = adafruit_touchscreen.Touchscreen(
 x1_pin = board.TOUCH_XL,
 x2_pin = board.TOUCH_XR,
 y1_pin = board.TOUCH_YD,
 y2_pin = board.TOUCH_YU,
 calibration=((5200, 59000), (5800, 57000)),
 size = (d.width, d.height),
 z_threshold = ui_config['display']['touch_threshold']
)

screensaver = screensaver.Screensaver(d, ui_config["display"]["active_brightness"], ui_config["display"]["dimmed_brightness"], ui_config["display"]["dimm_after"])
ui = displayio.Group()

color_bitmap = displayio.Bitmap(d.width, d.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = ui_config['background']['background_colour']
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
ui.append(background)
d.show(ui)

buttons = []
for b in ui_config['buttons']:
 buttons.append(Button(
  x = b['x'],
  y = b['y'],
  width = b['width'],
  height = b['height'],
  name = b['name'],
  style = Button.ROUNDRECT,
  label = b['label'],
  label_color = b['label_color'],
  label_font = font,
  fill_color = b['fill_color']
 ))

for b in buttons: ui.append(b)

print("Ready")
if 'startup_sound_sequence' in ui_config: play_sound_sequence(ui_config['startup_sound_sequence'])

while True:
 if screensaver.is_time_to_go_to_sleep(): screensaver.go_to_sleep()
 p = ts.touch_point
 if p:
  if screensaver.is_active:
   screensaver.wakeup()
   debounce(ts)
  else: #Don't handle the tap other than just waking up the screen
   screensaver.screen_was_touched()
   for b in buttons:
    if b.contains(p):
     b.selected = True
     try:
      if 'on_press_sound_sequence' in ui_config: play_sound_sequence(ui_config['on_press_sound_sequence'])
      with wifi.get(f"{secrets['server_url']}/cmd/{b.name}") as resp:
       print(f"{b.label}: {resp.text.rstrip()}")
      debounce(ts) #touch held within button
      b.selected = False
     except Exception as e:
      print("Failed to get data, retrying\n", e)
      wifi.reset()
      continue