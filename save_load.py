import json

class SaveLoadManager:
    FILE_NAME = "game_state.json"

    @staticmethod
    def save_game(player, enemy, turn, history):
        try:
            game_state = {
                "player": {
                    "name": player.name,
                    "health": player.health,
                    "damage": player.damage,
                    "armor": player.armor,
                    "resist": player.resist
                },
                "enemy": {
                    "name": enemy.name,
                    "health": enemy.health,
                    "damage": enemy.damage,
                    "armor": enemy.armor,
                    "resist": enemy.resist
                },
                "turn": turn,
                "history": history
            }
            with open(SaveLoadManager.FILE_NAME, "w") as file:
                json.dump(game_state, file, indent=4)
            print(f"Game successfully saved to {SaveLoadManager.FILE_NAME}.")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game():
        try:
            with open(SaveLoadManager.FILE_NAME, "r") as file:
                game_state = json.load(file)
            print(f"Game successfully loaded from {SaveLoadManager.FILE_NAME}.")
            return game_state
        except FileNotFoundError:
            print(f"No saved game found in {SaveLoadManager.FILE_NAME}.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding saved game file {SaveLoadManager.FILE_NAME}.")
            return None
