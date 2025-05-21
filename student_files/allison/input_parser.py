# Formats input string by removing articles.
def reformat(string):
    string = string.strip().lower()

    while string.find("  ") >= 0:
        string = string.replace("  ", " ")

    for a in ["the", "a", "an", "this", "that"]:
        string = string.replace(" " + a + " ", " ")

    return string


# Parses input string and calls corresponding methods in Adventure.
def parse(string, adv):
    if (i := string.find(" ")) >= 0:
        command = string[:i]
        phrase = string[(i + 1):]
    else:
        command = string
        phrase = ""

    # Quit
    if command in ["q", "quit"]:
        adv.end_game()

    # Look
    elif command in ["l", "look"]:
        adv.look()

    # Check inventory
    elif command in ["i", "inv", "inventory"]:
        adv.display_inventory()

    # Check score
    elif command in ["score"]:
        adv.display_score()

    # Move
    elif command in ["n", "north", "e", "east", "s", "south", "w", "west"] and phrase == "":
        adv.move(command[0])

    elif command in ["move", "go", "run", "walk", "march"]:
        if phrase == "":
            phrase = format(input(f"Where would you like to {command}? "))

        if phrase in ["n", "north", "e", "east", "s", "south", "w", "west"]:
            adv.move(phrase[0])
        else:
            print("What?")

    # Add to inventory
    elif command in ["take", "get", "grab", "pick", "acquire"]:
        if command == "pick" and phrase[:3] == "up ":
            adv.take(command + phrase[:3], phrase[3:])
        else:
            adv.take(command, phrase)

    # Remove from inventory
    elif command in ["drop", "release"]:
        adv.drop(command, phrase)

    # Examine
    elif command == "examine":
        adv.examine(command, phrase)

    # None
    else:
        adv.nonsense()
