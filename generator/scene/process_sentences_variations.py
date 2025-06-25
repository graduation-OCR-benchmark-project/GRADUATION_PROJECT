import os
from generator.scene.distortions import ImageDistorter
from utils import Utils

class SentenceVariationGenerator:
    """
    Generates multiple variations of sentence images based on specified distortion configs.
    Each variation is saved along with a JSON record.
    """

    def __init__(self, config):
        self.fonts_folder = config["fonts_folder"]
        self.background_folder = config["background_folder"]
        self.font_size_range = config["font_size_range"]
        self.text_color_range = config["text_color_range"]
        self.output_folder = config["output_folder"]
        self.json_output_path = config["json_output_path"]
        self.distorter = ImageDistorter()

    def generate_base_image(self, sentence, seed_index):
        font_path, font_size, text_color = Utils.get_random_font(
            self.fonts_folder, self.font_size_range, self.text_color_range, seed_index
        )
        if font_path is None:
            return None

        font = Utils.load_font(font_path, font_size)
        lines = sentence.split()
        width, height = Utils.get_text_size(lines, font)
        canvas = Utils.create_transparent_canvas(width, height)
        draw = Utils.create_draw_context(canvas)
        Utils.draw_centered_text(draw, lines, font, text_color, canvas.size)

        return canvas

    def apply_variation(self, image, variant, seed_index):
        if variant.get("blur"):
            image = self.distorter.apply_random_blur(image)
        if variant.get("noise"):
            image = self.distorter.apply_random_noise(image)
        if variant.get("res_reduce"):
            image = self.distorter.apply_random_resolution_reduce(image)
        if variant.get("rotate"):
            image = self.distorter.apply_random_rotation(image)
        return image

    def generate_and_save_variation(self, sentence, seed_index, variant):
        base_image = self.generate_base_image(sentence, seed_index)
        if base_image is None:
            return None

        distorted = self.apply_variation(base_image, variant, seed_index)
        background_image = Utils.get_random_background_image(self.background_folder, seed_index)
        composed = Utils.place_image_on_background(distorted, background_image, seed_index)

        name = variant["name"].lower()
        filename = f"sentence_{seed_index}_{name}.png"
        path = os.path.join(self.output_folder, filename)
        composed.save(path)

        json_record = {
            filename: {
                "ground_truth": sentence,
                "category": "sentences",
                "subcategory": name
            }
        }
        Utils.save_to_json(json_record, self.json_output_path)
        return filename

    def process(self, sentences, distortion_variants, start_index=0, max_images=100):
        os.makedirs(self.output_folder, exist_ok=True)

        for idx, sentence in enumerate(sentences):
            if idx >= max_images:
                break
            seed_index = start_index + idx

            for variant in distortion_variants:
                self.generate_and_save_variation(sentence, seed_index, variant)