from raspledstrip.ledstrip import *
from raspledstrip.animation import *
from raspledstrip.color import Color
import os
import requests
import json
import time
import traceback


# Things that should be configurable
ledCount = 32 * 5
api = 'http://lumiere.meteor.com/'
waitTime = 6

class Lumiere:
  """
  Class to handle getting light information.
  """

  def __init__(self):
    """
    Constructor.  Read settings if there.
    """
    settings_file = 'settings.json';
    self.settings = {};
    if (os.path.isfile(settings_file)):
      self.settings = json.loads(open(settings_file).read())

    self.lights = self.settings['lights'] if 'lights' in self.settings else 160
    self.api = self.settings['api'] if 'api' in self.settings else 'http://lumiere.lighting'
    self.poll_interval = self.settings['poll_interval'] if 'poll_interval' in self.settings else 6

    self.current_id = None
    self.light_array = []
    self.led = LEDStrip(self.lights)
    self.led.all_off()


  def listen(self):
    """
    Handles the continual checking.
    """
    while True:
      try:
        self.query_lumiere()
        time.sleep(self.poll_interval)
      except (KeyboardInterrupt, SystemExit):
        raise
      except:
        print traceback.format_exc()


  def set_lights(self):
    """
    Change the lights.
    """
    self.fill_lights()

    # Animate
    anim = FireFlies(self.led, self.light_array, 1, 1, 0, self.led.lastIndex)
    for i in range(50):
      anim.step()
      self.led.update()

    # Final fill
    for li, l in enumerate(self.light_array):
      self.led.set(li, l)
    self.led.update()


  def fill_lights(self):
    """
    Fill up LED count with all the colors.
    """
    self.light_array = []
    light_array = []
    length = len(self.current['colors'])

    for x in range(0, self.lights - 1):
      light_array.append(self.hex_to_rgb(self.current['colors'][x % length]))

    for li, l in enumerate(light_array):
      self.light_array.append(Color(l[0], l[1], l[2]))


  def query_lumiere(self):
    """
    Make request to API.
    """
    r = requests.get('%s/api/colors' % (self.api))
    if r.status_code == requests.codes.ok:
      self.current = r.json()

      # Only update if new record
      if self.current_id is None or self.current_id != self.current['_id']:
        self.current_id = self.current['_id']
        self.set_lights()


  def hex_to_rgb(self, value):
    """
    Turns hex value to RGB tuple.
    """
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))


if __name__ == '__main__':
  lumiere = Lumiere()
  lumiere.listen()
