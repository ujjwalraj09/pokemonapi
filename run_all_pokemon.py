import subprocess
import requests

def get_all_pokemon_names():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"  # large limit to get all Pokémon
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        names = [pokemon['name'] for pokemon in data['results']]
        return names
    else:
        print(f"Failed to fetch Pokémon names. Status code: {response.status_code}")
        return []

def run_script_for_all_pokemon():
    pokemon_names = get_all_pokemon_names()
    with open('pokemon_data.txt', 'w') as file:
        for pokemon_name in pokemon_names:
            print(f"Processing {pokemon_name}...")
            result = subprocess.run(['python3', 'main.py', pokemon_name], capture_output=True, text=True)
            file.write(result.stdout)
            file.write("\n\n")  # separate each Pokémon's data with a new line

if __name__ == "__main__":
    run_script_for_all_pokemon()
