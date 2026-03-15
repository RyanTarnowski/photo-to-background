from processing import process
from globals import validate_argv, display_help_text
import sys
import os

def main():
    #TODO: Use pyfiglet for the title
    print("Photo to background")
    if validate_argv(sys.argv): 
        print("Processing photos in input ...")
        
        for file in os.listdir("./input"):
            file_path = os.path.join("./input", file)
            if os.path.isfile(file_path):
                process(file_path=file_path, 
                        resolution=sys.argv[1], 
                        resize_method=sys.argv[2], 
                        transformation=sys.argv[3], 
                        color_palette=sys.argv[4])
        
        print("Processing complete")
    return

if __name__ == "__main__":
    main()
