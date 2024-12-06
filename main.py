from parser import CharacterParser
from game import Game

def main():
    print("Welcome to the Character Catalog and Game!")
    print("1. Load characters from API")
    print("2. Start text-based game")
    print("3. Exit")
    
    choice = input("Choose an option: ").strip()

    if choice == "1":
        parser = CharacterParser()
        characters = parser.fetch_characters()
        parser.save_characters(characters)
        print("Characters fetched and saved successfully!")
    elif choice == "2":
        game = Game()
        game.start()
    elif choice == "3":
        print("Exiting the application. Goodbye!")
    else:
        print("Invalid choice. Please restart the program.")

if __name__ == "__main__":
    main()
