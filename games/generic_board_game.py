## Base module that should cover most board games. Designed to be extensible and cover cases for most games
import random
from datetime import datetime

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

    def __init__(self, max_players=4, player_type='player', player_types='players', name="Board Game"):
        #p = engine()
        self.name = name
        self.player_limit = max_players
        self.player_type = player_type
        self.player_types = player_types
        self.players = []
        self.shuffled_players = []

    def add_player(self, name):
        ## Add a new player to the board game. Returns error if max_player limit reached. 
        if len(self.players) >= self.player_limit:
            raise ValueError(f'{self.player_type.capitalize()} Limit of {self.player_limit} reached. Cannot add more players.')
        else:
            
            #make sure that the player name is unique
            for player in self.players:
                if player.name.strip().lower() == name.strip().lower():
                    raise ValueError(f'{name.strip()} is taken. Case tricks won’t work—names must be unique!')
            self.players.append(Player(name))


    def get_player_order(self):
        if not self.shuffled_players:
            self.set_player_order()
        return self.shuffled_players

    def set_player_order(self):
        self.shuffled_players = self.players.copy()
        random.shuffle(self.shuffled_players)

    def setup_game_cli(self, game_file={}):
        
        cur_game = {}
        #add players 
        print(f'When finished adding {self.player_types.capitalize()} press Enter key')
        while len(self.players) <= self.player_limit:
            print(f'Enter {self.player_type.capitalize()} name: ', end='')
            name = input()
            if not name.strip():
                # ends the loop if there are no more players. (no player name entered)
                break
            else:
                try:
                    self.add_player(name)
                except ValueError as e:
                    print(f'{e}')
                    continue

        #sort player order
        self.set_player_order()

        #return game file details        
        #generate an ID - we need to know if there are any other save games for the same day. 
        id = datetime.now().strftime('%y%m%d')
        if not game_file:
            #if there is no game file then this will be the first game.
            id = f'{id}-001'
        else: 
            #otherwise iterate through the keys to check for an appropiate game id
            day_games = []
            for key in game_file:
                if id == key[:6]:
                    day_games.append(key)
            if day_games:
                day_games.sort()
                last_key = day_games.pop()
                game_num = int(last_key[-3:].lstrip('0')) + 1
                id = f'{id}-{str(game_num).zfill(3)}'                    
            else: 
                id = f'{id}-001'

        game_players = {}
        #return player order
        for i, player in enumerate(self.get_player_order(), start=1):
            game_players[i] = player.name
            
        cur_game['players'] = game_players
        game_file[id] = cur_game

    
    def setup_game(self, game_file, interface='cli'):
        # Create a class that directly access the interface. This allows for the complexities of individual games to be dealt with. 
        self.setup_game_cli(game_file)

    def __repr__(self):
        return f'<Boardgame name={self.name} max_players={self.max_players} player_type={self.player_type} players=({[p.name for p in self.players]})'