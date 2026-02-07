import trio
import sys

from holehe.core import storm_entry

class StormOSModuleRunner:
    """
    This class can only be run on Storm Framework
    """
    def __init__(self):
        self.options = {
            "EMAIL": {
                "value": "",
                "required": True,
                "description": "Register"
            }
        }

    def run_module(self):
        """This logic relates to Storm Framework commands and inputs."""
        email = self.options['EMAIL']['value']

        try:
            raw_data = trio.run(storm_entry, email)
            self.data_count(raw_data)
        except Exception as e:
            print(f"[!] ERROR: {e}")

    def data_count(self, data):
        """Logic for calculating how many results are found"""
        detected_count = len([x for x in data if x['exists']])
        print(f"[*] Synchronization: {detected_count}.")
        pass

