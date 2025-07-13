# Takes care of initial game selection and then loading of games. 
# Supported games must be written before entering into the configuration file. While they will be displayed their selection will cause and exception. 
# Current implementation supports console only, further work should be done at some point to de-couple a lot of this code from the interface used. 

import yaml
from importlib import import_module
from pathlib import Path

# Defines a list of supported commands that can be used when editing via the CLI (yes I really need to decouple interface.)
# Stored as a tuple ([command],[description]). 
# command must be exactly one 4 length string of lower case alpha characters. 
# description is a more verbose description of what the command does in natural language e.g. Exits the session. 
SUPPORTED_COMMANDS = [
    ('quit', 'Exits the session.'),
    ('help', 'Provides information on use of interface.'),
    ('play', 'When followed by a game id launchs the companion app for that game. e.g. ''play gbg'''),
    ('load', 'When followed by a game id allows the user to select a previously played game. e.g. ''play gbg'''),
    ('desc', 'When followed by a game id displays additoinal information for that game. e.g. ''play gbg''')
]

# defining global variables - Only one game should be selected per instance of the program running. 
# module = None
# bg_class = None

# To aid extensibilty we load the supported games from a config file. 
# Once a user has selected the game that they want to play then we import that module. 

print('{:-<119}'.format(''))
print('Choose a game from the below using the ''play'' command. type ''quit'' to quit, or ''help'' for supported commands')
print('{:-<119}'.format(''))

def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def load_game_list(path='supported_games.yaml'):
    
    with open(path, 'r') as f:  
        game_data = yaml.safe_load(f)
        return {next(iter(d)): d[next(iter(d))] for d in game_data['board_games']}

# At this stage just the name and the id is enough for each game. The user can request more information later on. 
# This could be extended at a later date to show what information is avialable for each game.
games = load_game_list()

for key, game in games.items():
    print(f'Name: {game["name"]:40s}', end='')
    print(f'ID:{key}')
    print()

BG = None
command = None
# The below  currently relys on 4 letter codes to allow the user to perform functions. 
while True:   
    module = None
    bg_class = None   
    game_str = None
    game = None
    ipt = input('Enter command or ''help'' for assistance: ').split(' ', 1)
    
    command = ipt[0].lower().strip()
    if(len(ipt) > 1):
        game_str = ipt[1].lower().strip()

    if game_str:       
        game = games.get(game_str)
        if not game:
            print(f'Game id {game_str} is not valid, some commands will not work as intended, please try again. type ''help'' for a list of commands.')
            command = 'invalid_input'

    match command:
        case 'quit':
            break
        case 'help':
            print()
            for a in SUPPORTED_COMMANDS:
                print(f'{a[0]}: {a[1]}')
                #print(a)
            print()
        case 'desc':
            if game:
                print(game.get('description'))
            else: 
                print('Please enter ''desc'' followed by the game id.')
        case 'play':
            if game:
                BG_mod = import_module(game.get('module'))
                cls = getattr(BG_mod, game.get('class'))
                BG = cls()
                break
            else:
                print('Please enter ''play'' followed by the game id.')
        case 'load':
            if game:
                BG_mod = import_module(game.get('module'))
                cls = getattr(BG_mod, game.get('class'))
                BG = cls()
                break
            else:
                print('Please enter ''play'' followed by the game id.')
        # case 'expn': for expansions TODO
        case 'invalid_input':
            pass
        case _:
            print('Command not recognised. Please enter one of the following:')
            for a in SUPPORTED_COMMANDS:
                print(f'{a[0]}: {a[1]}')
                #print(a)
            print()

playing_game = f'Playing {BG.name}'

for i in range(len(playing_game)):
    print('-', end='')
print(f'\n{playing_game}')
for i in range(len(playing_game)):
    print('-', end='')
print()

config = load_config()
save_file_name = game.get('save_file')
#Make sure that the directory exists for save files
savedir = Path.home() / Path(config['save_path'].lstrip('\\/')) / Path(save_file_name)
savedir.parent.mkdir(parents=True, exist_ok=True)

save_file = {}
if savedir.is_file():
    with savedir.open('r') as f:
        save_file = yaml.safe_load(f) or {}

if command == 'load':
    for key in save_file:
        print(f'Game id = {key}, Players are:')
        players = save_file[key]['players']
        for player in players:
            print(f'\tPlayer {player}: {players[player]}')
    input('Enter game id: ')
# TODO implment load_game method in Board Game
elif command == 'play':
    print("About to set up the game...")
    # Hand off the rest to the individual board game class, plus the interface that is 
    BG.setup_game(save_file)

with savedir.open('w') as f:
    yaml.safe_dump(save_file, f)

print("Finished setting up the game.")

