import typings
from database.variants import modifyDictionarywithVariants
from typing import List, Dict
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
                        modify_info.update({info[1]: dictionary[str(info[1]).lower()]})
                    info[1] = dictionary[str(info[1]).lower()]
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


def modifyMetadata(metadata, dictionary, selected_domains):
    error = False
    error_info = []
    for domain in metadata:
        if domain in selected_domains:
            for key in metadata[domain]:
                for slot in metadata[domain][key]:
                    if slot == "booked":
                        for booked_index, booked_dict in enumerate(
                            metadata[domain][key][slot]
                        ):
                            skip = False
                            for booked_key in booked_dict:
                                values = booked_dict[booked_key]
                                if isinstance(values, list):
                                    for value in values:
                                        try:
                                            metadata[domain][key][slot][booked_index][
                                                booked_key
                                            ] = dictionary[str(value).lower()]
                                            skip = True
                                            break
                                        except:
                                            if (
                                                re.match("\d{2}:\d{2}", value)
                                                or value.isdigit()
                                                or re.match("\d{1}:\d{2}", value)
                                                or value == "none"
                                                or value == "dontcare"
                                            ):
                                                skip = True
                                                break
                                    if (
                                        skip == False
                                        and metadata[domain][key][slot] != []
                                    ):
                                        error = True
                                        error_info.append(
                                            {
                                                domain: {
                                                    key: {
                                                        slot: metadata[domain][key][
                                                            slot
                                                        ]
                                                    }
                                                }
                                            }
                                        )
                                else:
                                    value = values
                                    try:
                                        metadata[domain][key][slot][booked_index][
                                            booked_key
                                        ] = dictionary[str(value).lower()]
                                        break
                                    except:
                                        if (
                                            re.match("\d{2}:\d{2}", value)
                                            or value.isdigit()
                                            or re.match("\d{1}:\d{2}", value)
                                            or value == "none"
                                            or value == "dontcare"
                                            or booked_key == "reference"
                                        ):
                                            continue
                                        else:
                                            error = True
                                            error_info.append(
                                                {
                                                    domain: {
                                                        key: {
                                                            slot: metadata[domain][key][
                                                                slot
                                                            ]
                                                        }
                                                    }
                                                }
                                            )
                                            continue
                    else:
                        skip = False
                        for value in metadata[domain][key][slot]:
                            try:
                                metadata[domain][key][slot] = dictionary[
                                    str(value).lower()
                                ]
                                skip = True
                                break
                            except:
                                if (
                                    re.match("\d{2}:\d{2}", value)
                                    or value.isdigit()
                                    or re.match("\d{1}:\d{2}", value)
                                    or value == "none"
                                    or value == "dontcare"
                                ):
                                    skip = True
                                    break
                        if skip == False and metadata[domain][key][slot] != []:
                            error = True
                            error_info.append(
                                {domain: {key: {slot: metadata[domain][key][slot]}}}
                            )

    return error, error_info


def convertDialogs(
    dataset_of_domain: typings.dataframe,
    conversion_files: List[str],
    modifiers: List[Dict[str, str]],
    selected_domains: List[str],
):
    """Converts dialog acts and meta data of a Dataframe into another language

    Notes:

    - It takes in a Dataframe so on once run it can only convert one domain's Dataframe.
    - The Mapping xlsx file must have columns of the form  `word` <-> `mapping_word_english` for each `word` in `ontology`.

    Args:

      -  `dataset_of_domain` : Pandas Dataframe to be converted.
      -  `path_to_conversion_file` : Path to xlsx file containing mapping from english to other langugage.
      -  `ontology` : Array containing words in ontology. eg `departure`
      -  `modifiers` : Array containing fields to be modified e.g. `Taxi-Inform`.
      -  `selected_domains` : Array containing selected domains
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
    print(dictionary["Black Tesla".lower()])
    errors = dict()
    metadata_errors = dict()
    for index in dataset_of_domain.index:
        for ind, dialog in enumerate(dataset_of_domain["log"][index]):
            err, error_info, modify_info = modifyDialogAct(
                dialog["dialog_act"], dictionary, modifiers
            )
            dialog["text"] = convert_text(modify_info, dialog["text"])
            if err:
                errors.setdefault(index, []).append(error_info)

            if dialog["metadata"] == {}:
                continue
            metadata_err, metadata_error_info = modifyMetadata(
                dialog["metadata"], dictionary, selected_domains
            )
            if metadata_err:
                metadata_errors.setdefault(index, []).append(metadata_error_info)

    with open("metadata-errors.json", "w") as f:
        json.dump(metadata_errors, f, indent=2)
    with open("conversion-errors.json", "w") as f:
        json.dump(errors, f, indent=2)
    print(
        "Dialogs and text successfully converted.\n{} error found.".format(len(errors))
    )


def convert_text(modify_info, text):
    for k in modify_info.keys():
        try:
            text = ireplace(k, modify_info[k], text)
        except:
            continue
    return text


if __name__ == "__main__":
    pass
