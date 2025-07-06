#kod çalışıyor fakat dosya adlarını farklı verirsen yeniden 
#deneme3 gibi dosyalar oluşturuyor 
#bu da process.py dosyasında farklı isimler verdiğin için

#çalışıyor. kodları gene okuyarak içselleştir 
#kodun tamamı bitmedi eksik kısımlar var, calculate_cer_bosluk_haric,
#calculate_cer_bosluk_noktalama_haric gibi fonksiyonlar var ve genel olarak bir iyileştirme 
# yapılabilir.

import json
from utils import load_json, save_json 
import editdistance
from jiwer import wer
import string
#from preprocessing_json import 
class CerWerCalculator:
    """In this module, takes json file and calculates the Character Error Rate (CER) and Word Error Rate (WER) for each model's predictions against the ground truth.
    It updates the JSON structure with these metrics and saves the modified data back to a file.
    """
    def __init__(self, file_path, output_path, json_data=None, cer_calculate=None):
        self.file_path = file_path
        self.output_path = output_path
        self.json_data = json_data
        self.meta_data = None
        self.cer_calculate = cer_calculate or self.calculate_cer #cer_calculate zaten 
                                                        #self.calculate_cer
    def load_json(self):
        """Load JSON data from the specified file path and extract meta data if available.
        This method internally caalls the utils.load_json function to read the JSON file.
        """
        self.json_data, self.meta_data = load_json(self.file_path)

    def save_json(self):
        """Save the updated JSON data to the specified output path.
        This method uses the utils.save_json function to write the JSON data back to a file."""
        save_json(self.json_data, self.output_path)
        print(f"JSON data saved to {self.output_path}")

    def calculate_cer(self, prediction, ground_truth):
        """Calculate the Character Error Rate (CER) between the prediction and ground truth.
        CER is defined as the Levenshtein distance between the two strings divided by the length of the ground truth.
        Parameters:
            prediction (str): The predicted text.
            ground_truth (str): The ground truth text.
        Returns:
            float: The calculated CER value.
        """
        return editdistance.eval(prediction, ground_truth) / max(1, len(ground_truth))
    
    def clean_text(self, text):
        """Remove spaces and punctuation from the prediction or ground truth text.
        This method is used to preprocess the text before calculating CER."""
        return text.translate(str.maketrans('', '', string.whitespace + string.punctuation))

    def calculate_cer_without_spaces_and_punctuation(self,prediction, ground_truth):
        """Calculate the Character Error Rate (CER) without considering spaces and punctuation.
        parameters:
            prediction (str): The predicted text. taken from the json file. 
            ground_truth (str): The ground truth text.taken from the json file.
        Returns:
            float: The calculated CER value.
        """
        gt = self.clean_text(ground_truth)
        pred = self.clean_text(prediction)
        if not gt:
            return 1.0
        return editdistance.eval(pred, gt) / max(1, len(gt)) 


    def calculate_cer_without_spaces(self,ground_truth, prediction):
        """Calculate the Character Error Rate (CER) without considering spaces.
        parameters:
            prediction (str): The predicted text. taken from the json file. 
            ground_truth (str): The ground truth text.taken from the json file.
            Returns:
                float: The calculated CER value.
        """

        gt = ground_truth.replace(" ", "")
        pred = prediction.replace(" ", "")
        if not gt:
            return 1.0
        return editdistance.eval(pred, gt) / max(1, len(gt))
        

    def calculate_for_all_models(self, cer_function=None):
        """
        Calculate CER and WER for all models in the loaded JSON data.

        Iterates through each image's predictions and ground truth, calculates
        the Character Error Rate (CER) and Word Error Rate (WER), and updates
        the JSON structure with these values. The CER can optionally be calculated
        using a custom function (e.g., ignoring spaces or punctuation).
        The '_meta' section, if present, is ignored during CER and WER calculation, but remains intact in the JSON data.

        Parameters:
            cer_function (callable, optional): 
                A custom CER calculation function that takes (prediction, ground_truth) as arguments.
                If not provided, the default `self.cer_calculate` method is used.

        Returns:
            None
                Adds 
                The method updates the JSON data in place and does not return any value.
        """


        cer_function = cer_function or self.cer_calculate
        for image_name, image_info in self.json_data.items():
            if image_name == "_meta":
                continue

            ground_truth = image_info.get("ground_truth", "").strip()

            for model_name, model_info in image_info.get("models", {}).items():
                prediction = model_info.get("prediction", "").strip()

                if not prediction or not ground_truth:
                    model_info["cer"] = None
                    model_info["wer"] = None
                    continue
                cer_value = cer_function(ground_truth, prediction)
                wer_value = wer(ground_truth, prediction)

                model_info["cer"] = round(cer_value, 4)
                model_info["wer"] = round(wer_value, 4)

    def run(self,cer_function=None): #if cer_function is not given it will work as defaul which is self.cer_calculate
        """Execute the whole processing pipeline:
        1. Load the JSON data from the specified file.
        2. Calculate CER and WER for all models using the provided or default CER function.
        3. Save the updated JSON data to the output file.
        Parameters:
            cer_function (callable, optional): 
                A custom CER calculation function that takes (prediction, ground_truth) as arguments.
                If not provided, the default `self.cer_calculate` method is used.
        Returns:
            None
                The method updates the JSON data in place and saves it to the output file.
        """
        self.load_json()
        self.calculate_for_all_models(cer_function)  #buradan dolayı default çalışıyor şu an burayı değiştirirsen değişir 
        self.save_json() 
