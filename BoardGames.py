## Contains base classes for board games. 
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