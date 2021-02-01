import typings
from database.variants import modifyDictionarywithVariants
from typing import List
import pandas as pd
import itertools
import re
import json
import constants
import re


def ireplace(old, repl, text):
    return re.sub("(?i)" + re.escape(old), lambda m: repl, text)


def modifyDialogAct(dialog_act, dictionary, modifiers) -> str:
    error = False
    error_info = []
    modify_info = {}
    for key in dialog_act:
        if key in modifiers:
            for info in dialog_act[key]:
                try:
                    if str(info[1]).lower() in dictionary.keys():
                        modify_info.update({info[1]: dictionary[info[1]]})
                    info[1] = dictionary[info[1]]
                except:
                    if (
                        re.match("\d{2}:\d{2}", info[1])
                        or info[1].isdigit()
                        or re.match("\d{1}:\d{2}", info[1])
                        or info[0] == "none"
                        or info[1] == "dontcare"
                    ):
                        continue
                    else:
                        error = True
                        error_info.append({info[0]: info[1]})
                        continue
    return error, error_info, modify_info


def convertDialogActs(
    dataset_of_domain: typings.dataframe,
    conversion_files: List[str],
    modifiers: List[str],
):
    """Converts a dialog act of a Dataframe into another language

    Notes:

    - It takes in a Dataframe so on once run it can only convert one domain's Dataframe.
    - The Mapping xlsx file must have columns of the form  `word` <-> `mapping_word_english` for each `word` in `ontology`.

    Args:

      -  `dataset_of_domain` : Pandas Dataframe to be converted.
      -  `path_to_conversion_file` : Path to xlsx file containing mapping from english to other langugage.
      -  `ontology` : Array containing words in ontology. eg `departure`
      -  `modifiers` : Array containing fields to be modified e.g. `Taxi-Inform`.
    """
    dictionary = dict()
    for file in conversion_files:
        df = pd.read_excel(file["name"], engine="openpyxl")
        dictionary.update(
            {
                str(df["mapping_{}_english".format(word)][index]).lower(): df[word][
                    index
                ]
                for index, word in itertools.product(
                    range(0, len(df.index)), file["ontology"]
                )
            }
        )
    dictionary = {**dictionary, **constants.car_dictionary, **constants.day_dictionary}
    dictionary = modifyDictionarywithVariants(
        dictionary, ["database/taxi-variants.json", "database/attraction-variants.json"]
    )
    errors = dict()
    for index in dataset_of_domain.index:
        for ind, dialog in enumerate(dataset_of_domain["log"][index]):
            err, error_info, modify_info = modifyDialogAct(
                dialog["dialog_act"], dictionary, modifiers
            )
            dialog["text"] = convert_text(modify_info, dialog["text"])
            if err:
                errors.setdefault(index, []).append(error_info)
    with open("conversion-errors.json", "w") as f:
        json.dump(errors, f, indent=2)
    print(
        "Dialogs and text successfully converted.\n{} error found.".format(len(errors))
    )


def convert_text(modify_info, text):
    for k in modify_info.keys():
        if text.find(k) != -1:
            try:
                text = ireplace(k, modify_info[k], text)
            except:
                continue
    return text


if __name__ == "__main__":
    pass
