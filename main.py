import requests
import argparse
import sys
from PIL import Image
from io import BytesIO

BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m' 
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_MAGENTA = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_LIGHT_GRAY = '\033[47m'
BACKGROUND_DARK_GRAY = '\033[100m'
BACKGROUND_BRIGHT_RED = '\033[101m'
BACKGROUND_BRIGHT_GREEN = '\033[102m'
BACKGROUND_BRIGHT_YELLOW = '\033[103m'
BACKGROUND_BRIGHT_BLUE = '\033[104m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
BACKGROUND_BRIGHT_CYAN = '\033[106m'
BACKGROUND_WHITE = '\033[107m'
RESET = '\033[0m'

def get_pokemon_type_color(pokemon_type):
    switcher = {
        'NORMAL': BACKGROUND_WHITE,
        'FIRE': BACKGROUND_RED,
        'WATER': BACKGROUND_BLUE,
        'ELECTRIC': BACKGROUND_YELLOW,
        'GRASS': BACKGROUND_GREEN,
        'ICE': BACKGROUND_CYAN,
        'FIGHTING': BACKGROUND_DARK_GRAY,
        'POISON': BACKGROUND_MAGENTA,
        'GROUND': BACKGROUND_BRIGHT_YELLOW,
        'FLYING': BACKGROUND_LIGHT_GRAY,
        'PSYCHIC': BACKGROUND_BRIGHT_MAGENTA,
        'BUG': BACKGROUND_GREEN,
        'ROCK': BACKGROUND_DARK_GRAY,
        'GHOST': BACKGROUND_BRIGHT_RED,
        'DRAGON': BACKGROUND_BRIGHT_BLUE,
        'DARK': BACKGROUND_BLACK,
        'STEEL': BACKGROUND_LIGHT_GRAY,
        'FAIRY': BACKGROUND_BRIGHT_CYAN
    }
    return switcher.get(pokemon_type.upper(), RESET)

def save_image_from_url(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(filename)
            print(f"Image saved as {filename}")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching and saving image: {str(e)}")

def fetch_image(data):
    image = data['sprites']
    image_url = image['front_shiny']
    Name = data['name'].capitalize()
    # filename = Name+".png"
    filename = "sprite.png"
    save_image_from_url(image_url, filename)

def convert_to_title_case(input_string):
    words = input_string.split('-')
    capitalized_words = [word.capitalize() for word in words]
    converted_string = ' '.join(capitalized_words)
    
    return converted_string

def pokemon_print_details(data):
    Name = data['name'].capitalize()
    National_number = data['id']   
      
    Types = data['types']
    Abilities = data['abilities']

    Height = int(data['height'])/10
    Weight = int(data['weight'])/10
    stats = data['stats']
 
    base_stats = {}
    for items in stats:
        stat = items['stat']
        key = stat['name']
        value = items['base_stat']
        base_stats[key] = int(value)

    print(f"Name: {Name}")
    print(f"National Number: {National_number}")

    print('Type:', end=' ')
    for items in Types:
        type_data = items['type']
        type_name = type_data['name'].upper()
        print(f"{get_pokemon_type_color(type_name)} {type_name} {RESET}", end=' ')
    print()

    print('Abilities:', end=' ')
    for items in Abilities:
        ability_data = items['ability']
        ability_name = ability_data['name'].capitalize()
        print(ability_name, end=' ')
    print()

    print(f"Height: {Height} m")
    print(f"Weight: {Weight} Kg")
    print()
    print("Base stats:")
    total = 0
    for items in base_stats:
        print(f"{convert_to_title_case(items)}: {base_stats[items]}")
        total += base_stats[items]
    print(f"Total: {total}")
    fetch_image(data)

def fetch_pokemon(pokemon):
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = base_url + pokemon

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_print_details(data)
        
    else:
        print(response.status_code)

def main():
    parser = argparse.ArgumentParser(description="Fetch pokemon name from cmd")
    parser.add_argument('pokemon', type=str, help='The pokemon name to fetch')
    args = parser.parse_args()
    fetch_pokemon(args.pokemon)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: Pokemon Name not provided")
        sys.exit(1)
    main()
