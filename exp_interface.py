from exp_error import *
from exp_info import *

def interface_init():
    global interface
    interface = {}

def entry_exists(id):
    return id in interface

def get_entry(id):
    if not entry_exists(id):
        err = Exception(f"InterfaceEntry '{id}' does not exist.")
        raise err
    return interface[id]

class InterfaceEntry:
    def __new__(cls, id):
        if cls == InterfaceEntry:
            err = Exception(f"Cannot create InterfaceEntry '{id}'. Needs to be an instance of a class inheriting from InterfaceEntry.")
            raise err
        try: interface
        except NameError: interface_init()
        if id in interface: return interface[id]
        new_entry = super().__new__(cls)
        new_entry.id = id
        interface[id] = new_entry
        new_entry.exists = False
        return new_entry

    def __init__(self, id=None):
        if self.exists: return
        self.exists = True