import shutil, textwrap
from room import Room
from item_inventory import Item, Inventory
from input_parser import reformat, parse


# Print the given string to fit the terminal width (without line breaks in the
# middle of words)
def pretty_print(string):
    print(textwrap.fill(string, shutil.get_terminal_size().columns))


# Implements a text-based adventure game.
class Adventure():
    def __init__(self):
        self.world = {}                 # dictionary from room names to Room objects
        self.score = 0                  # player score
        self.current_room = "START"     # string of current room name
        self.rooms_visited = 1          # number of rooms visited by the player
        self.inventory = Inventory()    # player inventory
        self.quit = False               # game loop controller

    # Set up all rooms with descriptions, exits, and inventories
    def initialize_world(self):
        # Create Room object and add it to world dictionary
        self.world["START"] = Room(
            "You are at the north end of a hallway, in what looks like a school. Reinforced, unopenable doors block your way north, and there is a wall to the west. To the east is another room, possibly a classroom. To the south is more hallway, but an invisible wall blocks off that direction.",
            "You are at the north end of the hallway."
        )
        # Specify exits (other rooms that can be accessed from this room)
        self.world["START"].set_exits({"s": "NORTH POLE"})

        self.world["NORTH POLE"] = Room(
            "You are in a classroom, the North Pole. There are desks, and both the tables and the walls are whiteboards.",
            "You are in the North Pole."
        )
        self.world["NORTH POLE"].set_exits({"n": "START"})
        # Create Item object and add it to room's inventory
        self.world["NORTH POLE"].add_item(Item("coin",
            "The coin is golden and unusually ornate. It doesn't look like any currency you've ever seen."
        ))

    # Play the game by implementing user input loop
    def play(self):
        self.initialize_world()

        # Display initial messages
        print("-" * shutil.get_terminal_size().columns)
        self.display_current_room()
        self.world[self.current_room].visited = True

        # Main game loop
        while not self.quit:
            print()
            user_input = reformat(input(">> "))
            parse(user_input, self)

        # Display final messages
        self.display_farewell_message()

    # Look around at current room by printing long version of room description
    def look(self):
        self.display_current_room(True)

    # Examine something, if possible, by printing its description (all items in
    # the player's inventory should be examinable)
    def examine(self, command, phrase):
        if phrase == "":
            phrase = format(input(f"What would you like to {command}? "))

        # Check if item is in player's inventory or current room's inventory
        if self.inventory.has_item(phrase):
            pretty_print(self.inventory.get_item(phrase))
        elif self.world[self.current_room].has_item(phrase):
            pretty_print(f"You have to take the {phrase} before you can examine it.")
        else:
            pretty_print(f"There is no examinable {phrase} in this area.")

        # Redisplay room information
        self.display_current_room()

    # Move player in the given direction, if possible
    def move(self, direction):
        # Check if move is valid
        if direction in self.world[self.current_room].exits:
            # Update current room
            self.current_room = self.world[self.current_room].exits[direction]
            self.display_current_room()
            self.world[self.current_room].visited = True
            self.rooms_visited += 1

            # Bonus for visiting all rooms
            if self.rooms_visited == len(self.world):
                pretty_print("Congratulations! You get 10 points for visiting all the rooms!")
                self.score += 10
        else:
            pretty_print("You can't go that way.")
            self.display_current_room()

    # Take item by removing it from current room's inventory and adding it to
    # player's inventory, if possible
    def take(self, command, phrase):
        if phrase == "":
            phrase = reformat(input(f"What would you like to {command}? "))

        # Check if object is in current room's inventory
        if self.world[self.current_room].has_item(phrase):
            # Move object from room's inventory to player's inventory
            item = self.world[self.current_room].remove_item(phrase)
            self.inventory.add_item(item)
            pretty_print(f"You {command} the {phrase}.")

            # Bonus for collecting all items
            if self.inventory.has_item("coin"):
                pretty_print("Congratulations! You get 10 points for collecting all the items!")
                self.score += 10
        else:
            pretty_print(f"There is no {command}able {phrase} in this area.")

        # Redisplay room information
        self.display_current_room()

    # Drop item by removing it from player's inventory and adding it to current
    # room's inventory, if possible
    def drop(self, command, phrase):
        if phrase == "":
            phrase = reformat(input(f"What would you like to {command}? "))

        # Check if object is in player's inventory
        if self.inventory.has_item(phrase):
            # Move object from player's inventory to current room's inventory
            item = self.inventory.remove_item(phrase)
            self.world[self.current_room].add_item(item)
            pretty_print(f"You {command} the {phrase}.")

            if phrase == "coin" and self.current_room == "START":
                pretty_print("Congratulations! You get 30 points for returning the coin!")
                self.score += 30
                self.end_game()
                return
        else:
            pretty_print(f"You don't have a {phrase}.")

        # Redisplay room information
        self.display_current_room()

    # Quit the game by breaking the user input loop
    def end_game(self):
        self.quit = True

    # Respond to message if not understood
    def nonsense(self):
        pretty_print("I'm not sure what you mean.")

        # Redisplay room information
        self.display_current_room()

    # Prints out current room's long or short description, inventory, and exits
    def display_current_room(self, long_flag=False):
        if long_flag or not self.world[self.current_room].visited:
            pretty_print(self.world[self.current_room].long_description)
        else:
            pretty_print(self.world[self.current_room].short_description)

        self.world[self.current_room].display_inventory()
        self.world[self.current_room].display_exits()

    # Display player's current score
    def display_score(self):
        pretty_print(f"You currently have {score} points.")

        # Redisplay room information
        self.display_current_room()

    # Display player's inventory
    def display_inventory(self):
        if self.inventory.is_empty():
            pretty_print("Your backpack is empty.")
        else:
            pretty_print("Your backpack contains:")
            pretty_print(str(self.inventory))

        # Redisplay room information
        self.display_current_room()

    # Print score and thank you
    def display_farewell_message(self):
        pretty_print(f"You scored {self.score} points.")
        pretty_print("Thanks for playing!")
        print()


game = Adventure()
game.play()
