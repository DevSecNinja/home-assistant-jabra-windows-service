import time
import random
import requests
import json
import configparser
import glob
import sys
import os

from pathlib import Path
from SMWinservice import SMWinservice
from requests import post
from time import sleep
from msvcrt import kbhit

import pywinusb.hid as hid

class PythonCornerExample(SMWinservice):
    _svc_name_ = "JabraHomeAssistantSync"
    _svc_display_name_ = "Jabra Home Assistant Sync"
    _svc_description_ = "This service syncs the Jabra hook status to Home Assistant"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            # Browse for non system HID class devices, if a telephony page
            # hook usage control is available monitor value change events
            # play with this value (or set it if you know your device capabilities)
            # this allows to poll the telephony device for the current usage value
            input_interrupt_transfers = False

            # get all currently connected HID devices we could filter by doing
            # something like hid.HidDeviceFilter(vendor_id = 0x1234), product Id
            # filters (with masks) and other capabilities also available
            all_devices = hid.HidDeviceFilter(vendor_id = 0x0b0e).get_devices() # Vendor_id 0x0b0e = Jabra

            if not all_devices:
                # add a delay of 0.5 seconds for resource utilization
                sleep(0.5)

                print("No HID class devices attached.")
            else:
                # search for our target usage (the hook button)
                #target pageId, usageId
                usage_telephony_hook = hid.get_full_usage_id(0xb, 0x20)

                def hook_pressed(new_value, event_type):
                    "simple usage control handler"
                    # this simple handler is called on 'pressed' events
                    # this means the usage value has changed from '1' to '0'
                    # no need to check the value
                    event_type = event_type #avoid pylint warnings
                    
                    # import the config file
                    config = configparser.ConfigParser()
                    config.read(os.path.join(sys.path[0], "secrets.ini"))

                    if new_value:
                        print("On Hook!")
                        response = requests.post(
                                config.get('DEFAULT', 'HomeAssistantURL'),
                                headers={'Authorization': config.get('DEFAULT', 'HomeAssistantAuth'), 'content-type': 'application/json'},
                                data=json.dumps({'state': 'on', 'attributes': {'friendly_name': 'Jabra Headset','icon': 'mdi:headset'}}))
                        print(response.text)
                    else:
                        print("Off Hook!")
                        response = requests.post(
                                config.get('DEFAULT', 'HomeAssistantURL'),
                                headers={'Authorization': config.get('DEFAULT', 'HomeAssistantAuth'), 'content-type': 'application/json'},
                                data=json.dumps({'state': 'off', 'attributes': {'friendly_name': 'Jabra Headset','icon': 'mdi:headset'}}))
                        print(response.text)

                for device in all_devices:
                    try:
                        device.open()

                        # browse input reports
                        all_input_reports = device.find_input_reports()

                        for input_report in all_input_reports:
                            if usage_telephony_hook in input_report:
                                #found a telephony device w/ hook button
                                print("\nMonitoring {0.vendor_name} {0.product_name} "\
                                        "device.\n".format(device))

                                # add event handler (example of other available
                                # events: EVT_PRESSED, EVT_RELEASED, EVT_ALL, ...)
                                device.add_event_handler(usage_telephony_hook,
                                    hook_pressed, hid.HID_EVT_CHANGED) #level usage

                                if input_interrupt_transfers:
                                    # poll the current value (GET_REPORT directive),
                                    # allow handler to process result
                                    input_report.get()

                                while not kbhit() and device.is_plugged() and self.isrunning:
                                    #just keep the device opened to receive events
                                    sleep(0.5)
                                # return - Uncomment if you want the service to stop
                    finally:
                        device.close()
                print("Sorry, no one of the attached HID class devices "\
                    "provide any Telephony Hook button")

if __name__ == '__main__':
    PythonCornerExample.parse_command_line()