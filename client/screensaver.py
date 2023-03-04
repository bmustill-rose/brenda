import time

class Screensaver:

 def __init__(self, display, active_brightness, dimmed_brightness, dimm_after):
  self.display = display
  self.active_brightness = active_brightness
  self.dimmed_brightness = dimmed_brightness
  self.dimm_after = dimm_after
  self.is_active = False
  self.time_since_last_touch = time.monotonic()

 def go_to_sleep(self):
  if not self.is_active: 
   print("sleeping")
   self.display.brightness = self.dimmed_brightness
   self.is_active = True

 def screen_was_touched(self):
  self.time_since_last_touch = time.monotonic()

 def wakeup(self):
  self.screen_was_touched()
  print("Woken up")
  self.display.brightness = self.active_brightness
  self.is_active = False

 def is_time_to_go_to_sleep(self):
  if time.monotonic() > self.time_since_last_touch+self.dimm_after:
   return True
  else:
   return False