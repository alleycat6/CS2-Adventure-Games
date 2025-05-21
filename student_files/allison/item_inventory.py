# Implements an item in the game that is not part of a Room object.
class Item():
    def __init__(self, n, d):
        self.name = n           # string of item name
        self.description = d    # string of item description

    def __str__(self):
        return self.description


# Implements a collection of Item objects.
class Inventory():
    def __init__(self):
        self.items = {}    # dictionary from item names to Item objects

    def __str__(self):
        return "\n".join(self.items.keys())

    # Check whether inventory is empty
    def is_empty(self):
        return len(self.items) == 0

    # Check whether inventory has item
    def has_item(self, item_name):
        return item_name in self.items

    # Return inventory item object, if possible
    def get_item(self, item_name):
        return self.items.get(item_name)

    # Add item to inventory
    def add_item(self, item):
        self.items[item.name] = item

    # Remove and return item from inventory, if possible
    def remove_item(self, item_name):
        return self.items.pop(item_name, None)
