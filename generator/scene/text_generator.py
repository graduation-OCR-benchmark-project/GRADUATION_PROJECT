from PIL import ImageDraw, ImageFont, Image
#from utils import Utils # get_text_size, create_transparent_canvas, draw_centered_text, get_random_font
#from distortions import ImageDistorter as Distortion
from generator.scene.utils import Utils
from generator.scene.distortions import ImageDistorter as Distortion


def text_prepare_sentence(text, font, max_width=2000, min_width=400, mode="single-line"):
    """
    Splits the sentence into lines based on max/min width constraints or keeps it single-line.
    """
    if mode == "single-line":
        words = text.split()
        limited_text = " ".join(words[:6])
        return [limited_text]

    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        bbox = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), test_line, font=font)

        if min_width <= bbox[2] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines


def prepare_text_image_sentence(text, font, max_width, min_width, mode):
    lines = text_prepare_sentence(text, font, max_width, min_width, mode)
    total_width, total_height = Utils.get_text_size(lines, font)
    text_image = Utils.create_transparent_canvas(total_width, total_height)
    draw = ImageDraw.Draw(text_image)
    return draw, text_image, lines, (total_width, total_height)


def generate_transparent_text_image_sentence(text, fonts_folder, font_size_range=(50, 60),
                                             text_color_range=((0, 0, 0), (255, 255, 255)),
                                             max_width=2000, min_width=400, mode="single-line",
                                             rotate=True, blur=True, seed_index=None):
    font_path, font_size, text_color = Utils.get_random_font(fonts_folder, font_size_range, text_color_range, seed_index)
    if not font_path:
        print("ERROR: Font file not found.")
        return None

    font = ImageFont.truetype(font_path, font_size)
    draw, text_image, lines, text_size = prepare_text_image_sentence(text, font, max_width, min_width, mode)
    Utils.draw_centered_text(draw, lines, font, text_color, text_size)

    if rotate:
        text_image = Distortion.apply_random_rotation(text_image)
    if blur:
        text_image = Distortion.apply_random_blur(text_image)

    return text_image


def text_prepare_word(text, font, max_width=600):
    words = text.split()
    processed_words = []

    for word in words:
        bbox = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), word, font=font)
        if bbox[2] <= max_width:
            processed_words.append(word)
        else:
            processed_words.append(word)

    return processed_words


def prepare_text_image_word(text, font):
    lines = text_prepare_word(text, font)
    total_width, total_height = Utils.get_text_size(lines, font)
    text_image = Utils.create_transparent_canvas(total_width, total_height)
    draw = ImageDraw.Draw(text_image)
    return draw, text_image, lines, (total_width, total_height)


def generate_transparent_text_image_word(text, fonts_folder=None, font_size_range=None,
                                         text_color_range=None, max_width=2000,
                                         rotate=True, blur=True, seed_index=None):
    font_path, font_size, text_color = Utils.get_random_font(
        fonts_folder, font_size_range, text_color_range, seed_index=seed_index
    )
    if not font_path:
        print("ERROR: Font file not found.")
        return None

    font = ImageFont.truetype(font_path, font_size)
    draw, text_image, lines, text_size = prepare_text_image_word(text, font)
    Utils.draw_centered_text(draw, lines, font, text_color, text_size)

    if rotate:
        text_image = Distortion.apply_random_rotation(text_image)
    if blur:
        text_image = Distortion.apply_random_blur(text_image)

    return text_image
