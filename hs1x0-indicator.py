#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Small Gtk Indicator Applet wrapping pyHS100 for use with TP-Link HS100/HS110
Uses a modified/fixed version of pyHS100:
     <https://github.com/GadgetReactor/pyHS100>

Copyright (c) 2016 moqui

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
__author__ = "moqui"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "github@moqui.me"

import os
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from pyHS100.pyHS100 import SmartPlug
from gi.repository import Gtk, GLib, AppIndicator3

currentpath = os.path.dirname(os.path.realpath(__file__))

### Config
actorname = "TP-Link HS100" # Actor name to show in indicator
showactorname = True # Show name in indicator (True|False)
actorip = "192.168.0.100" # IP addresse of indicator
### Config

def switch_actor_on(self, indicator, actor):
    actor.state = "ON"
    update_indicator(indicator, actor)
    return True


def switch_actor_off(self, indicator, actor):
    actor.state = "OFF"
    update_indicator(indicator, actor)
    return True


def update_indicator(indicator, actor):
    state = actor.state
    if state == 'ON':
        indicator.set_icon(currentpath+"/on.svg")
    elif state == 'OFF':
        indicator.set_icon(currentpath+"/off.svg")
    else:
        indicator.set_icon(currentpath+"/error.svg")
    return True


def main():
        # Build application indicator
        indicator = AppIndicator3.Indicator.new_with_path (
        "hs1x0-indicator",
        currentpath+"/error.svg",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        currentpath
        )

        actor = SmartPlug(actorip)

        # build exit menu item
        menu_item_exit = Gtk.MenuItem("_Exit")
        menu_item_exit.set_use_underline(True)
        menu_item_exit.connect("activate", lambda w: Gtk.main_quit())
        menu_item_exit.show()

        # build on menu item
        menu_item_on = Gtk.MenuItem("_On")
        menu_item_on.set_use_underline(True)
        menu_item_on.connect("activate", switch_actor_on, indicator, actor)
        menu_item_on.show()

        # build off menu item
        menu_item_off = Gtk.MenuItem("O_ff")
        menu_item_off.set_use_underline(True)
        menu_item_off.connect("activate", switch_actor_off, indicator, actor)
        menu_item_off.show()

        # build small menu
        menu = Gtk.Menu()
        menu.append(menu_item_on)
        menu.append(menu_item_off)
        menu.append(menu_item_exit)
        indicator.set_menu(menu)
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        indicator.set_icon(currentpath+"/error.svg")
        if showactorname:
            indicator.set_label(actorname,actorname+" ")

        # Update all 1000ms
        GLib.timeout_add(1000, update_indicator, indicator, actor)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()
        return True


if __name__ == "__main__":
    main()
