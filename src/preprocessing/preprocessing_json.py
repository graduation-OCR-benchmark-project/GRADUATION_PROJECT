
import json
from utils import load_json, save_json
class JsonCategoryProcessor:
    """
    In this module, works for changing json file structure for better organization in subcategories.
    """
    def __init__(self,  file_path, output_path,json_data=None):
        self.file_path = file_path
        self.output_path = output_path
        self.json_data = json_data
        self.meta_data = None

    def load_json(self):
        self.json_data, self._meta_data = load_json(self.file_path)

    def save_json(self):
        save_json(self.json_data, self.output_path)
        print(f"JSON data saved to {self.output_path}")
    @staticmethod
    def determine_category(category):
        """Determine the category based on the input category (more generalizing).
        subcategory turned into type (text type) for better understanding.
        category turned into subcategory (more specialized).
        Parameters:
            category (str): The input category to be classified.
        Returns:
            str: The determined category type. (more generalizing)
            str: The determined subcategory (more specialized).
            str: The determined text-type as type (additional info).
        
        """
        
        input_subcategory = category
        if input_subcategory in ["word", "sentences"]:
            return "context_dependent_errors"
        elif input_subcategory in ["blur", "noisy", "rotated", "clean", "low_resolution"]:
            return "distortion_type"
        elif input_subcategory in ["turkish", "non_turkish"]:
            return "turkish_character_confusion"
        elif input_subcategory in ["short_words", "long_words"]:
            return "word_length_effects"
        else:
            return "unknown"
    
    def process_json(self):
        """Process the loaded JSON data to restructure it according to the specified format.
        Adds meta data back if it exists,
        checks for ground_truth key in each entry, if None, skips that entry,
        and gives warning message. Converts the structure of each entry to include
        with using the determine_category method.
        Updates:
            creates a new JSON structure (as dictionary) with the following 
            output path, respectively input path. 

        """
        for filename, content in self.json_data.items():
            ground_truth = content.get("ground_truth")
            if ground_truth is None:
                print(f"Warning: 'ground_truth' key is missing for {filename}. Skipping this entry.")
                continue  

            new_content = {
                "ground_truth": ground_truth,
                "type": content.get("subcategory"), 
                "category": self.determine_category(content.get("category")), 
                "subcategory": content.get("category"),  
                "models": content.get("models")  
            }
            self.json_data[filename] = new_content

        if self._meta_data is not None:
            self.json_data["_meta"] = self._meta_data


    def run(self):
        """Executes the full JSON processing workflow.
        1.Loads the JSON data from input path
        2.Process the JSON data to reorganize its structure
        3.Saves the processed JSON data to the output path"""
        self.load_json()
        self.process_json()
        self.save_json()
        return self.output_path
        


