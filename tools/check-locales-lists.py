import os
import sys
import ruamel.yaml
from ruamel.yaml import YAML
from pathlib import Path

FILE_NAME = "*.lproj"
BLOCKZILLA_FOLDER = os.path.join(os.path.dirname(__file__), 'Blockzilla')
yaml = ruamel.yaml.YAML()

def get_current_locales_in_project(): 
    locales_files = []

    for file in os.listdir(BLOCKZILLA_FOLDER):
        if file.endswith(".lproj"):
            locales_files.append(file)

    # Save only the locale's name
    locales_files = [item.replace(".lproj", "") for item in locales_files]
    locales_list = sorted(locales_files)
    return locales_list

def get_locales_from_list_in_repo():
    with open('l10n-screenshots-config.yml') as f:
        my_dict = yaml.load(f)
        return my_dict["locales"]

def get_diff(first_list, second_list):
    second = set(second_list)
    return ([item for item in first_list if item not in second_list])

def modify_local_file(add_locales, remove_locales):
    with open('l10n-screenshots-config.yml') as f:
        my_dict = yaml.load(f)


    with open('l10n-screenshots-config.yml', 'w') as f:
        # remove
        my_dict["locales"] = [i for i in my_dict["locales"] if not any([e for e in remove_locales if e in i])]
        # add 
        my_dict["locales"].extend(add_locales)
        my_dict["locales"] = sorted(my_dict["locales"])

        yaml.indent(mapping=2, sequence=4, offset=6)
        yaml.dump(my_dict, f)

if __name__ == '__main__':
    locales_project_list = get_current_locales_in_project()
    locales_config_file_list = get_locales_from_list_in_repo()

    # if locales in diff are in 1 but not in 2 -> remove from config file
    remove_locales = get_diff(locales_config_file_list, locales_project_list)
    print(f"Remove:  {remove_locales}")

    # if locales in diff are in 2 but not in 1 -> add to config file
    add_locales = get_diff(locales_project_list, locales_config_file_list)
    print(f"Add: {add_locales}")

    modify_local_file(add_locales, remove_locales)
