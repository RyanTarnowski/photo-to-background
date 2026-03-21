from pathlib import Path
from globals import OMARCHY_THEME_PATH
import tomllib
import os

home_dir = Path("~").expanduser()
file_path = home_dir / OMARCHY_THEME_PATH

def get_omarchy_theme_colors():
    try:
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)
        
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except tomllib.TOMLDecodeError as e:
        print(f"Error decoding TOML: {e}")

