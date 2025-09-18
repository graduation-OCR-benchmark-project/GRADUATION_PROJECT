# Turkish Synthetic Word Generator

Generates synthetic Turkish word images for OCR training using TRDG.

## About
This project uses the [TextRecognitionDataGenerator (TRDG)](https://github.com/Belval/TextRecognitionDataGenerator) by Belval to create synthetic Turkish text images.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add font files to `fonts/` folder
3. Add Turkish words to `sample_data/turkish_words.txt`
4. Run the notebook

The `sample_data/` folder contains sample Turkish words and sentences for testing. 
For production use, replace with your own Turkish word corpus.

## Note
This project requires pip version < 24.1 due to TRDG dependency issues.
