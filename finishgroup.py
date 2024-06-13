# This program stores move objects to Pokemon objects and allows the Pokemon to "battle" until one opponent's hit points are at 0.

# Import required libraries
import random

# Create required lists
move_lst = []
pokemon_list = []

# Write Move class
class Move:
    def __init__(self, move_name, elemental_type, low_attack_points, high_attack_points):
        self.move_name = move_name
        self.elemental_type = elemental_type
        self.low_attack_points = low_attack_points
        self.high_attack_points = high_attack_points
    
    def get_info(self):
        return f"{self.move_name} (Type: {self.elemental_type}): {self.low_attack_points}-{self.high_attack_points}"
    
    def generate_attack_value(self):
        return random.randint(self.low_attack_points, self.high_attack_points)

# Write Pokemon class
class Pokemon:
    def __init__(self, name, elemental_type, hit_points):
        self.name = name
        self.elemental_type = elemental_type
        self.hit_points = hit_points
        self.list_of_moves = []
    
    def get_info(self):
        return f"{self.name} - Type: {self.elemental_type} - Hit Points: {self.hit_points}"
    
    def heal(self):
        self.hit_points += 15
        return f"\n{self.name} has been healed to {self.hit_points} hit points."
    
    def display_choices(self):
        choices = ""
        for counter, move in enumerate(self.list_of_moves, start=1):
            choices += f"{counter}: {move.move_name} (Type: {move.elemental_type}) {move.low_attack_points}-{move.high_attack_points} Attack Points\n"
        choices += "H: Heal 15 hit points"
        return choices
    
    def attack(self, move_index, opposing_pokemon):
        move = self.list_of_moves[move_index]
        attack_value = move.generate_attack_value()
        effectiveness = ""

        if move.elemental_type == "Grass" and opposing_pokemon.elemental_type == "Fire":
            attack_value *= 0.5
            effectiveness = "It's not very effective..."
        elif move.elemental_type == "Grass" and opposing_pokemon.elemental_type == "Water":
            attack_value *= 2.0
            effectiveness = "It's super effective!"
        elif move.elemental_type == "Fire" and opposing_pokemon.elemental_type == "Water":
            attack_value *= 0.5
            effectiveness = "It's not very effective..."
        elif move.elemental_type == "Fire" and opposing_pokemon.elemental_type == "Grass":
            attack_value *= 2.0
            effectiveness = "It's super effective!"
        elif move.elemental_type == "Water" and opposing_pokemon.elemental_type == "Grass":
            attack_value *= 0.5
            effectiveness = "It's not very effective..."
        elif move.elemental_type == "Water" and opposing_pokemon.elemental_type == "Fire":
            attack_value *= 2.0
            effectiveness = "It's super effective!"
        elif move.elemental_type == "Normal" :
            attack_value *= 1.0
            effectiveness = "There was no effect."
        
        critical_hit = random.randint(1, 100)
        if critical_hit <= 6:
            attack_value *= 1.5
            effectiveness = "Critical hit!"
        
        attack_value = round(attack_value)
        opposing_pokemon.hit_points -= attack_value
        
        return attack_value, effectiveness

# Write pokemon_battle function separate from classes
def pokemon_battle(your_pokemon, opposing_pokemon):
    print(f"\nBATTLE START!\n{opposing_pokemon.name} wants to fight!\nGo! {your_pokemon.name}!")

    while your_pokemon.hit_points > 0 and opposing_pokemon.hit_points > 0:
        print(f"Opponent: {opposing_pokemon.get_info()}")
        print(f"You: {your_pokemon.get_info()}\n")

        print("\nYour options:")
        print(your_pokemon.display_choices())
        
        chosen_option = input("Choose an option: ")

        if chosen_option.upper() == "H":
            print(your_pokemon.heal())
        elif chosen_option in ["1", "2"]:
            move_index = int(chosen_option) - 1
            if 0 <= move_index < len(your_pokemon.list_of_moves):
                attack_value, effectiveness = your_pokemon.attack(move_index, opposing_pokemon)
                print(f"\n{your_pokemon.name} used {your_pokemon.list_of_moves[move_index].move_name}!")
                print(effectiveness)
                print(f"{opposing_pokemon.name} took {attack_value} points of damage!\n")
                input("Press enter to proceed . . . ")
            else:
                print("Invalid move index. Please choose again.")
        else:
            print("Invalid choice. Please choose again.")
            continue
        
        if opposing_pokemon.hit_points <= 0:
            break
        
        cpu_move_index = random.randint(0, len(opposing_pokemon.list_of_moves) - 1)
        attack_value, effectiveness = opposing_pokemon.attack(cpu_move_index, your_pokemon)
        print(f"\n{opposing_pokemon.name} chose {opposing_pokemon.list_of_moves[cpu_move_index].move_name}!")
        print(effectiveness)
        print(f"{your_pokemon.name} took {attack_value} points of damage!\n")
        
        if your_pokemon.hit_points <= 0:
            break
        
        input("Press enter to proceed...")
        print()
    
    if your_pokemon.hit_points <= 0:
        print(f"\n{your_pokemon.name} has been defeated.\n{opposing_pokemon.name} has won!")
    elif opposing_pokemon.hit_points <= 0:
        print(f"\n{opposing_pokemon.name} has been defeated.\n{your_pokemon.name} has won!")

def choosing_attack():
    assigned_moves = {}
    for pokemon in pokemon_list:
        while len(pokemon.list_of_moves) < 2:
            attack = random.choice(move_lst)
            if attack.elemental_type == pokemon.elemental_type or attack.elemental_type == "Normal":
                pokemon.list_of_moves.append(attack)
                move_lst.remove(attack)
        assigned_moves[pokemon.name] = [move.move_name for move in pokemon.list_of_moves]
    return assigned_moves

def choose_pokemon():
    try:
        your_pokemon_index = int(input("Choose the # of your pokemon: ")) - 1
        if 0 <= your_pokemon_index < len(pokemon_list):
            return pokemon_list.pop(your_pokemon_index)
        else:
            print("Invalid choice. Please choose a valid number.")
            return choose_pokemon()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return choose_pokemon()

def choose_opponent_pokemon():
    pokemon_count = 1
    for pokemon in pokemon_list:
        print(f"{pokemon_count}: {pokemon.name} - Type: {pokemon.elemental_type} - Hit Points: {pokemon.hit_points}")
        pokemon_count += 1
    
    try:
        your_opponent_pokemon_index = int(input("Choose the # of your opponent's pokemon: ")) - 1
        if 0 <= your_opponent_pokemon_index < len(pokemon_list):
            return pokemon_list.pop(your_opponent_pokemon_index)
        else:
            print("Invalid choice. Please choose a valid number.")
            return choose_opponent_pokemon()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return choose_opponent_pokemon()

# Create the move objects
move_lst.append(Move("Tackle", "Normal", 5, 20))
move_lst.append(Move("Quick Attack", "Normal", 6, 25))
move_lst.append(Move("Slash", "Normal", 10, 30))
move_lst.append(Move("Flamethrower", "Fire", 5, 30))
move_lst.append(Move("Ember", "Fire", 10, 20))
move_lst.append(Move("Water Gun", "Water", 5, 15))
move_lst.append(Move("Hydro Pump", "Water", 20, 25))
move_lst.append(Move("Vine Whip", "Grass", 10, 25))
move_lst.append(Move("Solar Beam", "Grass", 18, 27))

# Create Pokemon objects and append to the Pokemon list
pokemon_list.append(Pokemon("Bulbasaur", "Grass", 60))
pokemon_list.append(Pokemon("Charmander", "Fire", 55))
pokemon_list.append(Pokemon("Squirtle", "Water", 65))

# Display the moves that will be chosen from
print("These are the moves the pokemon will randomly choose from:")
for move in move_lst:
    print("\t" + move.get_info())
# print("H: Heal 15 hit points\n")

# Set variable assigned moves to the executing of the choosing_attack function
assigned_moves = choosing_attack()

# Display the results of the choosing_attack function in the correct format
for pokemon, moves in assigned_moves.items():
    print(f"\n{pokemon} was assigned:")  # Print the name of the pokemon 
    for move in moves:
        print(f"    {move}")  # And then print its assigned names
    
# Print a statement that lists all available Pokemon for the user to choose from
print("\nAvailable Pokemon:")

# Have a for loop go through and print each item name in the enumerated list
enum_p_list = enumerate(pokemon_list, start=1)  # Enumerate the list using 'enumerate' function
for index, item in enum_p_list:  # For each indexed item in the list . . . 
    print(f"{index}: {item.name} - Type: {item.elemental_type} - Hit Points: {item.hit_points}")  # Use reference word 'item' instead of 'pokemon'

# Have user choose their pokemon using the choose_pokemon function
your_pokemon = choose_pokemon()
print(f"\nYou chose {your_pokemon.name} as your pokemon\n")

# Have user choose opponent's pokemon using choose_opponent_pokemon function
opposing_pokemon = choose_opponent_pokemon()
print(f"\nYou chose {opposing_pokemon.name} as the opponent.")

# Have the pokemon battle
pokemon_battle(your_pokemon, opposing_pokemon)