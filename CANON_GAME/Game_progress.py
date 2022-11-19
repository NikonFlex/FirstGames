import json

def read_file_with_progress():
    try:
        print('try')
        with open(r'.\resources\cannon_game_progress.json') as game_progress:
            game_progress = json.load(game_progress)
        print('e5y4r5h')
        return Game_progress(game_progress['cannon_level'], game_progress['coins_n'], game_progress['game_level'])
    except:
        print('except')
        return Game_progress(1, 0, 1)
    
class Game_progress:
    def __init__(self, cannon_level, coins_n, game_level):
        self.cannon_level = cannon_level
        self.coins_n = coins_n
        self.game_level = game_level

    def write_game_progress(self):
        with open(r'.\resources\cannon_game_progress.json', 'w') as game_progress:
            json.dump(vars(self), game_progress)