import random
import json
from parser import CharacterParser

class GameCharacter:
    def __init__(self, name, health, damage, armor, resist):
        self.name = name
        self.health = health
        self.damage = damage
        self.armor = armor
        self.resist = resist


    def attack(self, target):
        clean_damage = max(self.damage - target.armor, 0)
        final_damage = clean_damage * (1 - target.resist)
        target.health -= final_damage
        return final_damage

    def is_alive(self):
        return self.health > 0

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
            "armor": self.armor,
            "resist": self.resist
        }

    @staticmethod
    def from_dict(data):
        return GameCharacter(
            data["name"],
            data["health"],
            data["damage"],
            data["armor"],
            data["resist"]
        )

    def __str__(self):
        return f"{self.name}: Health={self.health}, Damage={self.damage}, Armor={self.armor}, Resist={self.resist}"


class Game:
    SAVE_FILE = "game_state.json"

    def __init__(self):
        self.characters = []
        self.history = []
        self.turn = 1

    def save_game(self, player, enemy):
        game_state = {
            "player": player.to_dict(),
            "enemy": enemy.to_dict(),
            "turn": self.turn,
            "history": self.history
        }
        with open(self.SAVE_FILE, "w") as file:
            json.dump(game_state, file, indent=4)
        print("Game state saved successfully!")

    def load_game(self):
        try:
            with open(self.SAVE_FILE, "r") as file:
                game_state = json.load(file)
            player = GameCharacter.from_dict(game_state["player"])
            enemy = GameCharacter.from_dict(game_state["enemy"])
            self.turn = game_state["turn"]
            self.history = game_state["history"]
            print("Game state loaded successfully!")
            return player, enemy
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
            return None, None

    def choose_enemy(self, player):
        return random.choice([c for c in self.characters if c != player])

    def load_characters(self):
        parser = CharacterParser()
        data = parser.load_characters()
        self.characters = [
            GameCharacter(
                name=c["name"],
                health=random.randint(50, 100),
                damage=random.randint(10, 20),
                armor=random.randint(5, 10),
                resist=random.uniform(0.1, 0.3)
            )
            for c in data
        ]

    def start(self):
        while True:
            print("1. Start new game")
            print("2. Load saved game")
            print("3. Return to main menu")
            choice = input("Choose an option: ").strip()

            if choice == "2":
                player, enemy = self.load_game()
                if not player or not enemy:
                    self.load_characters()
                    player, enemy = self.choose_characters()
            elif choice == "1":
                self.load_characters()
                player, enemy = self.choose_characters()
            elif choice == "3":
                print("Returning to the main menu...")
                return
            else:
                print("Invalid choice. Please try again.")
                continue

            exit_to_menu = self.play_turns(player, enemy)
            if exit_to_menu:
                return

    def choose_characters(self):
        print("Choose your character:")
        for index, character in enumerate(self.characters, start=1):
            print(f"{index}. {character}")

        choice = int(input("Enter character number: ")) - 1
        player = self.characters[choice]
        enemy = random.choice([c for c in self.characters if c != player])
        print(f"You chose {player.name}. Your enemy is {enemy.name}.")
        return player, enemy

    def play_turns(self, player, enemy):
        while player.is_alive() and enemy.is_alive():
            print(f"Turn {self.turn}:")
            print(f"Your character: {player}")
            print(f"Enemy character: {enemy}")

            action = input("Choose action (attack/defend/save): ").strip().lower()
            if action == "attack":
                damage = player.attack(enemy)
                self.history.append(f"{player.name} attacked {enemy.name} for {damage:.2f} damage.")
                print(f"You dealt {damage:.2f} damage to {enemy.name}.")
            elif action == "defend":
                if random.random() < 0.75:
                    print(f"{player.name} dodged the attack!")
                    self.history.append(f"{player.name} dodged {enemy.name}'s attack.")
                else:
                    reduced_damage = enemy.attack(player) * 0.5
                    player.health -= reduced_damage
                    print(f"{player.name} reduced the damage and took only {reduced_damage:.2f}!")
                    self.history.append(f"{player.name} reduced the damage from {enemy.name}'s attack.")

                heal = random.randint(10, 15)
                player.health += heal
                print(f"{player.name} recovered {heal} health!")
                self.history.append(f"{player.name} defended and recovered {heal} health.")

                counter_damage = player.damage * random.uniform(0.5, 1.0)
                enemy.health -= counter_damage
                print(f"{player.name} counter-attacked and dealt {counter_damage:.2f} damage!")
                self.history.append(f"{player.name} counter-attacked {enemy.name} for {counter_damage:.2f} damage.")
            elif action == "save":
                self.save_game(player, enemy)
                print("Game saved! Returning to the main menu...")
                return  # Завершаем метод, чтобы вернуться в главное меню
            else:
                print("Invalid action. Skipping turn.")

            if enemy.is_alive():
                enemy_damage = enemy.attack(player)
                player.health -= enemy_damage
                self.history.append(f"{enemy.name} attacked {player.name} for {enemy_damage:.2f} damage.")
                print(f"{enemy.name} dealt {enemy_damage:.2f} damage to you.")

            self.turn += 1

        if player.is_alive():
            print("You won!")
        else:
            print("You lost!")

        print("Game history:")
        for event in self.history:
            print(event)

