import requests
import json

class CharacterParser:
    BASE_API_URL = "https://genshin.jmp.blue/"
    CHARACTERS_ENDPOINT = "characters"

    def fetch_characters(self):
        try:
            response = requests.get(self.BASE_API_URL + self.CHARACTERS_ENDPOINT)
            response.raise_for_status()
            character_names = response.json()
            characters = []

            for name in character_names:
                url = f"{self.BASE_API_URL}{self.CHARACTERS_ENDPOINT}/{name}"
                char_response = requests.get(url)
                if char_response.status_code == 200:
                    character_data = char_response.json()
                    characters.append({
                        "name": character_data.get("name"),
                        "element": character_data.get("element"),
                        "rarity": character_data.get("rarity"),
                        "weapon": character_data.get("weapon"),
                        "description": character_data.get("description"),
                        "image": character_data.get("image")
                    })
                else:
                    print(f"Failed to fetch details for {name}")
            return characters
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []

    def load_characters(self, file_name="characters.json"):
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"No character file found at {file_name}. Please fetch and save characters first.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_name}. Ensure the file is not corrupted.")
            return []

    def save_characters(self, characters, file_name="characters.json"):
        try:
            with open(file_name, "w") as file:
                json.dump(characters, file, indent=4)
            print(f"Characters successfully saved to {file_name}.")
        except Exception as e:
            print(f"Error saving characters: {e}")

