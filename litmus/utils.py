###########
# imports #
###########
import json
import os


########
# read #
########
def read(path):
    """
    Returns the contents of a file as a string.

    Args:
        path (str): Path to the file.

    Returns:
        str: The file's contents.

    Raises:
        OSError: If the file cannot be opened.
    """
    with open(path) as f:
        return f.read()


#########
# write #
#########
def write(path, txt):
    """
    Writes a string to a file, creating any missing directories.

    Args:
        path (str): Path to write to.
        txt (str): Text to write.

    Raises:
        OSError: If the file cannot be written.
    """
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok = True)

    with open(path, "w") as f:
        f.write(txt)


#############
# read_json #
#############
def read_json(path):
    """
    Reads a JSON file.

    Args:
        path (str): Path to the file.

    Returns:
        object: The deserialized contents.

    Raises:
        OSError: If the file cannot be opened.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    return json.loads(read(path))


##############
# write_json #
##############
def write_json(path, obj):
    """
    Writes an object to a JSON file, creating any missing directories.

    Args:
        path (str): Path to write to.
        obj (object): JSON-serializable object.

    Raises:
        OSError: If the file cannot be written.
        TypeError: If the object is not JSON-serializable.
    """
    write(path, json.dumps(obj, indent = 4))
