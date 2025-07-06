"""process.py
This script serves as the main entry point for preprocessing JSON data and calculating Character Error Rate (CER) and Word Error Rate (WER).
It imports necessary classes from other modules and runs the preprocessing and CER/WER calculations.
Steps performed:
1.Preprocess categories and save to a new JSON file (preprocessing_json.py).
2.Calculate CER and WER for the preprocessed data and save results to specified JSON files (cer_wer_calculation.py).
(in this step CER values are calculated in three different ways:
    - with spaces and punctuation
    - without spaces
    - without spaces and punctuation

Outputs:
- json/preprocessed.json: Preprocessed JSON with updated categories.
- json/cer_wer_calculated.json: Standard CER and WER.
- json/cer_wer_calculated_without_spaces.json: CER ignoring spaces.
- json/cer_wer_calculated_without_spaces_and_punctuation.json: CER ignoring spaces and punctuation.
"""


from preprocessing_json import JsonCategoryProcessor
from cer_wer_calculation import CerWerCalculator
#usage 
if __name__ =="__main__":
    processor = JsonCategoryProcessor( "json/converted_data.json",
                                      "json/preprocessed.json")
    preprocessed_path = processor.run()
    calculator = CerWerCalculator(preprocessed_path, 
                                  "json/cer_wer_calculated.json")
    calculator.run(cer_function=calculator.calculate_cer)

    
    
    calculator_without_spaces = CerWerCalculator(preprocessed_path,
                                                 "json/cer_wer_calculated_without_spaces.json",)
    calculator_without_spaces.run(cer_function=calculator.calculate_cer_without_spaces)


    calculator_without_spaces_and_punctuation = CerWerCalculator(preprocessed_path,
                                                 "json/cer_wer_calculated_without_spaces_and_punctuation.json")
    calculator_without_spaces_and_punctuation.run(cer_function=calculator.calculate_cer_without_spaces_and_punctuation)


