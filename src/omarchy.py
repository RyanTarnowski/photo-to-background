import tomllib

def get_omarchy_theme_colors(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)
        
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except tomllib.TOMLDecodeError as e:
        print(f"Error decoding TOML: {e}")

