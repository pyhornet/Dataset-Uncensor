### What it does:
This Python script implements a JSON line filtering mechanism that excludes specific words and phrases, effectively removing political bias or refusal statements from JSON-based datasets. The script's functionality can be easily extended by modifying the `words_to_match` list, which contains the predefined terms for filtering. This code is intended for educational purposes.

### How to use:
To utilize this script, simply execute the following command: `python uncensor.py dataset-example.json`. This will generate a new JSON file named **`{base_name}-{current_time}-UNCENSORED.json`**. `{base_name}` represents the name of your input JSON file. `{current_time}` represents the current system date and time, ensuring that each output file remains distinct.
