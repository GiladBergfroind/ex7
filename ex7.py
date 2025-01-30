import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def print_pokemon(pokemon):
    print(f'ID: {pokemon.get("ID")}, Name: {pokemon.get("Name")}, Type: {pokemon.get("Type")}, '
          f'HP: {pokemon.get("HP")}, Attack: {pokemon.get("Attack")}, Can Evolve: {pokemon.get("Can Evolve")}')

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    isValid = 1
    while isValid:
        x = input(f"{prompt}")
        if x.isdigit():
            x = int(x)
            isValid = 0
        elif len(x) >1 and x[0] == '-' and x[1:].isdigit():
            x = int(x)
            return x
        else:
            print("Invalid input")
    return int(x)

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    return HOENN_DATA[poke_id-1]

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    i = 0
    name = name.lower()
    currentName = HOENN_DATA[0].get("Name").lower()
    for i in range (135):
        if currentName != name:
            currentName = HOENN_DATA[i].get("Name").lower()
        else:
            return HOENN_DATA[i]
    return None

def print_owner(pokeList):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    numOfPokemons = len(pokeList)
    for i in range(numOfPokemons):
        print_pokemon(pokeList[i])
    return



########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    owner_node = {"owner": owner_name,"pokedex": [first_pokemon], "left": None, "right": None}
    return owner_node

def insert_owner_bst(root, newNode):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    currentName = root.get("owner")
    newName = newNode.get("owner")
    currentName =currentName.lower()
    newName = newName.lower()
    if (newName < currentName):
        if (root.get("left")):
            return insert_owner_bst(root.get("left"),newNode)
        root.update({"left": newNode})
        if (root.get("left") == None):
            print("Insertion failed.\n")
            return False
        else:
            return True
    if (newName > currentName):
        if (root.get("right")):
            return insert_owner_bst(root.get("right"),newNode)
        root.update({"right": newNode})
        if (root.get("right") == None):
            print("Insertion failed.\n")
            return False
        else:
            return True
    return False

def find_owner_bst(root, ownerName):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    currentName = root.get("owner")
    newName = ownerName
    currentName = currentName.lower()
    newName = newName.lower()
    if (newName == currentName):
        return root
    if (newName < currentName):
        if (root.get("left")):
            return find_owner_bst(root.get("left"), ownerName)
    if (newName > currentName):
        if (root.get("right")):
            return find_owner_bst(root.get("right"), ownerName)
    return None

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    while node["left"]:
        node = node["left"]
    return node


def delete_owner_bst(root, ownerName):
    """
    Remove a node from the BST by ownerName. Return the updated root.
    """
    if root is None:
        return None  # Base case: Tree is empty

    ownerName = ownerName.lower()  # Convert input to lowercase
    currentName = root["owner"].lower()  # Convert stored owner name to lowercase

    if ownerName < currentName:
        root["left"] = delete_owner_bst(root["left"], ownerName)  # Recur on the left subtree
    elif ownerName > currentName:
        root["right"] = delete_owner_bst(root["right"], ownerName)  # Recur on the right subtree
    else:
        # Node found: Handle the deletion cases

        # Case 1: No children
        if root["left"] is None and root["right"] is None:
            return None

        # Case 2: Only right child
        if root["left"] is None:
            return root["right"]

        # Case 3: Only left child
        if root["right"] is None:
            return root["left"]

        # Case 4: Node has two children
        successor = min_node(root["right"])  # Find the smallest node in the right subtree
        root["owner"] = successor["owner"]  # Copy successor's data
        root["right"] = delete_owner_bst(root["right"], successor["owner"])  # Delete the successor

    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root,numOfOwners):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    queue = []
    rootNum = 0
    queue.append(root)
    for i in range(numOfOwners):
        counter = 0
        if queue[rootNum].get("left") != None:
            queue.append(queue[rootNum].get("left"))
            counter += 1
        if queue[rootNum].get("right") != None:
            queue.append(queue[rootNum].get("right"))
            counter += 1
        rootNum += counter
    for j in range(numOfOwners):
        pokedex = queue[j].get("pokedex")
        print(f'Owner: {queue[j].get("owner")}')
        print_owner(pokedex)

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(ownerNode,newPokemon):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    newPokedex = ownerNode.get("pokedex")
    newPokedex.append(newPokemon)
    ownerNode.update({"pokedex": newPokedex})
    return  ownerNode

def release_pokemon_by_name(ownerNode):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    numOfPokemons = len(ownerNode.get("pokedex"))
    nameToDelete = input("Enter Pokemon Name to release: ").lower()
    i = 0
    for i in range(numOfPokemons):
        currentName = ownerNode.get("pokedex")[i].get("Name").lower()
        if nameToDelete == currentName:
            print(f'Releasing {ownerNode.get("pokedex")[i].get("Name")} from {ownerNode.get("owner")}.')
            ownerNode.get("pokedex").remove(ownerNode.get("pokedex")[i])
            return
    print(f"No Pokemon named '{nameToDelete}' in {ownerNode['owner']}\'s Pokedex.")
    return
def evolve_pokemon_by_name(ownerNode):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    pokedex = ownerNode.get("pokedex")
    oldPokemonName = input("Enter Pokemon Name to evolve: ").lower()
    oldPokemon = get_poke_dict_by_name(oldPokemonName)
    if oldPokemon is None:
        print(f"No Pokemon named '{oldPokemonName}' in {ownerNode.get('owner')}'s Pokedex.")
        return
    if oldPokemon.get("Can Evolve") == "FALSE":
        print(f"{oldPokemonName} cannot evolve.")
        return
    newPokemonId = oldPokemon.get("ID") + 1
    numOfPokemons = len(pokedex)
    i = 0
    for i in range(numOfPokemons):
        if oldPokemonName != pokedex[i].get("Name"):
            i += 1
        else:
            break
    if i == numOfPokemons:
        i = 0
    for i in range(numOfPokemons):
        newPokemon = pokedex[i]
        if newPokemonId == newPokemon.get("ID"):
            print(f"Pokemon evolved from {oldPokemonName} (ID {oldPokemon.get('ID')}) to"
                  f" {newPokemon.get('Name')} (ID {newPokemonId})."
                  f"\n {newPokemon.get('Name')} was already present; releasing it immediately.")
    newPokemon = get_poke_dict_by_id(newPokemonId)
    pokedex.remove(pokedex[i])
    pokedex.append(newPokemon)

########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sort_owners_by_num_pokemon(root,numOfOwners):
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    if numOfOwners == 0:
        print("No owners at all")
        return
    print("=== The Owners we have, sorted by number of Pokemons ===")
    queue = []
    rootNum = 0
    queue.append(root)
    for i in range(numOfOwners):
        counter = 0
        if queue[rootNum].get("left") != None:
            queue.append(queue[rootNum].get("left"))
            counter += 1
        if queue[rootNum].get("right") != None:
            queue.append(queue[rootNum].get("right"))
            counter += 1
        rootNum += counter
    for i in range(numOfOwners):
        for j in range(numOfOwners-1):
            if len(queue[j].get("pokedex")) > len(queue[j+1].get("pokedex")):
                queue[j],queue[j+1] = queue[j+1],queue[j]
            elif (len(queue[j].get("pokedex")) == len(queue[j+1].get("pokedex"))
                  and queue[j].get("owner") > queue[j+1].get("owner")):
                queue[j], queue[j + 1] = queue[j + 1], queue[j]
    for h in range(numOfOwners):
        length = len(queue[h].get("pokedex"))
        print(f"Owner: {queue[h].get('owner')} (has {length} Pokemon)")
    return
########################
# 6) Print All
########################

def print_all_owners(ownerRoot,numOfOwners):
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    if numOfOwners == 0:
        print("No owners at all")
        return
    print("1) BFS\n2) Pre-Order\n3) In-Order\n4) Post-Order")
    choice = read_int_safe("Your choice:\n")
    if choice == 1:
        bfs_traversal(ownerRoot,numOfOwners)
    elif choice == 2:
        pre_order_print(ownerRoot)
    elif choice == 3:
        in_order_print(ownerRoot)
    elif choice == 4:
        post_order_print(ownerRoot)
    else:
        print("Invalid choice")
def pre_order_print(root):
    """
    Helper to print data in pre-order.
    """
    if root is None:
        return
    pokedex = root.get("pokedex")
    print(f"Owner: {root.get('owner')}")
    print_owner(pokedex)
    pre_order_print(root.get("left"))
    pre_order_print(root.get("right"))

def in_order_print(root):
    """
    Helper to print data in in-order.
    """
    if root is None:
        return
    pre_order_print(root.get("left"))
    pokedex = root.get("pokedex")
    print(f"Owner: {root.get('owner')}")
    print_owner(pokedex)
    pre_order_print(root.get("right"))

def post_order_print(root):
    """
    Helper to print data in post-order.
    """

    if root is None:
        return
    pre_order_print(root.get("left"))
    pre_order_print(root.get("right"))
    pokedex = root.get("pokedex")
    print(f"Owner: {root.get('owner')}")
    print_owner(pokedex)



########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(ownerNode):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    choice = 1
    i = 0
    numOfPokemons = len(ownerNode.get("pokedex"))
    if numOfPokemons == 0:
        currentPokemon = None
    else:
        currentPokemon = ownerNode.get("pokedex")[0]
    while choice != 7:
        printcounter = 0
        print("\n-- Display Filter Menu --\n1. Only a certain Type\n2. Only Evolvable\n3. Only Attack above __\n"
        "4. Only HP above __\n5. Only names starting with letter(s)\n6. All of them!\n7. Back")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            if numOfPokemons != 0:
                wantedType = input("Which Type? (e.g. GRASS, WATER): ")
                wantedType = wantedType.lower()
                for i in range (numOfPokemons):
                    currentPokemon = ownerNode.get("pokedex")[i]
                    currentType = currentPokemon.get("Type")
                    currentType = currentType.lower()
                    if currentType == wantedType:
                        print_pokemon(currentPokemon)
                        printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 2:
            for i in range(numOfPokemons):
                if numOfPokemons != 0:
                    currentPokemon = ownerNode.get("pokedex")[i]
                    if currentPokemon.get("Can Evolve") == "TRUE":
                        print_pokemon(currentPokemon)
                        printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 3:
            requiredAttack = read_int_safe("Enter Attack threshold: ")
            for i in range(numOfPokemons):
                if numOfPokemons != 0:
                    currentPokemon = ownerNode.get("pokedex")[i]
                    if currentPokemon.get("Attack") > requiredAttack:
                        print_pokemon(currentPokemon)
                        printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 4:
            requiredHP = read_int_safe("Enter HP threshold: ")
            for i in range(numOfPokemons):
                if numOfPokemons != 0:
                    currentPokemon = ownerNode.get("pokedex")[i]
                    if currentPokemon.get("HP") > requiredHP:
                        print_pokemon(currentPokemon)
                        printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 5:
            startingLetters = input("Starting letter(s): ")
            for i in range(numOfPokemons):
                if numOfPokemons != 0:
                    currentPokemon = ownerNode.get("pokedex")[i]
                    currentName = currentPokemon.get("Name").lower()
                    if currentName.startswith(startingLetters):
                        print_pokemon(currentPokemon)
                        printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 6:
            for i in range(numOfPokemons):
                if numOfPokemons != 0:
                    currentPokemon = ownerNode.get("pokedex")[i]
                    print_pokemon(currentPokemon)
                    printcounter += 1
            if printcounter == 0 or numOfPokemons == 0:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 7:
            print("Back to Pokedex Menu.\n")
            return
        else:
            print("Invalid choice")




########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex(ownerRoot):
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    if ownerRoot is None:
        print("No owners at all")
        return
    ownerName = input("Owner name:\n")
    currentOwner = find_owner_bst(ownerRoot,ownerName)
    if currentOwner is None:
        print(f"Owner '{ownerName}' not found.")
        return
    choice = 1
    while choice != 5:
        print(f"-- {currentOwner['owner']}\'s Pokedex Menu --\n1. Add Pokemon\n2. Display Pokedex\n3. Release Pokemon\n"
              "4. Evolve Pokemon\n5. Back to Main")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            newPokemon2 = None
            numOfPokemons = len(currentOwner["pokedex"])
            id = read_int_safe("Enter Pokemon ID to add: ")
            if id < 1 or id > 135:
                print(f"ID {id} not found in Honen data.")
                continue
            else:
                newPokemon = get_poke_dict_by_id(id)
                for i in range(numOfPokemons):
                    if id == currentOwner["pokedex"][i]["ID"]:
                        print("Pokemon already in the list. No changes made.")
                        newPokemon2 = currentOwner["pokedex"][i]
                        continue
                if newPokemon2 is None:
                    add_pokemon_to_owner(currentOwner, newPokemon)
                    print(f'Pokemon {newPokemon.get("Name")} (ID {id}) added to {currentOwner["owner"]}\'s Pokedex.')
                    continue
        elif choice == 2:
            display_filter_sub_menu(currentOwner)
        elif choice == 3:
            release_pokemon_by_name(currentOwner)
        elif choice == 4:
            evolve_pokemon_by_name(currentOwner)
        elif choice == 5:
            print("Back to Main Menu.\n")
            return
        else:
            print("Invalid choice")

def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    numOfOwners = 0
    choice = 1
    while choice != 6:
        print("=== Main Menu ===\n1. New Pokedex\n2. Existing Pokedex\n3. Delete a Pokedex\n"
          "4. Display owners by number of Pokemon\n5. Print All\n6. Exit")
        choice = read_int_safe("Your choice: ")
        if numOfOwners == 0:
            ownerRoot = None
        if choice == 1:
            ownerName = input('Owner name: ')
            if  numOfOwners != 0 and find_owner_bst(ownerRoot,ownerName) != None:
                print(f"Owner '{ownerName}' already exists. No new Pokedex created.\n")
                continue
            print("Choose your starter Pokemon:\n1) Treecko\n2) Torchic\n3) Mudkip")
            chosenPokemon = read_int_safe("Your choice: ")
            if chosenPokemon == 1:
                firstPokemon = get_poke_dict_by_id(1)
                print(f'New Pokedex created for {ownerName} with starter {firstPokemon.get("Name")}.')
            elif chosenPokemon == 2:
                firstPokemon = get_poke_dict_by_id(4)
                print(f'New Pokedex created for {ownerName} with starter {firstPokemon.get("Name")}.')
            elif chosenPokemon == 3:
                firstPokemon = get_poke_dict_by_id(7)
                print(f'New Pokedex created for {ownerName} with starter {firstPokemon["Name"]}.')
            else:
                print("Invalid. No new Pokedex created.")
                continue
            newOwner = create_owner_node(ownerName, firstPokemon)
            if numOfOwners == 0:
                ownerRoot = newOwner
                numOfOwners += 1
            else:
                if(insert_owner_bst(ownerRoot,newOwner) == True):
                    numOfOwners += 1
        elif choice == 2:
            existing_pokedex(ownerRoot)
        elif choice == 3:
            if ownerRoot is None:
                print("No owner at all")
                continue
            ownerName = input("Enter owner to delete:").lower()
            oldOwner = find_owner_bst(ownerRoot,ownerName)
            if oldOwner is None:
                print(f"Owner '{ownerName}' not found.")
                continue
            oldOwner = delete_owner_bst(ownerRoot,ownerName)
            if oldOwner is ownerRoot:
                ownerRoot = oldOwner
            numOfOwners -= 1
        elif choice == 4:
            sort_owners_by_num_pokemon(ownerRoot,numOfOwners)
        elif choice == 5:
            print_all_owners(ownerRoot,numOfOwners)
        elif choice == 6:
            print("Goodbye!")
            choice = 6
            return
        else:
            print("Invalid choice")


def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()
    pass

if __name__ == "__main__":
    main()
