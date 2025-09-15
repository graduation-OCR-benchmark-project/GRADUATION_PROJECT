# Turkish Synthetic Word Generator

Generates synthetic Turkish word images for OCR training using TRDG.

## About
This project uses the [TextRecognitionDataGenerator (TRDG)](https://github.com/Belval/TextRecognitionDataGenerator) by Belval to create synthetic Turkish text images with optimized parameters for OCR model training.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add font files to `fonts/` folder
3. Add Turkish words to `sample_data/balanced_turkish_words.txt`
4. Run the notebook

## Parameters
- Generates 230 images by default
- Uses blur, skew, and noise effects
- Supports multiple font styles and backgrounds
## Note
This project requires pip version < 24.1 due to TRDG dependency issues.
