import tkinter as tk
from tkinter import messagebox
from game import Game


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-Based RPG Game")
        self.game = Game()
        self.player = None
        self.enemy = None

        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Main Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Start New Game", command=self.new_game, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Load Saved Game", command=self.load_game, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, height=2).pack(pady=5)

    def new_game(self):
        self.game.load_characters()
        self.choose_character()

    def load_game(self):
        self.player, self.enemy = self.game.load_game()
        if self.player and self.enemy:
            self.battle_screen()
        else:
            messagebox.showinfo("Error", "No saved game found!")

    def choose_character(self):
        self.clear_window()
        tk.Label(self.root, text="Choose Your Character", font=("Arial", 14)).pack(pady=10)

        for index, character in enumerate(self.game.characters, start=1):
            tk.Button(
                self.root,
                text=f"{character.name} (Health: {character.health}, Damage: {character.damage})",
                command=lambda char=character: self.start_battle(char),
                width=40,
                height=2
            ).pack(pady=5)

    def start_battle(self, player):
        self.player = player
        self.enemy = self.game.choose_enemy(player)
        self.battle_screen()

    def battle_screen(self):
        self.clear_window()

        # Player and Enemy Info
        player_frame = tk.Frame(self.root)
        player_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(player_frame, text="Player", font=("Arial", 14)).pack()
        tk.Label(player_frame, text=str(self.player), justify=tk.LEFT).pack()

        enemy_frame = tk.Frame(self.root)
        enemy_frame.pack(side=tk.RIGHT, padx=10)
        tk.Label(enemy_frame, text="Enemy", font=("Arial", 14)).pack()
        tk.Label(enemy_frame, text=str(self.enemy), justify=tk.LEFT).pack()

        # Battle Actions
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=20)
        tk.Button(action_frame, text="Attack", command=self.attack, width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Defend", command=self.defend, width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Save & Exit", command=self.save_game, width=20).pack(side=tk.LEFT, padx=10)

        # Battle Log
        self.log_text = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.log_text.pack(pady=10)

    def attack(self):
        damage = self.player.attack(self.enemy)
        self.add_log(f"You attacked {self.enemy.name} for {damage:.2f} damage.")
        if not self.enemy.is_alive():
            self.add_log(f"You defeated {self.enemy.name}!")
            messagebox.showinfo("Victory", "You won the battle!")
            self.main_menu()
            return
        self.enemy_turn()

    def defend(self):
        self.add_log(f"{self.player.name} defended.")
        self.enemy_turn()

    def save_game(self):
        self.game.save_game(self.player, self.enemy)
        messagebox.showinfo("Game Saved", "Game saved successfully!")
        self.main_menu()

    def enemy_turn(self):
        damage = self.enemy.attack(self.player)
        self.add_log(f"{self.enemy.name} attacked you for {damage:.2f} damage.")
        if not self.player.is_alive():
            self.add_log("You were defeated!")
            messagebox.showinfo("Defeat", "You lost the battle!")
            self.main_menu()

    def add_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
