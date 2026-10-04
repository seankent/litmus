###########
# imports #
###########
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
    """
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok = True)

    with open(path, "w") as f:
        f.write(txt)
