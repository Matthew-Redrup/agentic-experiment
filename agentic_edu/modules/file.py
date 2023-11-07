import json
import yaml
import logging


def write_file(fname, content):
    """
    Write content to a file.

    Args:
        fname (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open(fname, "w") as f:
        f.write(content)


def write_json_file(fname, json_str: str):
    """
    Write a JSON string to a file.

    Args:
        fname (str): The name of the file to write to.
        json_str (str): The JSON string to write to the file.

    Raises:
        json.decoder.JSONDecodeError: If the JSON string is not valid JSON.
    """
    # convert ' to "
    json_str = json_str.replace("'", '"')

    # Convert the string to a Python object
    data = json.loads(json_str)

    # Write the Python object to a file as JSON
    with open(fname, "w") as f:
        json.dump(data, f, indent=4)


def write_yaml_file(fname, json_str: str):
    """
    Convert a JSON string to YAML and write it to a file.

    Args:
        fname (str): The name of the file to write to.
        json_str (str): The JSON string to convert to YAML and write to the file.

    Raises:
        json.decoder.JSONDecodeError: If the JSON string is not valid JSON.
    """
    logging.debug("Write_yml_file() %s", json_str)

    # Try to replace single quotes with double quotes for JSON
    cleaned_json_str = json_str.replace("'", '"')

    logging.debug("cleaned_json_str: %s", cleaned_json_str)

    # Safely convert the JSON string to a Python object
    try:
        data = json.loads(cleaned_json_str)
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        raise

    # Write the Python object to a file as YAML
    with open(fname, "w") as f:
        yaml.dump(data, f)
