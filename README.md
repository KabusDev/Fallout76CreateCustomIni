![Fallout76CreateCustomIni](https://staticdelivery.nexusmods.com/mods/2590/images/314/314-1558456148-714359290.png)

# Fallout76CreateCustomIni

Simple script to create a `Fallout76Custom.ini` for `.ba2` mods installed in Fallout 76.

## Authors
Kabus for OneDrive and refactoring, more convenient modification for mod load order based on resource_map.json

Forked from Rathinosk, originally based on GrimTech's fork of a Python INI file generator. Find the original script at this [Nexus Link](https://www.nexusmods.com/fallout76/mods/314).

## Features

- Automatically detects and includes installed `.ba2` mod files.
- Supports custom data folder and INI file location.
- Can be run with administrative privileges if needed.
- Allows copying content from an existing INI file.
- Customizable through a JSON config file.

## Requirements

- Python 3.x
- Fallout 76 installed
- Mods in `.ba2` format

## Instructions

1. **Backup**: Make a backup of your current `Fallout76Custom.ini` if you have one.
2. **Copy**: Copy the `.py` or `.exe` file to your Fallout 76 data directory.
3. **Run**:
    - For the `.py` file: Run `py createCustomIni.py` from the command line or Vortex.
    - For the `.exe` file: Run `createCustomIni.exe`.
4. **Verify**: Check that the generated `Fallout76Custom.ini` looks correct, especially the first few times.

## Options

- `-h, --help`: Show the help message.
- `--datafolder`: Specify Fallout 76's data folder location (Default: current directory).
- `--inifolder`: Specify the folder where `Fallout76Custom.ini` lives (Default: `C:\Users\[current_user]\Documents\My Games\Fallout 76`).
- `--inifilename`: Specify the filename for the INI (Default: `Fallout76Custom.ini`).
- `--runasadmin`: Run the program as administrator, will ask for permission.
- `--copyinicontents`: Copy a file's contents into your `.ini`.
- `--configfile`: Specify the JSON config file for `RESOURCE_MAP` (Default: `resource_map.json`).

### Example Usage

```sh
python createCustomIni.py --datafolder "C:\Fallout76\Data" --inifolder "C:\Users\YourName\Documents\My Games\Fallout 76" --inifilename "Fallout76Custom.ini" --configfile "resource_map.json"
```

### Running as Administrator

If Fallout 76 is installed in a UAC-protected location, you may need to run the script with administrative privileges:

```sh
python createCustomIni.py --runasadmin
```

## Configuration

The script relies on a JSON configuration file (`resource_map.json`) to map resource files. The JSON structure should look like this:

```json
[
  {
    "filename": "sResourceArchive2List",
    "mods": ["mod1.ba2", "mod2.ba2"],
    "default_mods": ["basegame1.ba2"],
    "found_mods": []
  },
  ...
]
```

- `filename`: The INI file entry for the resource list.
- `mods`: The list of mod filenames that should be checked.
- `default_mods`: The list of default mod filenames.
- `found_mods`: This list will be populated by the script with found mod filenames.

## Troubleshooting

- **DuplicateSectionError**: If a section already exists in the INI file, the script will merge entries and override based on the last occurrence in the file.
- **File Not Found**: Ensure the paths provided in the command-line arguments are correct and the files exist.

## License

This project is licensed under the MIT License.