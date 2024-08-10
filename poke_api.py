'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os
import image_lib

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_info() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")
    download_pokemon_artwork('dugtrio', r'C:\temp')
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return None

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_pokemon_names(limit=100000, offset=0):
    """Gets a list of all Pokemon names from the PokeAPI.

    Args:
        limit (int): Maximum number of Pokemon names to fetch. Defaults to 100000.
        offset (int): The starting point in the list of Pokemon names. Defaults to 0.

    Returns:
        list: List of Pokemon names, if successful. Otherwise None.
    """
    print(f'Getting list of Pokemon names....', end='')
    params = {
        'limit': limit,
        'offset': offset
    }
    resp_msg = requests.get(POKE_API_URL, params=params)
    if resp_msg.status_code == requests.codes.ok:
        print('Success')
        resp_dict = resp_msg.json()
        return [p['name'] for p in resp_dict['results']]
    else:
        print('Failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def download_pokemon_artwork(pokemon_name, folder_path='.'):
    """Downloads and saves the official artwork of a specified Pokemon.

    Args:
        pokemon_name (str): Name of the Pokemon to download artwork for.
        folder_path (str): Path to the folder where the artwork will be saved.

    Returns:
        str: Path to the saved image file, if successful. Otherwise None.
    """
    poke_info = get_pokemon_info(pokemon_name)
    if poke_info is None:
        return None

    # Extract the artwork URL from the info dictionary
    artwork_url = poke_info['sprites']['other']['official-artwork']['front_default']
    if artwork_url is None:
        print(f"No artwork available for {pokemon_name.capitalize()}.")
        return None

    # Determine the image file path
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(folder_path, f'{pokemon_name}.{file_ext}')

    # Don't download Pokemon artwork if there already exists one
    if os.path.exists(image_path):
        print(f"Artwork for {pokemon_name.capitalize()} already exists.")
        return image_path

    # Download and save the image
    print(f'Downloading artwork for {pokemon_name.capitalize()}...', end='')
    image_data = image_lib.download_image(artwork_url)
    if image_data is None:
        return None

    if image_lib.save_image_file(image_data, image_path):
        print(f'Artwork saved at {image_path}')
        return image_path

    return None

if __name__ == '__main__':
    main()
