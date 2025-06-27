#buradaki temel üzerine diğer bütün grafik kısımlarını da yazarak yapabilirsin 
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

with open("changed.json", "r", encoding="utf-8") as f:
    data = json.load(f)
data.pop("_meta", None)

rows = []
for image_name, image_info in data.items():
    gt = image_info.get("ground_truth")
    typee=image_info.get("type")
    cat = image_info.get("category")
    subcat = image_info.get("subcategory")
    models = image_info.get("models")
    for model_name, model_info in models.items():
        row = {
            "image": image_name,
            "ground_truth": gt,
            "type":typee,
            "category": cat,
            "subcategory": subcat,
            "model": model_name,
            "prediction": model_info["prediction"],
            "cer": model_info["cer"],
            "wer": model_info["wer"]
        }
        rows.append(row)
df = pd.DataFrame(rows)

# CER ve WER 1'in üzerindekileri 1 e eşit yapıyor
df["cer"] = df["cer"].clip(upper=1.0).fillna(1.0)
df["wer"] = df["wer"].clip(upper=1.0).fillna(1.0)



def model_performance_type_comparison():
    grouped = df.groupby(["model", "type"])["cer"].mean().unstack(fill_value=1) #none dönen değerleri de 1 olarak dolduruyor 
    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(12, 6), width=0.8,
                      color=["mediumseagreen", "orange", "mediumpurple"])
    plt.ylabel("CER (%)")
    plt.title("Model Performance Comparison Type - CER")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_comparison_type_CER.png", dpi=300)
    plt.show()

model_performance_type_comparison()

def model_performance_category_comparison():
    grouped = df.groupby(["model", "category"])["cer"].mean().unstack(fill_value=1) #none dönen değerleri de 1 olarak dolduruyor 
    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(12, 6), width=0.8,
                      color=["steelblue", "tomato", "goldenrod", "slateblue"])
    plt.ylabel("CER (%)")
    plt.title("Model Performance Comparison Category - CER")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_comparison_category_CER.png", dpi=300)
    plt.show()

model_performance_category_comparison()

def model_performance_context_dependent_compraison():
    # Sadece 'context_dependent_errors' kategorisindeki veriler
    df_filter = df[df["category"] == "context_dependent_errors"] #buradaki kısmı düzelttim şimdi çalışıyor 
    # Model ve subcategory bazında ortalama CER hesapla
    grouped = df_filter.groupby(["model", "subcategory"])["cer"].mean().unstack(fill_value=1)

    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(14, 7), width=0.8,
                    color = ["cadetblue", "lightsteelblue"])

    plt.ylabel("CER")
    plt.title("Model Performance on Context-Dependent Subcategories (CER)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Subcategory", loc="upper right")
    plt.tight_layout()
    plt.savefig("context_dependent_subcategory_comparison_CER.png", dpi=300)
    plt.show()

model_performance_context_dependent_compraison()

def model_performance_distortion_type_compraison(): #distortion_type
    # Sadece 'context_dependent_errors' kategorisindeki veriler
    df_filter = df[df["category"] == "distortion_type"]

    # Model ve subcategory bazında ortalama CER hesapla
    grouped = df_filter.groupby(["model", "subcategory"])["cer"].mean().unstack(fill_value=1)

    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(14, 7), width=0.8,
                    color=["mediumseagreen", "darkorange", "mediumpurple", "crimson", "teal"])

    plt.ylabel("CER")
    plt.title("Model Performance on Distortion-Types Subcategories (CER)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Subcategory", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_distortion_type_compraison.png", dpi=300)
    plt.show()

model_performance_distortion_type_compraison()

def model_performance_turkish_character_confusion_compraison(): #turkish_character_confusion
    # Sadece 'context_dependent_errors' kategorisindeki veriler
    df_filter = df[df["category"] == "turkish_character_confusion"]

    # Model ve subcategory bazında ortalama CER hesapla
    grouped = df_filter.groupby(["model", "subcategory"])["cer"].mean().unstack(fill_value=1)

    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(14, 7), width=0.8,
                                            color = ["peru", "khaki"])

    plt.ylabel("CER")
    plt.title("Model Performance on Turkish Character Confusion Subcategories (CER)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Subcategory", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_turkish_character_confusion_compraison.png", dpi=300)
    plt.show()

model_performance_turkish_character_confusion_compraison()


#bu kısmı çalıştırarak dene 
def model_performance_word_length_effects_compraison(): #word_length_effects
    # Sadece 'context_dependent_errors' kategorisindeki veriler
    df_filter = df[df["category"] == "word_length_effects"]

    # Model ve subcategory bazında ortalama CER hesapla
    grouped = df_filter.groupby(["model", "subcategory"])["cer"].mean().unstack(fill_value=1)

    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(14, 7), width=0.8,
                                            color = ["royalblue", "indianred"])
    plt.ylabel("CER")
    plt.title("Model Performance on Word Length Effects Subcategories (CER)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Subcategory", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_word_length_effects_compraison.png", dpi=300)
    plt.show()

model_performance_word_length_effects_compraison()



def model_performance_general_cer():
    grouped = df.groupby(["model"])["cer"].mean() 
    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(12, 6), width=0.8,
                                                color = ["darkslategray"])
    plt.ylabel("CER (%)")
    plt.title("Model Performance Comparison Category - CER")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_general_CER.png", dpi=300)
    plt.show()
model_performance_general_cer()

def model_performance_sentence_only_wer(): #word_length_effects
    # Sadece 'context_dependent_errors' kategorisindeki veriler
    df_filter = df[df["subcategory"] == "sentences"]
    # Model ve subcategory bazında ortalama CER hesapla
    grouped = df_filter.groupby(["model", "subcategory"])["wer"].mean().unstack(fill_value=1) 

    # Grafik çizimi
    ax = grouped.plot(kind="bar", figsize=(14, 7), width=0.8,
                                                    color = ["plum"])

    plt.ylabel("CER")
    plt.title("Model Performance on Sentences (WER)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Subcategory", loc="upper right")
    plt.tight_layout()
    plt.savefig("model_performance_sentences_wer.png", dpi=300)
    plt.show()

model_performance_sentence_only_wer()