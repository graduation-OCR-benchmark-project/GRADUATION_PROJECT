import os
import random
from generator.scene.distortions import ImageDistorter
from generator.scene.utils import Utils

class ProcessWords: #WordGenerator isime hala karar vermedim ikisi de olabilir 
    """
    Handles the generation of synthetic word images, including filtering,
    rendering, distortion, background placement, and JSON annotation saving.
    """

    def __init__(self, config):
        self.fonts_folder = config["fonts_folder"]
        self.background_folder = config["background_folder"]
        self.font_size_range = config["font_size_range"]
        self.text_color_range = config["text_color_range"]
        self.output_folder = config["output_folder"]
        self.json_output_path = config["json_output_path"]
        self.distorter = ImageDistorter(
            blur_radius_range=config.get("blur_radius_range", (1, 2)),
            noise_level_range=config.get("noise_level_range", (0.1, 0.15)),
            scale_factor_range=config.get("scale_factor_range", (0.7, 0.9)),
            rotation_angle_range=config.get("rotation_angle_range", (-15, 15))
        )

    def filter_words(self, words, mode):
        if mode == "non_turkish":
            words = [w for w in words if not Utils.contains_turkish_special_characters(w)]
        elif mode == "turkish":
            words = [w for w in words if Utils.contains_turkish_special_characters(w)]
        elif mode == "short":
            words = [w for w in words if Utils.words_length(w, min_len=3, max_len=10)]
        elif mode == "long":
            words = [w for w in words if Utils.words_length(w, min_len=10)]
        elif mode == "mixed":
            words = [w for w in words if Utils.words_length(w, min_len=3)]
        return words

    def generate_single_word_image(self, word, seed_index):
        font_path, font_size, text_color = Utils.get_random_font(
            self.fonts_folder, self.font_size_range, self.text_color_range, seed_index
        )
        if font_path is None:
            return None

        font = Utils.load_font(font_path, font_size)
        lines = [word]
        width, height = Utils.get_text_size(lines, font)
        canvas = Utils.create_transparent_canvas(width, height)
        draw = Utils.create_draw_context(canvas)
        Utils.draw_centered_text(draw, lines, font, text_color, canvas.size)

        return canvas

    def generate_and_save(self, word, seed_index, apply_blur=True,
                          apply_noise=True, apply_resolution_reduce=True, apply_rotation=True):
        text_image = self.generate_single_word_image(word, seed_index)
        if text_image is None:
            return None

        if apply_blur:
            text_image = self.distorter.apply_random_blur(text_image)
        if apply_noise:
            text_image = self.distorter.apply_random_noise(text_image)
        if apply_resolution_reduce:
            text_image = self.distorter.apply_random_resolution_reduce(text_image)
        if apply_rotation:
            text_image = self.distorter.apply_random_rotation(text_image)

        background_image = Utils.get_random_background_image(self.background_folder, seed_index)
        composed_image = Utils.place_image_on_background(text_image, background_image, seed_index)

        filename = f"word_{seed_index}.png"
        image_path = os.path.join(self.output_folder, filename)
        composed_image.save(image_path)

        json_record = {
            filename: {
                "ground_truth": word,
                "category": "words",
                "subcategory": "standard"
            }
        }
        Utils.save_to_json(json_record, self.json_output_path)
        return filename

    def process(self, words, mode="non_turkish", start_index=0, max_images=100):
        os.makedirs(self.output_folder, exist_ok=True)
        words = self.filter_words(words, mode)

        for idx, word in enumerate(words):
            if idx >= max_images:
                break
            seed_index = start_index + idx
            self.generate_and_save(word, seed_index)  # default distortions apply
