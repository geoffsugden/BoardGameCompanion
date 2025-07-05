import random

class Player:
    def __init__(self, name):
        self.name = name
        self.turn_order = 0

    def get_name(self):
        return self.name

    def set_turn_order(self, turn_order):
        self.turn_order = turn_order
    
    def get_turn_order(self):
        return self.turn_order

    def __str__(self):
        return self.name

class Drafting_Player(Player):
    def __init__(self, name):
        super().__init__(name)
        self.drafting_choices = []
        self.selected_chocie = None

    def add_draft_choice(self, choice):
        self.drafting_choices.append(choice)
    
    def get_draft_choices(self):
        return self.drafting_choices

class Boardgame:
    
    def __init__(self, max_players=7):
        self.max_players = max_players
        self.players = []

    def add_player(self,player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        else:
            print(f'Max Players Reached, limit is {self.max_players}.')
            return False

    def set_player_order(self):
        random.shuffle(self.players)
        for i, player in enumerate(self.players, start=1):
            player.set_turn_order(i)
        return self.players

    def get_player_order(self):
        if not all(p.turn_order for p in self.players):
            self.set_player_order()
        return sorted(self.players, key=lambda p: p.turn_order)
    
    def game_setup(self):
        self.add_players()
    
    def print_setup(self):
        for i, player in enumerate(self.get_player_order()):
            print(f'Player {i+1} is {player.get_name()}')

    def add_players(self):
        print("When done entering players, press enter.")
        for i in range(self.max_players):
            name = input("Enter player name ")
            if not name.strip():
                break
            self.add_player(Player(name))
        print()
        return True

class Caverna(Boardgame):

    def __init__(self, max_players=7):
        super().__init__(max_players)
        self.game_name = 'Caverna'    
    
class Caverna_FF(Caverna):
    RACES = [
        "Cave Goblins",
        "Dark Elves",
        "Elves",
        "Humans",
        "Mountain Dwarves",
        "Pale Ones",
        "Silicoids",
        "Trolls"
    ]

    def __init__(self, max_players=7):
        super().__init__(max_players)
        self.game_name = 'Caverna: Forgotten Folk'

    def add_players(self):
        print("When done entering players, press enter.")
        for i in range(self.max_players):
            name = input("Enter player name ")
            if not name.strip():
                break
            self.add_player(Drafting_Player(name))
        print()
        return True
        
    def game_setup(self):
        super().game_setup()
        num_players = len(self.players)
        num_choices = 0
        sorted_races = self.RACES
        random.shuffle(sorted_races)
        
        if num_players <= 4:
            num_choices = 2
        else:
            num_choices = 1
            
        for player in self.players:
            for i in range(num_choices):
                player.add_draft_choice(sorted_races.pop(0))      
             
    def print_setup(self):
        for i, player in enumerate(self.get_player_order()):
            print(f'Player {i+1} is {player.get_name()}')
            for i, choice in enumerate(player.get_draft_choices(), start=1):
                print(f'\tChoice {i} is {choice}')

SUPPORTED_GAMES = {
    "caverna": (Caverna, "Caverna"),
    "caverna_ff": (Caverna_FF, "Caverna: Forgotten Folk"),
    "board_game": (Boardgame, "Other")
}

print("What game are you playing?")
for i, (key,(_,name)) in enumerate(SUPPORTED_GAMES.items(),start=1):
    print(f'{i}. {name}')

playing = input("Choose game by number ").strip()

index = int(playing)-1
key = list(SUPPORTED_GAMES.keys())[index]
Boardgame = SUPPORTED_GAMES[key][0]()

Boardgame.game_setup()
Boardgame.print_setup()



# def player_list(num_players=7):
#     for i in range (num_players):
#         print(f'Enter player number {i+1}, leave blank if no more players')
#         player = input()
#         if len(player) <= 0:
#             break
#         else:
#             players.append(player)
#     return players

# def first_player(players):
#     num_players = len(players)
#     first_index = random.randint(0,num_players-1)
#     return players[first_index]

# def player_order(players):
#     random.shuffle(players)
#     return players

# if int(gameversion) not in {1,2,3}:
#     print("Please enter a valid option 1, 2 or 3")
#     time.sleep(2)
#     sys.exit()
# elif int(gameversion) == 3:
#     players = player_list()
#     players = player_order(players)
#     for i,player in enumerate(players):
#         print(f'Player {i+1} is {player}')
#     sys.exit()
# elif int(gameversion) == 2:
#     players = player_list()
#     print(f'First Player is {first_player(players)}')
#     print()
# else:
#     players = player_list()
#     print(f'First Player is {first_player(players)}')
#     print("Std")



print("--__--")
input()
exit()

