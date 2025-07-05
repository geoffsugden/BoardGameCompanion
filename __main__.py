import BoardGames
import Caverna

SUPPORTED_GAMES = {
    "caverna": (Caverna.Caverna, "Caverna"),
    "caverna_ff": (Caverna.Caverna_FF, "Caverna: Forgotten Folk"),
    "board_game": (BoardGames.Boardgame, "Other")
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

exit()

