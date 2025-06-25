from generator.scene.process_words_variations import WordVariationGenerator
from generator.scene.utils import Utils

config = {
    "fonts_folder": "data/roboto/",
    "background_folder": "data/background/background/",
    "output_folder": "data/outputs/words/",
    "json_output_path": "data/annotations/words.json",
    "font_size_range": (30, 60),
    "text_color_range": ((0, 0, 0), (255, 255, 255))
}

if __name__ == "__main__":
    words = Utils.load_texts_from_file_word("data/duzeltilmis_nutuk_cümleler.txt")
    generator = WordVariationGenerator(config)
    generator.process(words)
