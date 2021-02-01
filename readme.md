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
python task2_convert_hindi.py
```
