import json
import re

JSON_PATH = "./keywords.json"
def classify_text_by_regex(input_text: str) -> str:
    """
    Classify the input text based on regex patterns stored in a JSON file.

    Args:
        input_text (str): The text to be classified.

    Returns:
        str: The first matching parent category from the JSON, or an empty string if none match.
    """
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        pattern_dict = json.load(file)

    for category, patterns in pattern_dict.items():
        for pattern in patterns:
            if re.search(pattern, input_text['text']):
                return category  # Return immediately on the first match

    return ""  # No match found
