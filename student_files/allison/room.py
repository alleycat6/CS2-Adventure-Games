import os, textwrap
from item_inventory import Inventory


# Print the given string to fit the terminal width (without line breaks in the
# middle of words)
def pretty_print(string):
    print(textwrap.fill(string, os.get_terminal_size().columns))


# Implements a room in the game, with descriptions, possible exits, and an
# inventory.
class Room():
    # Class variable for formatting directions when printed
    directions_dict = {"n": "North", "e": "East", "s": "South", "w": "West"}

    def __init__(self, l="", s=""):
        self.long_description = l       # string of long room description
        self.short_description = s      # string of short room description
        self.visited = False            # whether room has been visited by the player yet
        self.exits = {}                 # dictionary from directions to other room names
                                        #     example: {"n": "ROOM1", "e": "ROOM2"}
        self.inventory = Inventory()    # room inventory

    # Update exits with given dictionary
    def set_exits(self, new_exits):
        self.exits.update(new_exits)

    # Inventory methods shortcut
    def has_item(self, item_name): return self.inventory.has_item(item_name)
    def get_item(self, item_name): return self.inventory.get_item(item_name)
    def add_item(self, item): return self.inventory.add_item(item)
    def remove_item(self, item_name): return self.inventory.remove_item(item_name)

    # Print out possible exit directions
    def display_exits(self):
        # Check if there are any exits
        if len(self.exits) > 0:
            pretty_print("From here you can go:")
            pretty_print(" ".join(sorted(map(Room.directions_dict.get, self.exits.keys()))))
        else:
            pretty_print("You cannot go anywhere from here. There are no available exits.")

    # Print out inventory
    def display_inventory(self):
        if not self.inventory.is_empty():
            pretty_print("The following items are on the floor:")
            pretty_print(str(self.inventory))
