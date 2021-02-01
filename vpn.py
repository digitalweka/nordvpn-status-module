#pylint: disable=C0111,R0903

"""Bumblebee status bar module for nordvpn by Stefan Dyer"""

import os
import subprocess
import re
import random

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                bumblebee.output.Widget(full_text=self.get_location)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self.toggle) #Mouse input

    def get_location(self, widgets):
        return self._location

    #Parses location list from nordvpn to python list
    def parse_locations(self, raw_list):
        raw_list = re.sub(r'(A\ ).+(cation.)', '', str(raw_list)) #Remove any update warnings
        raw_list = re.sub('\\\\.',' ',raw_list).replace('-',' ').replace(',','') #Remove escape characters
        raw_list = " ".join(raw_list.split())
        return list(raw_list.split(" ")[1:-1])

    #Choose a city to connect to
    def choose_city(self):
        countries = self.parse_locations(subprocess.check_output(["nordvpn", "countries"])) #Get all countries
        temp = subprocess.check_output(["nordvpn", "cities", random.choice(countries)]) #Get all cities in a country
        city = random.choice(self.parse_locations(temp)) #Pick one city
        return city

    #Toggle connection to VPN
    def toggle(self, widgets):
        status = subprocess.check_output(["nordvpn", "status"]) #Check if connected already
        status = self.parse_locations(status)
        if 'Disconnected' in status:
            city = self.choose_city() #Choose a random city to connect to
            subprocess.check_output(["nordvpn", "connect", city]) #Connect. Look at this line if you see JSON
        else:
            subprocess.check_output(["nordvpn", "disconnect"]) #Disconnect

    #Update the display text
    def update(self, widgets):
        try:
            self._location = self.current_location()
        except:
            self._location = " No WIFI "

    #Get current location
    def current_location(self):
        status = subprocess.check_output(["nordvpn", "status"])
        status = self.parse_locations(status)
        if 'Disconnected' in status:
            return "VPN: Disconnected "
        else:
            city_loc = status.index("City:") #Position of city name will always be after "City:" string.
            country_loc = status.index("Country:")
            doubles = ["New", "United", "South", "Costa", "Czech", "North"] #Countries with two word names
            if status[country_loc + 1] in doubles:
                return "VPN: " + status[city_loc + 1] + ", " + status[country_loc + 1] + " " + status[country_loc + 2] + " "
            else:
                return "VPN: " + status[city_loc + 1] + ", " + status[country_loc + 1] + " "
