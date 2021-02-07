# WRIP 2020 Tasks

## Task 1 Segregate MultiWOZ Dataset

### Steps to run:

- Install Dependencies

```
python3 -m pip install -r requirements.txt
```

- Download MultiWOZ 2.2 and MultiWOZ 2.1

- Convert to MultiWOZ 2.2 format

```
python convert_to_multiwoz_format.py --multiwoz21_data_dir=<multiwoz21_data_dir> --output_file=<output json file>

```

- Segregate Data _(takes path of data.json as input)_

```
python3 task1_segregate_multiwoz.py
```

- This will generate folders for each possible combination of domain **if that domain as atleast 1 file**. In each folder there are `json` files containing conversations and a `list.json` containing an array of file names. It also generates a stats.xlsx containing the stats of domains.

## Task 2 Convert to Hindi

### Steps to run

- Install Dependencies

```
python -m pip install -r requirements.txt
```

- Download MultiWOZ 2.2 and MultiWOZ 2.1

- Convert to MultiWOZ 2.2 format

```
python convert_to_multiwoz_format.py --multiwoz21_data_dir=<multiwoz21_data_dir> --output_file=<output json file>

```

- Convert Data _(takes path of data.json as input)_. This will dump all errors of domains into their json files.

```
python convert_hindi.py
```

# Task-3

We have performed the following subtasks:-

- Creating variants for all 3 domains
- Mapping the meta-data
- Mapping the dialogue text to hindi words took up from the dialogue act

A folder named `dataset` will be made in which the folder of all domains are there along with the folder `database_txt` . The folder `database_txt` contains the subfolders in which the files having only the goal and dialogue text mapped in hindi.

Run the command :

```
python3 convert_hindi.py
```
The prompt ask to input the path of the data file.

 `Some variants are still pending and not incorporated the replace in the text yet have some confusion in it.`