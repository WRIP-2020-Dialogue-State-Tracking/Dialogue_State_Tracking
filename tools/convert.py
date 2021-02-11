from numpy.core.fromnumeric import var
import typings
from database.variants import modifyDictionarywithVariants
from typing import List, Dict
import pandas as pd
import itertools
import re
import json
import constants
import re
from difflib import get_close_matches


def ireplace(old, repl, text):
    return re.sub("(?i)" + re.escape(old), lambda m: repl, text)

def fixAddress(
    dataset_of_domain: typings.dataframe,
    selected_domains: List[str]
):
    for index in dataset_of_domain.index:
        for _, dialog in enumerate(dataset_of_domain["log"][index]):
            dialog_act = dialog["dialog_act"]
            for domain in selected_domains: 
                for key in dialog_act:
                    remove_entries = []
                    if re.search(domain, key, flags=re.IGNORECASE):
                        address_exists = False
                        for info in dialog_act[key]:
                            if info[0] == "address":
                                address_exists = True
                                break
                        if not address_exists:
                            continue
                        address = ["address", ""]
                        for info in dialog_act[key]:
                            if info[0] == "address":
                                address[1] += info[1] + ", "
                                remove_entries.append(info)
                        for entry in remove_entries:
                            dialog_act[key].remove(entry)
                        address[1] = address[1][:-2]
                        dialog_act[key].append(address)

    print("Address Fixed.")


def modifyDialogAct(
    dialog_act,
    dictionary: Dict[str, str],
    modifiers,
    x_dict,
    variants: Dict[str, List[str]],
) -> str:

    error = False
    error_info = []
    modify_info = {}
    for key in dialog_act:
        if key:
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
                        or info[1] == "?"
                        or info[0] == "choice"
                        or info[0] == "ref"
                    ):
                        continue
                    else:
                        close_matches = get_close_matches(
                            (str(info[1])).lower(),
                            list(dictionary.keys()),
                            1,
                            0.001,
                        )
                        if len(close_matches) >= 1:
                            # prompt = str(
                            #     input(
                            #         "Map "
                            #         + close_matches[0]
                            #         + " to "
                            #         + (str(info[1]))
                            #         + " ? Y/N "
                            #     )
                            # )
                            # if prompt == "Y":
                            #     variants.setdefault(close_matches[0], []).append(
                            #         info[1]
                            #     )
                            #     print("Done!!")
                            #     dictionary[info[1]] = dictionary[close_matches[0]]
                            info[1] = dictionary[close_matches[0]]
                        #     with open(
                        #         "dictionary-final.json", "w", encoding="utf-8"
                        #     ) as f:
                        #         json.dump(dictionary, f, ensure_ascii=False)
                        #     with open(
                        #         "variants-extra.json", "w", encoding="utf-8"
                        #     ) as f:
                        #         json.dump(variants, f, ensure_ascii=False)
                        else:
                            error = True
                            error_info.append({info[0]: info[1]})
                            x_dict.setdefault(key, []).append(error_info)
                        # else:
                        # error = True
                        # error_info.append({info[0]: info[1]})
                        # x_dict.setdefault(key, []).append(error_info)
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
                str(df["mapping_{}_english".format(word)][index]).lower(): str(
                    df[word][index]
                )
                for index, word in itertools.product(
                    range(0, len(df.index)), file["ontology"]
                )
            }
        )
    dictionary = {**dictionary, **constants.car_dictionary, **constants.day_dictionary}
    dictionary = modifyDictionarywithVariants(
        dictionary,
        [
            "database/taxi-variants.json",
            "database/attraction-variants.json",
            "database/restaurant-variants.json",
            "database/variants-extra.json",
        ],
    )
    errors = dict()
    errors_by_modifier = dict()
    metadata_errors = dict()
    variants = dict()
    for index in dataset_of_domain.index:
        for ind, dialog in enumerate(dataset_of_domain["log"][index]):
            err, error_info, modify_info = modifyDialogAct(
                dialog["dialog_act"],
                dictionary,
                modifiers,
                errors_by_modifier,
                variants,
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

    with open("metadata-errors.json", "w", encoding="utf-8") as f:
        json.dump(metadata_errors, f, indent=2)
    with open("dictionary-final.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False)
    with open("variants-extra.json", "w", encoding="utf-8") as f:
        json.dump(variants, f, ensure_ascii=False)
    with open("modifier-errors.json", "w", encoding="utf-8") as f:
        json.dump(errors_by_modifier, f)
    with open("conversion-errors.json", "w", encoding="utf-8") as f:
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
