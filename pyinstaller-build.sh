# Window
pyinstaller --onefile gui.py --name MFPP

# MacOS
# Create code signing identity first
# https://github.com/pyinstaller/pyinstaller/issues/6167#issuecomment-906307356
pyinstaller --onefile gui.py --codesign-identity ansonliu-imac-code-sign --name MFPP