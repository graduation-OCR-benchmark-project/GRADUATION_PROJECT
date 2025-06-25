import random
from PIL import Image, ImageDraw
import os
import json
import string

class Utils:
    """
    Utility functions for image processing, font selection, text rendering,
    background placement, and data loading/saving.
    These static methods are used throughout the synthetic data generation pipeline.
    """

    @staticmethod
    def get_random_background_image(background_folder, seed_index=None):
        """
        Selects a random image from the given background folder.

        Args:
            background_folder (str): Path to the folder containing background images.
            seed_index (int, optional): Seed for deterministic randomness.

        Returns:
            PIL.Image: Randomly selected background image.
        """
        if seed_index is not None:
            random.seed(seed_index)
        background_image = random.choice([
            Image.open(os.path.join(background_folder, f))
            for f in os.listdir(background_folder) if f.endswith(('jpg', 'png'))
        ])
        return background_image

    @staticmethod
    def get_random_font(fonts_folder, font_size_range, text_color_range, seed_index=None):
        """
        Selects a random font file, size, and text color.

        Args:
            fonts_folder (str): Folder containing .ttf or .otf fonts.
            font_size_range (tuple): Min and max font size.
            text_color_range (tuple): Range for RGB values.
            seed_index (int, optional): Seed for deterministic randomness.

        Returns:
            tuple: (font_path (str), font_size (int), text_color (tuple))
        """
        font_files = [f for f in os.listdir(fonts_folder) if f.endswith(('.ttf', '.otf'))]
        if not font_files:
            return None, None, None

        if seed_index is not None:
            random.seed(seed_index)
        font_path = os.path.join(fonts_folder, random.choice(font_files))

        font_size = random.randint(*font_size_range)
        if seed_index is not None:
            random.seed(seed_index)
        text_color = tuple(random.randint(low, high) for low, high in zip(*text_color_range))

        return font_path, font_size, text_color

    @staticmethod
    def get_text_size(lines, font):
        """
        Calculates the maximum width and total height required to render given text lines.

        Args:
            lines (list): List of text lines.
            font (ImageFont.FreeTypeFont): Font object.

        Returns:
            tuple: (total_width, total_height)
        """
        text_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        total_width = max(text_draw.textbbox((0, 0), line, font=font)[2] for line in lines)
        total_height = sum(text_draw.textbbox((0, 0), line, font=font)[3] for line in lines)
        return total_width, total_height

    @staticmethod
    def create_transparent_canvas(width, height):
        """
        Creates a transparent canvas of given width and height.

        Args:
            width (int): Width of the canvas.
            height (int): Height of the canvas.

        Returns:
            PIL.Image: A transparent RGBA image.
        """
        return Image.new('RGBA', (width, height), (0, 0, 0, 0))

    @staticmethod
    def draw_centered_text(draw, lines, font, text_color, canvas_size):
        """
        Draws text lines centered horizontally on a transparent canvas.

        Args:
            draw (ImageDraw.Draw): PIL drawing context.
            lines (list): List of strings to render.
            font (ImageFont.FreeTypeFont): Font to use.
            text_color (tuple): RGB or RGBA color.
            canvas_size (tuple): (width, height) of the canvas.
        """
        total_width, total_height = canvas_size
        text_y = 0
        for line in lines:
            width, height = draw.textbbox((0, 0), line, font=font)[2:]
            text_x = (total_width - width) // 2
            draw.text((text_x, text_y), line, font=font, fill=text_color)
            text_y += height

    @staticmethod
    def place_image_on_background(foreground_image, background_image, seed_index):
        """
        Places the foreground (text) image on a random position on the background image.

        Args:
            foreground_image (PIL.Image): Foreground image with transparency.
            background_image (PIL.Image): Background image.
            seed_index (int): Seed for reproducible random placement.

        Returns:
            PIL.Image: Cropped image containing foreground and relevant background.
        """
        fg_width, fg_height = foreground_image.size
        bg_width, bg_height = background_image.size

        if fg_width > bg_width or fg_height > bg_height:
            scale_factor = min(bg_width / fg_width, bg_height / fg_height)
            new_width = int(fg_width * scale_factor)
            new_height = int(fg_height * scale_factor)
            foreground_image = foreground_image.resize((new_width, new_height))
            fg_width, fg_height = foreground_image.size

        padding = 20
        random.seed(seed_index)
        position_x = random.randint(0, max(bg_width - fg_width, 0))
        position_y = random.randint(0, max(bg_height - fg_height, 0))

        background_copy = background_image.copy()
        background_copy.paste(foreground_image, (position_x, position_y),
                              foreground_image.convert("L").point(lambda x: 255 if x > 0 else 0))

        left = max(position_x - padding, 0)
        upper = max(position_y - padding, 0)
        right = min(position_x + fg_width + padding, bg_width)
        bottom = min(position_y + fg_height + padding, bg_height)

        cropped_image = background_copy.crop((left, upper, right, bottom))
        return cropped_image

    @staticmethod
    def save_to_json(dataset, json_output_path):
        """
        Appends or updates a JSON file with a dataset dictionary.

        Args:
            dataset (dict): New data to be written.
            json_output_path (str): Path to the target JSON file.
        """
        os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
        if os.path.exists(json_output_path):
            with open(json_output_path, 'r', encoding='utf-8') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        existing_data.update(dataset)
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
        print(f"✅ JSON updated: {json_output_path}")

    @staticmethod
    def load_texts_from_file_sentence(txt_path):
        """
        Loads sentence data line by line from a text file.

        Args:
            txt_path (str): Path to the .txt file.

        Returns:
            list: List of sentences (strings).
        """
        with open(txt_path, 'r', encoding='utf-8') as file:
            text_list = [line.strip() for line in file.readlines()]
        return text_list

    @staticmethod
    def load_texts_from_file_word(txt_path, filter_numbers=True):
        """
        Loads words from a text file. Optionally filters out purely numeric tokens.

        Args:
            txt_path (str): Path to the .txt file.
            filter_numbers (bool): Whether to exclude tokens that are all digits.

        Returns:
            list: List of words (strings).
        """
        with open(txt_path, 'r', encoding='utf-8') as f:
            texts = [text for line in f.readlines() for text in line.strip().split()]

        if filter_numbers:
            texts = [text for text in texts if not text.isdigit()]
        return texts

    @staticmethod
    def contains_turkish_special_characters(word):
        """
        Checks whether a word contains any Turkish-specific characters.

        Args:
            word (str): Input word.

        Returns:
            bool: True if the word contains Turkish characters, else False.
        """
        turkish_special_chars = 'çÇğĞıİöÖşŞüÜ'
        return any(char in turkish_special_chars for char in word)

    @staticmethod
    def words_length(word, min_len=3, max_len=None):
        """
        Cleans punctuation from a word and checks if its length is within given bounds.

        Args:
            word (str): The word to check.
            min_len (int): Minimum allowed length.
            max_len (int, optional): Maximum allowed length.

        Returns:
            bool: True if the word length is within bounds, else False.
        """
        cleaned_word = word.strip(string.punctuation)
        if max_len is not None:
            return min_len <= len(cleaned_word) < max_len
        else:
            return len(cleaned_word) >= min_len
