import json


def create_dir_if_not_exists(directory):
    """
    Create a directory if it does not exist.

    :param directory: Directory path to create
    """
    import os

    if not os.path.exists(directory):
        os.makedirs(directory)


def read_json_file(filename):
    """
    Read a JSON file and return its content.

    :param filename: Name of the JSON file
    :return: Parsed JSON content
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_json_file(data, filename):
    """
    Save a list of dictionaries to a JSON file.

    :param data: List of dictionaries to save
    :param filename: Name of the JSON file
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
