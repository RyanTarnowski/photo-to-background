from PIL import Image, ImageFilter, UnidentifiedImageError
import cv2
import numpy
import colorsys
import os

def process(file_path, target_size, trans_type, color_type):
    print(f"Processing file: {file_path}")

    #Check if the input_file is a valid file type
    image_obj = valid_input_file(file_path)

    #Resize to target_size
    if image_obj:
        resized_image_obj = resize_image(image_obj, target_size)

    #Apply transformations based on trans_type and color_type
    if resized_image_obj:
        transformed_image_obj = transform_image(resized_image_obj, trans_type)   

    #Save file to output
    if transformed_image_obj:
        save_image(file_path, transformed_image_obj)

def valid_input_file(file_path):
    try:
        img = Image.open(file_path)
        img.load() #required this inorder to pass the image obj between functions
        img.verify()
        print(f"Format: {img.format} Size: {img.size} Mode: {img.mode}")
        return img
    except (IOError, SyntaxError, UnidentifiedImageError) as e:
        print(f"Bad file (not an image or corrupted): {file_path} - {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred with file: {file_path} - {e}")
        return None

def resize_image(image_obj, target_size):
    try:
        size = (2560, 1440)
        resized_image_obj = image_obj.resize(size, Image.LANCZOS)
        print(f"Image resized to: {resized_image_obj.size}")
        return resized_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while resizing image - {e}")
        return None

def transform_image(image_obj, trans_type):
    try:
        # OpenCV uses BGR color order, Pillow uses RGB, so conversion is needed
        cv2_image_obj = cv2.cvtColor(numpy.array(image_obj), cv2.COLOR_RGB2BGR)

        # Define the kernel for dilate and erode
        kernel = numpy.ones((5, 5), numpy.uint8)

        # Apply all the transformations effects
        cv2_image_obj = cv2.dilate(cv2_image_obj, kernel, iterations=1)
        cv2_image_obj = cv2.erode(cv2_image_obj, kernel, iterations=1)
        cv2_image_obj = cv2.medianBlur(cv2_image_obj, 5)
        cv2_image_obj = cv2.stylization(cv2_image_obj, sigma_s=50, sigma_r=0.45)
        
        # Convert the cv2 back to pil and apply some extra effects
        transformed_image_obj = Image.fromarray(cv2.cvtColor(cv2_image_obj, cv2.COLOR_BGR2RGB))
        transformed_image_obj = transformed_image_obj.quantize(colors=256)
        transformed_image_obj = transformed_image_obj.convert("RGB")
        
        return transformed_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while transforming image - {e}")
        return None

def save_image(file_path, image_obj):
    try:
        filename = os.path.basename(file_path)
        basename, extension = os.path.splitext(filename)
        new_filename = f"{basename}_background{extension}"
        new_full_path = os.path.join("./output", new_filename)
        image_obj.save(new_full_path)
        print(f"Background image saved to: {new_full_path}")
    except Exception as e:
        print(f"An unexpected error occurred while saving image - {e}")

