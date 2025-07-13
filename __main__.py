# Takes care of initial game selection and then loading of games. 
# Supported games must be written before entering into the configuration file. While they will be displayed their selection will cause and exception. 
# Current implementation supports console only, further work should be done at some point to de-couple a lot of this code from the interface used. 

import yaml
from importlib import import_module

# Defines a list of supported commands that can be used when editing via the CLI (yes I really need to decouple interface.)
# Stored as a tuple ([command],[description]). 
# command must be exactly one 4 length string of lower case alpha characters. 
# description is a more verbose description of what the command does in natural language e.g. Exits the session. 
SUPPORTED_COMMANDS = [
    ('quit', 'Exits the session.'),
    ('help', 'Provides information on use of interface.'),
    ('play', 'When followed by a game id launchs the companion app for that game. e.g. ''play gbg'''),
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


def load_game_list(path='supported_games.yaml'):
    
    with open('supported_games.yaml', 'r') as f:  
        game_data = yaml.safe_load(f)
        return {next(iter(d)): d[next(iter(d))] for d in game_data['board_games']}

# At this stage just the name and the id is enough for each game. The user can request more information later on. 
# This could be extended at a later date to show what information is avialable for each game.
games = load_game_list()

for key, game in games.items():
    print(f'Name: {game["name"]:40s}', end='')
    print(f'ID:{key}')
    print()

# The below  currently relys on 4 letter codes to allow the user to perform functions. 
while True:   
    module = None
    bg_class = None
    command = None
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
                module = game.get('module')
                bg_class = game.get('class')
                break
            else:
                print('Please enter ''play'' followed by the game id.')
        # case 'expn':
        case 'invalid_input':
            pass
        case _:
            print('Command not recognised. Please enter one of the following:')
            for a in SUPPORTED_COMMANDS:
                print(f'{a[0]}: {a[1]}')
                #print(a)
            print()

    
if not module:
    print('Goodbye')
    exit()

BG_mod = import_module(module)
cls = getattr(BG_mod, bg_class)
BG = cls()

playing_game = f'Playing {BG.name}'

for i in range(len(playing_game)):
    print('-', end='')
print(f'\n{playing_game}')
for i in range(len(playing_game)):
    print('-', end='')
print()

while True:
    print(f'Enter {BG.player_type.capitalize()} name: ', end='')
    name = input()
    if not name.strip():
        break
    else:
        BG.add_player(name)

# Just some spacing to make the output look better
print('\n')

for i, player in enumerate(BG.get_player_order(), start=1):
    print(f'Player {i} is {player}')

