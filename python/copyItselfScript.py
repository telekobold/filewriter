import shutil, os, time


def users_home_dir():
    """
    :returns: the user's home directory on Unix, Windows and MacOS systems
    """
    # return os.path.expanduser("~") # platform-independent user's home directory
    # return "/home/telekobold/TestVerzeichnis/OwnCloud-Test-Kopie" # For testing purposes
    return "/home/telekobold/TestVerzeichnis" # For testing purposes


def copy_itself(destination):
    """
    Makes a copy of this script and writes it to `destination`.
    
    :destination: the absolute file path where the copy should be placed.
    """
    copy_name = time.strftime("%Y-%m-%d_%H%M") + "_" + os.path.basename(__file__)
    shutil.copy(__file__, os.path.join(destination, copy_name))


if __name__ == "__main__":
    copy_itself(users_home_dir())
