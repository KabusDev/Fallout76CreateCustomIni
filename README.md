![](https://staticdelivery.nexusmods.com/mods/2590/images/314/314-1558456148-714359290.png)

# Fallout76CreateCustomIni
Simple script to create a Fallout76Custom.ini for .ba2 mods installed

## Rathinosk
This is a fork of GrimTech's fork this python INI file generator (<a href="https://www.nexusmods.com/fallout76/mods/314" target="_blank">Nexus Link</a>) modified for my own purposes.

## Instructions
  * Make a backup of your current Fallout76Custom.ini if you have one
  * Copy the .py or .exe file to your fallout76/data directory
  * Run the file from the command line or vortex using:
    * for the .py: `py createCustomIni.py`
    * for the .exe: `createCustomIni.exe`
  * Verify the Fallout76Custom.ini looks correct the first few times... maybe....

## Options
  * __-h__ __--help__ Show the help message
  * __--datafolder__ Specify fallout76\'s data folder location (Default: current directory)
  * __--inifolder__ Specify the folder where Fallout76Custom.ini lives (Default: C:\Users\[*current_user*]\Documents\My Games\Fallout 76)
  * __--inifilename__ Specify the filename for the ini (Default: Fallout76Custom.ini)
  * __--runasadmin__ Run the program as administrator, will ask for permission
  * __--copyinicontents__ Copy a file's contents in to your .ini

## Info
Script compiled with pyinstaller via Visual Studio...
