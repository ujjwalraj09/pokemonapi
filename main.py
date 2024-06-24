import requests
import argparse
import sys
from PIL import Image
from io import BytesIO

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
        base_stats[key]= int(value)

    print(f"Name: {Name}")
    print(f"National Number: {National_number}")

    print('Type: ', end = ' ')
    for items in Types:
        type_data = items['type']
        type_name = type_data['name'].capitalize()
        print(type_name, end = ' ')
    print()

    print('Abilities: ', end = ' ')
    for items in Abilities:
        ability_data = items['ability']
        ability_name = ability_data['name'].capitalize()
        print(ability_name, end = ' ')
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