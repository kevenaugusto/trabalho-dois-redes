import os

def delete(path_content):
    try:
        os.remove(path_content)
    except IsADirectoryError:
        delete_folder(path_content)

def delete_folder(path_content):
    try:
        os.rmdir(path_content)
    except NotADirectoryError:
        delete(path_content)
    except OSError:
        for content in os.listdir(path_content):
            delete(path_content / content)
        delete(path_content)