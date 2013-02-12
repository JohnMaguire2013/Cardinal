# Copyright (c) 2013 John Maguire <john@leftforliving.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.

import urllib2
from xml.dom import minidom

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?z=%s'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

class WeatherPlugin(object):
    def get_weather(self, cardinal, user, channel, msg):
        location = msg.split(' ', 1)[1]

        url = WEATHER_URL % urllib2.quote(location)
        dom = minidom.parse(urllib2.urlopen(url))

        try:
            ylocation = dom.getElementsByTagNameNS(WEATHER_NS, 'location')[0]
            yunits = dom.getElementsByTagNameNS(WEATHER_NS, 'units')[0]
            ywind = dom.getElementsByTagNameNS(WEATHER_NS, 'wind')[0]
            ycondition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]

            location_city = str(ylocation.getAttribute('city'))
            location_region = str(ylocation.getAttribute('region'))
            location_country = str(ylocation.getAttribute('country'))

            current_condition = str(ycondition.getAttribute('text'))
            current_temperature = str(ycondition.getAttribute('temp'))
            current_wind_speed = str(ywind.getAttribute('speed'))

            units_temperature = str(yunits.getAttribute('temperature'))
            units_speed = str(yunits.getAttribute('speed'))
            
            if units_temperature == "F":
                units_temperature2 = "C"
                current_temperature2 = str(int((float(current_temperature) - 32) * float(5)/float(9)))
            else:
                units_temperature2 = "F"
                current_temperature2 = str(int(float(current_temperature) * float(9)/float(5) + 32))

            location = location_city
            if location_region:
                location += ", " + location_region
            if location_country:
                location += ", " + location_country

            cardinal.sendMsg(channel, "[ %s | %s | Temp: %s %s (%s %s) | Winds: %s %s ]" % (location,
                                                                                    current_condition,
                                                                                    current_temperature, units_temperature,
                                                                                    current_temperature2, units_temperature2,
                                                                                    current_wind_speed, units_speed))
        except IndexError:
            cardinal.sendMsg(channel, "Sorry, couldn't find weather for \"%s\"." % location)

    get_weather.commands = ['weather', 'w']

def setup():
    return WeatherPlugin()
