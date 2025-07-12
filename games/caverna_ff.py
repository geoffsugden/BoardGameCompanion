from games.caverna import Caverna
from games.generic_board_game import Player
import random

class Player_FF(Player):

    def __init__(self, name):
        super().__init__(name)
        self.races = []

    def __str__(self):
        retval = None
        if self.score == 0:
            retval = f'{self.name}\n'
            for i, race in enumerate(self.races, start=1):
                retval += f'\tRace {i} is {race}\n'
        else:
            retval = f'{self.name} Score is {self.score}'
        return retval

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

    def __init__(self):
        super().__init__()

    def add_player(self, name):
        ## Add a new player to the board game. Returns error if max_player limit reached. 
        if len(self.players) >= self.player_limit:
            raise ValueError(f'{self.player_type.capitalize()} Limit of {self.player_limit} reached. Cannot add more players.')
        else:
            self.players.append(Player_FF(name))

    def get_player_order(self):
        super().get_player_order()
        num_players = len(self.shuffled_players)
        shuffled_races = self.RACES.copy()
        random.shuffle(shuffled_races)
        num_races = 1

        if num_players <= 4:
            num_races = 2
        for player in self.shuffled_players:
            for i in range(num_races):
                player.races.append(shuffled_races.pop())
        return self.shuffled_players

