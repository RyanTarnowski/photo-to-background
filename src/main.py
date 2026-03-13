from processing import process
import os

def main():
    print("Photo to background")
    print("Processing photos in input ...")

    for file in os.listdir("./input"):
        file_path = os.path.join("./input", file)
        if os.path.isfile(file_path):
            process(file_path, 1440, 1, 1)
    
    print("Processing complete")
    return
   
if __name__ == "__main__":
    main()
