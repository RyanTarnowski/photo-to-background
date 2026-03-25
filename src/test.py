import unittest
from globals import GREEN, RED, RESET, display_help_text, validate_argv
from processing import save_image, valid_input_file, resize_image, crop_image, transform_water, transform_colorize, color_palette_photo256, color_palette_photo3, color_palette_omarchy
from omarchy import get_omarchy_theme_colors
from contextlib import redirect_stdout
from io import StringIO
from PIL import Image
import os

class TestPhotoToBackground(unittest.TestCase):
    def setUp(self):
        # Cleanup any leftover test files from previous runs
        if os.path.exists("./assets/tests/Castle1_background.jpg"):
            os.remove("./assets/tests/Castle1_background.jpg")

    def test_validate_argv(self):
        bad_argv = []
        bad_arg_rez = ['src/main.py', '1000', 'crop', 'none', 'photo3']
        bad_arg_resize = ['src/main.py', '1440p', 'grow', 'none', 'photo3']
        bad_arg_trans = ['src/main.py', '1440p', 'crop', 'mono', 'photo3']
        bad_arg_color = ['src/main.py', '1440p', 'crop', 'none', 'photo4']
        good_argv = ['src/main.py', '1440p', 'crop', 'none', 'photo3']
        buffer = StringIO()

        with redirect_stdout(buffer):
            self.assertEqual(validate_argv(bad_argv), False, "Invalid argv")
            self.assertEqual(buffer.getvalue(), f"{RED}Invalid arguments{RESET}\n")
            buffer.seek(0)
            buffer.truncate(0)
            
            self.assertEqual(validate_argv(bad_arg_rez), False, "Invalid resolution arg")
            self.assertEqual(buffer.getvalue(), f"{RED}Invalid resolution{RESET}\n")
            buffer.seek(0)
            buffer.truncate(0)
            
            self.assertEqual(validate_argv(bad_arg_resize), False, "Invalid resize arg")
            self.assertEqual(buffer.getvalue(), f"{RED}Invalid resize method{RESET}\n")
            buffer.seek(0)
            buffer.truncate(0)
            
            self.assertEqual(validate_argv(bad_arg_trans), False, "Invalid transformation arg")
            self.assertEqual(buffer.getvalue(), f"{RED}Invalid transformation type{RESET}\n")
            buffer.seek(0)
            buffer.truncate(0)

            self.assertEqual(validate_argv(bad_arg_color), False, "Invalid color arg")
            self.assertEqual(buffer.getvalue(), f"{RED}Invalid color palette{RESET}\n")
            buffer.seek(0)
            buffer.truncate(0)

            self.assertEqual(validate_argv(good_argv), True, "Valid argv")
            self.assertEqual(buffer.getvalue(), "")
        
        buffer.close()

    def test_display_help_text(self):
        help_text= f"""
Photo 2 Background requires the following arguments
-----------------------------------------------------------------
1. Resolution: ["1080p", "1440p", "4k"]
2. Resize Method: ['none', 'resize', 'crop']
3. Transformation: ['none', 'water']
4. Color Palette: ['none', 'photo256', 'photo3', 'omarchy']

Example: {GREEN}python3 src/main.py "1440p" "resize" "water" "photo256"{RESET}
-----------------------------------------------------------------
"""
        buffer = StringIO()

        with redirect_stdout(buffer):
            display_help_text()
            self.assertEqual(buffer.getvalue(), help_text, "Display help text")
        buffer.close()

    def test_valid_input_file(self):
        buffer = StringIO()

        with redirect_stdout(buffer):
            self.assertEqual(valid_input_file("./assets/tests/notaphoto.txt"), None, "Not a valid image file")
            self.assertEqual(buffer.getvalue(), f"Bad file (not an image or corrupted): ./assets/tests/notaphoto.txt - cannot identify image file './assets/tests/notaphoto.txt'\n") 
            buffer.seek(0)
            buffer.truncate(0)

        with redirect_stdout(buffer):
            self.assertEqual(valid_input_file("./assets/tests/Castle1.jpg"), Image.open("./assets/tests/Castle1.jpg"), "Valid image file")
            self.assertEqual(buffer.getvalue(), "Format: JPEG Size: (3024, 4032) Mode: RGB\n") 
        
        buffer.close()

    def test_resize_image(self):
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        buffer = StringIO()

        with redirect_stdout(buffer):
            resized_image_obj = resize_image(test_image_obj, "1080p")
            self.assertEqual(resized_image_obj.size, (1920, 1080), "Resize Image")
            self.assertEqual(buffer.getvalue(), "Image resized to: (1920, 1080)\n")        

        test_image_obj.close()
        buffer.close()

    def test_crop_image(self):
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        buffer = StringIO()

        with redirect_stdout(buffer):
            cropped_image_obj = crop_image(test_image_obj, "1440p")
            self.assertEqual(cropped_image_obj.size, (2560, 1440), "Crop Image")
            self.assertEqual(buffer.getvalue(), "Image cropped to: (2560, 1440)\n") 
        
        test_image_obj.close()
        buffer.close()

    #def test_transform_water(self):
    #    test_image_obj = Image.open("./assets/tests/Castle1.jpg")
    #    buffer = StringIO()

    #    with redirect_stdout(buffer):
    #        transform_water(test_image_obj)
    #        self.assertEqual(buffer.getvalue(), "Image transformed to watercolor\n", "Transform to watercolor")

    #   test_image_obj.close()
    #    buffer.close()

    def test_transform_colorize(self):
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        buffer = StringIO()
        test_color_palette = [[0,0,0], [75, 75, 75], [255, 255, 255]]
        max_colors = test_image_obj.width * test_image_obj.height
        test_pre_colors = test_image_obj.getcolors(max_colors)

        with redirect_stdout(buffer):
            test_image_obj = transform_colorize(test_image_obj, test_color_palette)
            test_post_colors = test_image_obj.getcolors(max_colors)
            self.assertNotEqual(test_pre_colors, test_post_colors, "Transform colorize")
            self.assertEqual(buffer.getvalue(), f"Image colorized with: {test_color_palette} \n")

        test_image_obj.close()
        buffer.close()

    def test_color_palette_photo256(self):
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        max_colors = test_image_obj.width * test_image_obj.height
        test_image_obj = color_palette_photo256(test_image_obj)

        self.assertEqual(len(test_image_obj.getcolors(max_colors)), 256, "256 color palette")
        test_image_obj.close()

    def test_color_palette_photo3(self):
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        test_colors = color_palette_photo3(test_image_obj)
        test_expected_colors = [(255, 255, 255), (0, 0, 0), (125, 102, 58)]
        
        self.assertEqual(len(test_colors), 3, "3 color palette")
        self.assertEqual(test_colors, test_expected_colors, "3 color palette")
        test_image_obj.close()
        
    def test_color_palette_omarchy(self):
        current_directory = os.getcwd()
        test_omarchy_theme = current_directory + "/assets/tests/colors.toml"
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        test_colors = color_palette_omarchy(test_image_obj, test_omarchy_theme)
        test_expected_colors = [(158, 206, 106), (26, 27, 38), (50, 52, 74)]
        
        self.assertEqual(len(test_colors), 3, "3 color omarchy palette")
        self.assertEqual(test_colors, test_expected_colors, "3 color omarchy palette")
        test_image_obj.close()

    def test_save_image(self):
        current_directory = os.getcwd()
        test_image_obj = Image.open("./assets/tests/Castle1.jpg")
        buffer = StringIO()

        with redirect_stdout(buffer):
            save_image(current_directory + '/assets/tests/Castle1.jpg', './assets/tests' , test_image_obj)
            self.assertTrue(os.path.isfile('./output/Castle1_background.jpg'), "Save image")
            self.assertEqual(buffer.getvalue(), f"Background image saved to: ./assets/tests/Castle1_background.jpg \n\n")

        test_image_obj.close()
        buffer.close()

    #def test_get_omarchy_theme_colors(self):





