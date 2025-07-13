from games.generic_board_game import BoardGame, Player

class Caverna(BoardGame):

    def __init__(self):
        super().__init__(max_players=7, player_type='dwarf', player_types='dwarves', name='Caverna')