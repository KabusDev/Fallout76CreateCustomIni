""" This module creates a Fallout76Custom.ini file from the installed mods in the data directory """

import argparse
import ctypes
import json
import os
import sys
from configparser import ConfigParser
from os import walk

# Default paths and filenames
MODS_DIR = '.'
FILENAME = 'Fallout76Custom.ini'
INI_FOLDER = os.path.expanduser("~") + ("\\OneDrive\\Documents\\My Games\\Fallout 76" if os.path.exists(os.path.expanduser("~") + "\\OneDrive") else "\\Documents\\My Games\\Fallout 76")

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Automatically create the Fallout76Custom.ini file for you.')
parser.add_argument('--datafolder', default=MODS_DIR, help='Specify Fallout 76\'s data folder location (default: current directory)')
parser.add_argument('--inifolder', default=INI_FOLDER, help='Specify the folder where Fallout76Custom.ini should be placed')
parser.add_argument('--inifilename', default=FILENAME, help='Specify the filename for the INI (default: Fallout76Custom.ini)')
parser.add_argument('--runasadmin', action="store_true", help='Run as an admin. Use when Fallout 76 is installed in a UAC location.')
parser.add_argument('--configfile', default='resource_map.json', help='Specify the JSON config file for RESOURCE_MAP')
args = parser.parse_args()

# Assign arguments to variables
MODS_DIR = args.datafolder
FILENAME = args.inifilename
INI_FOLDER = args.inifolder
IS_ADMIN = args.runasadmin
CONFIG_FILE = args.configfile

# Load the RESOURCE_MAP from the JSON file
with open(CONFIG_FILE, 'r') as file:
    RESOURCE_MAP = json.load(file)

SR_2LIST_INDEX = 3

def update_archive_section(ini_path, resource_map):
    # Read original lines
    original_lines = []
    if os.path.exists(ini_path):
        with open(ini_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()

    # Use ConfigParser to get existing structure for easier updating
    config = ConfigParser()
    config.optionxform = str
    config.read(ini_path, encoding='utf-8')

    if 'Archive' not in config.sections():
        config.add_section('Archive')

    for RESOURCE in resource_map:
        RESOURCE['found_mods'].clear()

    for _, _, filenames in walk(MODS_DIR):
        for file in filenames:
            if file[:10] != 'SeventySix' and file.lower().endswith('.ba2'):
                found = False
                for RESOURCE in resource_map:
                    if file in RESOURCE['mods']:
                        if file not in RESOURCE['found_mods']:
                            RESOURCE['found_mods'].append(file)
                        found = True
                        break
                if not found:
                    resource_map[SR_2LIST_INDEX]['found_mods'].append(file)

    for RESOURCE in resource_map:
        if RESOURCE['found_mods']:
            found = frozenset(RESOURCE['found_mods'])
            mod_list = ', '.join(m for m in RESOURCE['mods'] if m in found)
            diff_list = ', '.join(i for i in found if i not in RESOURCE['mods'])
            default_mods = ', '.join(RESOURCE['default_mods'])

            full_list = ', '.join(filter(None, [default_mods, mod_list, diff_list]))

            if RESOURCE['filename'] == 'sResourceArchive2List' and 'ChatMod.ba2' not in full_list:
                full_list = ', '.join(filter(None, [full_list, 'ChatMod.ba2']))

            config.set('Archive', RESOURCE['filename'], full_list)

    # Merge new archive values into original lines
    archive_section = False
    output_lines = []
    for line in original_lines:
        stripped = line.strip()
        if stripped.startswith("[Archive]"):
            archive_section = True
            output_lines.append(line)
            continue
        if archive_section:
            if stripped.startswith("[") and stripped.endswith("]") and stripped != "[Archive]":
                archive_section = False
        if archive_section and "=" in line:
            key = line.split("=", 1)[0].strip()
            if key in config["Archive"]:
                line = f"{key} = {config['Archive'][key]}\n"
        output_lines.append(line)

    # If for some reason we don't have anythign in the archive section fo the ini??
    if '[Archive]' in ''.join(output_lines):
        archive_start = next(i for i, line in enumerate(output_lines) if line.strip() == '[Archive]')
        existing_keys = set()
        for i in range(archive_start + 1, len(output_lines)):
            stripped = output_lines[i].strip()
            if stripped.startswith('[') and stripped.endswith(']'):
                break
            if '=' in stripped:
                existing_keys.add(stripped.split('=', 1)[0].strip())

        insert_pos = archive_start + 1
        for key, value in config['Archive'].items():
            if key not in existing_keys:
                output_lines.insert(insert_pos, f"{key} = {value}\n")
                insert_pos += 1

    # If Archive section was missing entirely, append it
    if '[Archive]' not in ''.join(original_lines):
        output_lines.append('[Archive]\n')
        for key, value in config['Archive'].items():
            output_lines.append(f"{key} = {value}\n")

    with open(ini_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)


if IS_ADMIN:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
else:
    # Create any missing folders
    if not os.path.exists(INI_FOLDER):
        os.makedirs(INI_FOLDER)

    ini_path = os.path.join(INI_FOLDER, FILENAME)

    # Update the [Archive] section of the INI file
    update_archive_section(ini_path, RESOURCE_MAP)
