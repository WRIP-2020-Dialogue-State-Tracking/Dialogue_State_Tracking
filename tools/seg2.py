import typings
from typing import List
import pandas as pd
import itertools
import re
import json
import constants


def modifyDialogAct2(dialog_act, modifiers) -> str:
    info = []
    for key in dialog_act:
        if key in modifiers:
            for info in dialog_act[key]:
                info.append({info[0]: info[1]})
    return info


def convertDialogActs2(
    dataset_of_domain: typings.dataframe,
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

    _info = dict()
    for index in dataset_of_domain.index:
        for ind, dialog in enumerate(dataset_of_domain["log"][index]):
            info = modifyDialogAct2(dialog["dialog_act"], modifiers)
            if info:
                _info.setdefault(index, []).append(info)
    with open("info_{}.json".format(modifiers[0]), "w") as f:
        json.dump(_info, f, indent=2)
    print("Dialogs successfully converted.\n{} error found.".format(len(_info)))


if __name__ == "__main__":
    pass
