from PIL import Image, ImageFilter, UnidentifiedImageError
from globals import RESOLUTION, Transformation, Resize_Method, Color_Palette
import cv2
import numpy
import colorsys
import os
import math

def process(file_path, resolution, resize_method, transformation, color_palette):
    print(f"Processing file: {file_path}")

    #Check if the input_file is a valid file type
    image_obj = valid_input_file(file_path)

    #Resize to target_size
    if image_obj:
        match resize_method:
            case Resize_Method.RESIZE.value:
                resized_image_obj = resize_image(image_obj, resolution)
            case Resize_Method.CROP.value:
                resized_image_obj = crop_image(image_obj, resolution)
            case _:
                resized_image_obj = image_obj

    #Apply transformation
    if resized_image_obj:
        match transformation:
            case Transformation.WATER.value:
                transformed_image_obj = transform_water(resized_image_obj)
            case Transformation.EMBOSS.value:
                transformed_image_obj = transform_emboss(resized_image_obj)
            case _:
                transformed_image_obj = resized_image_obj

    #Apply color palette
    if transformed_image_obj:
        match color_palette:
            case Color_Palette.PHOTO256.value:
                transformed_image_obj = color_palette_original256(transformed_image_obj)
            case Color_Palette.OMARCHY.value:
                transformed_image_obj = color_palette_omarchy(transformed_image_obj)

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

def resize_image(image_obj, resolution):
    try:
        size = RESOLUTION[resolution]
        resized_image_obj = image_obj.resize(size, Image.LANCZOS)
        print(f"Image resized to: {resized_image_obj.size}")
        return resized_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while resizing image - {e}")
        return None

def crop_image(image_obj, resolution):
    try:
        size = RESOLUTION[resolution]

        width, height = image_obj.size
        new_width, new_height = size

        #Return the original image if the image can't be cropped
        if width < new_width or height < new_height:
            print("Image size smaller than target size")
            return image_obj

        left = int(math.ceil((width - new_width) / 2))
        top = int(math.ceil((height - new_height) / 2))
        right = int(width - math.floor((width - new_width) / 2))
        bottom = int(height - math.floor((height - new_height) / 2))

        resized_image_obj = image_obj.crop((left, top, right, bottom))
        print(f"Image cropped to: {resized_image_obj.size}")
        return resized_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while cropping image - {e}")
        return None

def transform_water(image_obj):
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
        
        return transformed_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while transforming image - {e}")
        return None

def transform_emboss(image_obj):
    try:
        transformed_image_obj = image_obj
        #TODO: Implement image emboss 
        return transformed_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while transforming image - {e}")
        return None

def color_palette_original256(image_obj):
    try:
        transformed_image_obj = image_obj.quantize(colors=256)
        transformed_image_obj = transformed_image_obj.convert("RGB")
        
        return transformed_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while appling color palette - {e}")
        return None

def color_palette_omarchy(image_obj):
    try:
        #TODO: Read colors from omarchy style config and apply them to the image
        transformed_image_obj = image_obj.quantize(colors=256)
        transformed_image_obj = transformed_image_obj.convert("RGB")
        
        return transformed_image_obj
    except Exception as e:
        print(f"An unexpected error occurred while appling color palette - {e}")
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

