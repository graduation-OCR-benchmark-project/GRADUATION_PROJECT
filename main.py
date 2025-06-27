from generator.scene.process_words_variations import WordVariationGenerator
from generator.scene.utils import Utils
from generator.scene.process_sentences_variations import SentenceVariationGenerator
from generator.scene.process_words import ProcessWords
config = {
    "fonts_folder": "data/roboto/",
    "background_folder": "data/background/background/",
    "output_folder": "data/outputs/sentence_variations/",
    "json_output_path": "data/annotations/sentence_variations.json",
    "font_size_range": (30, 60),
    "text_color_range": ((0, 0, 0), (255, 255, 255))
}

if __name__ == "__main__":
    words = Utils.load_texts_from_file_word("data/duzeltilmis_nutuk_cümleler.txt")
    generator = ProcessWords(config)
    generator.process(words)


#generator = SentenceGenerator() 
#process_sentences

#generator = ProcessWords() 
#process_words

#generator = WordVariationGenerator() -->düzeltildi 
#process_word_variations

#generator = SentenceVariationGenerator()
#process_sentence_variations 