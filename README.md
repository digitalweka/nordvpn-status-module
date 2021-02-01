# nordvpn-status-module

A module which toggles a VPN connection inside the bumblebee status bar. 

## Installation ##
Requires nordvpn-bin from the AUR. Add the vpn.py file to the bumblebee/modules directory and then modify i3/config appropriately.

## Usage ##
This module will connect the user to a random nordvpn server when clicked, or disconnect if already there is already a connection. The bar displays the location of the VPN server. Check that you are logged into nordvpn.
Any error given by nordvpn-bin will currently show up in the status bar as "No WIFI" due to sloppy handling (sorry). If this occurs, run nordvpn in the command line to view the error.
