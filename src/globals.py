from enum import Enum
import json

RESOLUTION = {
    '1080p': [1920, 1080],
    '1440p': [2560, 1440],
    '4k': [3840, 2160]
}

class Resize_Method(Enum):
    NONE = "none"
    RESIZE = "resize"
    CROP = "crop"

class Transformation(Enum):
    NONE = "none"
    WATER = "water"
    EMBOSS = "emboss"

class Color_Palette(Enum):
    PHOTO = "photo"
    PHOTO256 = "photo256"
    OMARCHY = "omarchy"

def validate_argv(argv):
    if len(argv) < 4:
        print("Invalid arguments")
        display_help_text()
        return False
    
    if argv[1] not in RESOLUTION:
        print("Invalid resolution")
        display_help_text()
        return False
    
    if argv[2] not in Resize_Method:
        print("Invalid resize method")
        display_help_text()
        return False
    
    if argv[3] not in Transformation:
        print("Invalid transformation type")
        display_help_text()
        return False
    
    if argv[4] not in Color_Palette:
        print("Invalid color palette")
        display_help_text()
        return False

    return True
 
def display_help_text():
    print("Photo 2 Background requires the following arguments")
    print("-----------------------------------------------------------------")
    print(f"1. Resolution: {json.dumps(list(RESOLUTION.keys()))}")
    print(f"2. Resize Method: {[item.value for item in Resize_Method]}")
    print(f"3. Transformation: {[item.value for item in Transformation]}")
    print(f"4. Color Palette: {[item.value for item in Color_Palette]}")
    print('\nExample: python3 src/main.py "1440p" "resize" "water" "photo" ')
    print("-----------------------------------------------------------------")
    
