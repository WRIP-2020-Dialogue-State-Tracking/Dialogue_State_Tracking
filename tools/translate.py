from pygoogletranslation import Translator
import pandas as pd
import typings
import json
import os

def translateDialogs(
    dataset: typings.dataset,
):
    for key in dataset:
        
        os.makedirs('dataset', exist_ok=True)
        
        # if (key == "__status" or key =='__invalid'):
        #     continue
        if (key != '_attraction_restaurant_taxi'):
            continue
        
        dataset_of_domain = dataset[key].T
        os.makedirs('dataset/dataset_txt/{}/hindi/'.format(key), exist_ok=True)
        print('dataset/dataset_txt/{}/hindi/'.format(key))
        translator = Translator()
        for index in dataset_of_domain.index:
            if index < "PMUL2361.json":
                continue
            text = []
            logs = []
            for dialog in dataset_of_domain["log"][index]:
                text.append(dialog["text"])
            
            translations = translator.translate(text, src='en', dest='hi')
            for translation in translations:
                translated_text = {
                    "text": translation.text
                }
                logs.append(translated_text)
            
            final_dict = {
                index: {
                    "log": logs
                }
            }
            with open("dataset/dataset_txt/{}/hindi/hindi_{}_txt.json".format(key, index.split('.')[0]), 'w', encoding='utf-8') as file:
                json.dump(final_dict, file, ensure_ascii=False, indent=4)