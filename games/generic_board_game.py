## Base module that should cover most board games. Designed to be extensible and cover cases for most games
import random

class Player:
    ## A player in a board game. Players have a name and a score

    def __init__(self, name):
        self.name = name
        self.score = 0

    def set_score(self, score):
        self.score = score

    def __str__(self):
        retval = None
        if self.score == 0:
            retval = f'{self.name}'
        else:
            retval = f'{self.name} Score is {self.score}'
        return retval

    def __repr__(self):
        return f'<Player name={self.name} score={self.score}>'

class BoardGame:
    ## Base class for a board game. Allows for a board game with players up to a max limit

    def __init__(self, max_players=4, player_type='player', name="Board Game"):
        self.name = name
        self.player_limit = max_players
        self.player_type = player_type
        self.players = []
        self.shuffled_players = []

    def add_player(self, name):
        ## Add a new player to the board game. Returns error if max_player limit reached. 
        if len(self.players) >= self.player_limit:
            raise ValueError(f'{self.player_type.capitalize()} Limit of {self.player_limit} reached. Cannot add more players.')
        else:
            self.players.append(Player(name))

    def get_player_order(self):
        if not self.shuffled_players:
            self.set_player_order()
        return self.shuffled_players

    def set_player_order(self):
        self.shuffled_players = self.players.copy()
        random.shuffle(self.shuffled_players)

    def __repr__(self):
        return f'<Boardgame name={self.name} max_players={self.max_players} player_type={self.player_type} players=({[p.name for p in self.players]})'