## Holds classes specific to Caverna and Caverna Expansions. Allows for specific additions to players for scoring etc. 
import random
import BoardGames

class Caverna(BoardGames.Boardgame):

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
            self.add_player(BoardGames.Drafting_Player(name))
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