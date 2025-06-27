#calculate.py, cer_wer.py, cer_wer2.py
#bütün kodlar burada ekli zaten 
#buradaki kod da çalışıyor 
import json 
import editdistance
from jiwer import wer
import string

with open("bosluk_kaldirilmis.json","r",encoding="utf-8") as f:
    data = json.load(f)

#boşluklar hariç CER hesaplama 
def calculate_cer_bosluk_haric(ground_truth, prediction):
    gt = ground_truth.replace(" ", "")
    pred = prediction.replace(" ", "")
    if not gt:
        return 1.0  # ground_truth boşsa hata oranı 1
    return editdistance.eval(gt, pred) / len(gt)

#boşluk ve noktalama kaldırılarak
def clean_text(text):
    return text.translate(str.maketrans('', '', string.whitespace + string.punctuation))

def calculate_cer_bosluk_noktalama_haric(ground_truth, prediction):
    gt = clean_text(ground_truth)
    pred = clean_text(prediction)
    if not gt:
        return 1.0
    return editdistance.eval(gt, pred) / len(gt)

def calculate_cer(prediction, ground_truth):
    return editdistance.eval(prediction, ground_truth) / max(1, len(ground_truth))


def loop_for_img(output_name,cer_calculate): #output name must be written as "name.json"
    for image_name, image_info in data.items(): 
        ground_truth = image_info.get("ground_truth", "").strip()
        
        for model_name, model_info in image_info.get("models", {}).items():
            prediction = model_info.get("prediction", "").strip()

            # Boş tahminleri atla
            if not prediction or not ground_truth:
                model_info["cer"] = None
                model_info["wer"] = None
                continue

            # CER ve WER hesapla
            cer_value = cer_calculate(ground_truth, prediction)
            wer_value = wer(ground_truth, prediction)

            # Sonuçları yaz
            model_info["cer"] = round(cer_value, 4)
            model_info["wer"] = round(wer_value, 4)

    # Güncellenmiş veriyi dosyaya kaydet
    with open(output_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"CER WER caşculated for {output_name}")

def determine_category(category):
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


def json_type_editing(): #only run it once is enough 
    meta_data = data.pop("_meta",None)
    for filename, content in data.items():
        ground_truth = content.get("ground_truth")
        if ground_truth is None:
            print(f"Warning: 'ground_truth' key is missing for {filename}. Skipping this entry.")
            continue  

        new_content = {
            "ground_truth": ground_truth,
            "type": content.get("subcategory"), 
            "category": determine_category(content.get("category")), 
            "subcategory": content.get("category"),  
            "models": content.get("models")  
        }
        determine_category(content.get("category"))
        data[filename] = new_content

    if meta_data is not None:
        data["_meta"] = meta_data
    print("json editin over")

    with open("bosluk_kaldirlmis_update.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


#loop_for_img("deneme.json",calculate_cer_bosluk_haric) #bu böyle çalışıyor 
#data.json zaten ilk oluşturulan boş dosya 
json_type_editing()