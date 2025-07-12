import yaml
from importlib import import_module

module = None
bg_class = None

# To aid extensibilty we load the supported games from a config file. 
# Once a user has selected the game that they want to play then we import that module. 

print('{:-<119}'.format(''))
print('Please choose a game from the below by typing the id and pressing enter, type ''desc id''  for more information on a game:')
print('type ''quit'' to quit')
print('{:-<119}'.format(''))


def load_game_list(path='supported_games.yaml'):
    with open('supported_games.yaml', 'r') as f:
        game_data = yaml.safe_load(f)
    return game_data['board_games']

game_list = load_game_list()

for game in game_list:
            
    print(f'Name: {game["name"]:40s}', end='')
    print(f'ID:{game["id"]}')
    print()

while True:   
    ipt = input()
    if ipt.lower().strip() == 'quit':
        break
    elif ipt[:4].lower() == 'desc':
        id = ipt[5:]
        for game in game_list:
            if game['id'] == id:
                print(game['description'])
                print('type ''play'' to play this game')
                ipt = input()
                if ipt.lower().strip() == 'quit':
                    break
                elif ipt.lower().strip() == 'play':
                    module = game['module']
                    bg_class = game['class']
                    break
        if ipt.lower().strip() in ('quit','play'):
            break
    else: 
        for game in game_list:
            if game['id'] == ipt:
                module = game['module']
                bg_class = game['class']
        break


    
if not module:
    print('Goodbye')
    exit()

BG_mod = import_module(module)
cls = getattr(BG_mod, bg_class)
BG = cls()

playing_game = f'Playing {BG.name}'

for i in range(len(playing_game)):
    print('-', end='')

print()
print(playing_game)
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

for player in BG.players:
    print(f'{BG.player_type.capitalize()} = {player.name}')

print()
print()

for i, player in enumerate(BG.get_player_order(), start=1):
    print(f'Player {i} is {player}')

