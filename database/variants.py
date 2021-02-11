import json


def modifyDictionarywithVariants(dictionary, variant_files):
    variants = dict()
    for file in variant_files:
        with open(file) as json_file:
            variants.update(dict(json.load(json_file)))
    for key in variants.keys():
        for variant in variants[key]:
            try:
                dictionary[variant.lower()] = dictionary[key].lower()
            except:
                continue
    return dictionary