# MFM Command Setup

1. Download the [current code of MFM](https://github.com/ansonl/mfm/archive/refs/heads/master.zip) and extract the entire folder to a location such as your user home directory `~`. 

2. Replace the UPPERCASE of the below sample MFM command text as described further below.

```sh
"PYTHONPATH/python3.exe" "SCRIPTPATH/mfm_cmd.py" -c "OPTIONSPATH/options.json" -t "TOOLCHANGEPATH/toolchange.gcode" --disable 0;
```

Command structure:

  - `PYTHONPATH` is the location of your [Python](https://python.org) installation. This is the folder that the Python executable is in. You may need to change `python3.exe` to match your Python name.

  - `SCRIPTPATH` is the location of all the files in the `src` directory.

  - `-c` – Options JSON
    - `OPTIONSPATH` is the location of your Options JSON file. Change `options.json` to the options file name.

  - `-t` – Toolchange G-code
    - `TOOLCHANGEPATH` is the location of your Minimal Toolchange G-code file. Change `toolchange.json` to the toolchange filename.

  - `-le` *optional* – Line ending style
    - `AUTO` – Auto detect
    - `WINDOWS` – `\r\n`
    - `UNIX` – `\n`

  - `-o` *optional* – Output Print G-code location. 
    - **Omit this parameter if using MFM as an intergrated Post-processing Script within the slicer.** This is the location of the output printing G-code. MFM will overwrite the input file if no output file is specified. 

  - `--disable` *optional* – Quick toggle for enable/disable MFM post processing without needing to clear the entire slicer Post-processing scripts option. 
    - `0` – MFM is enabled
    - `1` – MFM is disabled

  - `-h` – Show parameter help.

## Windows command example

Put the downloaded project folder in your user home folder. Replace `USERNAME` with your username.

```sh
"C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\python3.exe" "C:\Users\USERNAME\mfm\src\mfm_cmd.py" -c "C:\Users\USERNAME\mfm\premade_options\USAofPlastic-meters.json" -t "C:\Users\USERNAME\mfm\minimal_toolchanges\bambu-p1-series.gcode" --disable 0;
```

## Linux / Mac command example

Put the downloaded project folder in your user home folder.

```sh
/usr/local/bin/python3 "~/mfm/src/mfm_cmd.py" -c "~/mfm/premade_options/USAofPlastic-meters.json" -t "~/mfm/minimal_toolchanges/bambu-p1-series.gcode" --disable 0;
```

## Python path (PYTHONPATH)

The exact PYTHONPATH will depend on how you [installed Python](https://docs.python.org/3/using/windows.html).

Find where your Python location by running

- Windows cmd.exe `where python3` or `where python` or [`Get-Command`](https://superuser.com/a/676107)
- Linux/Mac terminal `which python3` or `which python`

Common Python install locations for Windows are

  - `C:\Program Files\Python X.Y` Python installer "for everyone" option
  - `C:\Users\USERNAME\AppData\Local\Programs\Python\PythonXY` Python installer "for me" option
  - `C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\python3.exe` VSCode Python install

Common Python install locations for Linux/Mac are

  - `/usr/local/bin/python3`
  - `python3` or `python`