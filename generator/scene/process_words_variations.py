import os
from generator.scene.distortions import ImageDistorter
from generator.scene.utils import Utils
from generator.scene.text_generator import generate_transparent_text_image_word
class WordVariationGenerator:
    """
    Generates word images with multiple distortion variants.
    Each variant is saved in its respective folder with a JSON record.
    """

    def __init__(self, config):
        self.fonts_folder = config["fonts_folder"]
        self.background_folder = config["background_folder"]
        self.output_folder = config["output_folder"]
        self.json_output_path = config["json_output_path"]
        self.font_size_range = config["font_size_range"]
        self.text_color_range = config.get("text_color_range", ((0, 0, 0), (255, 255, 255)))
        self.max_width = config.get("max_width", 2000)
        self.noise_level_range = config.get("noise_level_range", (0.1, 0.2))
        self.scale_factor_range = config.get("scale_factor_range", (0.2, 0.3))
        self.blur_radius_range = config.get("blur_radius_range", (2, 3))

    def filter_words(self, words, filter_type=None, length=None):
        if filter_type == 'turkish':
            words = [w for w in words if Utils.contains_turkish_special_characters(w)]
        elif filter_type == 'non_turkish':
            words = [w for w in words if not Utils.contains_turkish_special_characters(w)]

        if length == "short":
            words = [w for w in words if Utils.words_length(w, min_len=3, max_len=10)]
        elif length == "long":
            words = [w for w in words if Utils.words_length(w, min_len=10)]
        elif length == "mixed":
            words = [w for w in words if Utils.words_length(w, min_len=3)]
        return words

    def generate_variants(self):
        return [
            {"name": "blur", "blur": True, "rotate": False, "noise": False, "res_reduce": False},
            {"name": "rotate", "blur": False, "rotate": True, "noise": False, "res_reduce": False},
            {"name": "noise", "blur": False, "rotate": False, "noise": True, "res_reduce": False},
            {"name": "res_reduce", "blur": False, "rotate": False, "noise": False, "res_reduce": True},
            {
                "name": "all", "blur": True, "rotate": True, "noise": True, "res_reduce": True,
                "params": {
                    "noise_level_range": (0.05, 0.1),
                    "scale_factor_range": (0.7, 0.9),
                    "blur_radius_range": (1, 2)
                }
            }
        ]

    def generate_and_save_variation(self, word, idx, variant, seed_index):
        # Varyanta özel parametreleri al
        params = variant.get("params", {})
        noise_range = params.get("noise_level_range", self.noise_level_range)
        res_range = params.get("scale_factor_range", self.scale_factor_range)
        blur_range = params.get("blur_radius_range", self.blur_radius_range)

        
        base_img = generate_transparent_text_image_word(
            text=word,
            fonts_folder=self.fonts_folder,
            font_size_range=self.font_size_range,
            text_color_range=self.text_color_range,
            max_width=self.max_width,
            rotate=False,
            blur=False,
            seed_index=seed_index
        )

        image = base_img.copy()
        if variant["rotate"]:
            image = ImageDistorter().apply_random_rotation(image)
        if variant["blur"]:
            image = ImageDistorter().apply_random_blur(image,blur_radius_range=blur_range ) #blur_radius_range=blur_range

        background_image = Utils.get_random_background_image(self.background_folder, seed_index)
        final_image = Utils.place_image_on_background(image, background_image, seed_index)

        if variant["noise"]:
            final_image = ImageDistorter().apply_random_noise(final_image, noise_level_range=noise_range)
        if variant["res_reduce"]:
            final_image = ImageDistorter().apply_random_resolution_reduce(final_image, scale_factor_range=res_range)

        variant_output_path = os.path.join(self.output_folder, variant["name"])
        os.makedirs(variant_output_path, exist_ok=True)

        filename = f"{variant['name']}_{idx + 1}.png"
        save_path = os.path.join(variant_output_path, filename)
        final_image.save(save_path)

        return filename, variant["name"]

    def process(self, words, filter_type=None, length=None, start_index=0, last_index=None, max_images=1050):
        os.makedirs(self.output_folder, exist_ok=True)
        dataset = {}

        words = self.filter_words(words, filter_type, length)
        selected_words = words[start_index:last_index] if last_index else words[start_index:start_index + max_images]

        variants = self.generate_variants()

        for variant in variants:
            print(f"\n🔧 Generating images for variant: {variant['name']}")
            for idx, word in enumerate(selected_words):
                seed_index = start_index + idx
                filename, variant_name = self.generate_and_save_variation(word, idx, variant, seed_index)
                dataset[filename] = {
                    "filename": filename,
                    "ocr_analysis": {
                        "text": word,
                        "variant": variant_name
                    }
                }

        if self.json_output_path:
            Utils.save_to_json(dataset, self.json_output_path)
        print("\n✅ All variants generated successfully.")
