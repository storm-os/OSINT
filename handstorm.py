import trio
import sys

from storm.core import storm_entry

class StormOSModuleRunner:
    """
    This class can only be run on Storm Framework
    """
    def __init__(self):
        self.email = None

    def set_options(self, mail):
        self.email = mail
        
    def run_module(self):
        """
        This logic relates to Storm Framework commands and inputs.
        """
        try:
            raw_data = trio.run(storm_entry, self.email)
            self.data_count(raw_data)
        except Exception as e:
            print(f"[!] ERROR: {e}")

    def data_count(self, data):
        """Logic for calculating how many results are found"""
        detected_count = len([x for x in data if x['exists']])
        print(f"[*] Synchronization: {detected_count}.")
        pass

