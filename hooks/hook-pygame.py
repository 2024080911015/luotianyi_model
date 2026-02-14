# Hook for pygame-ce
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# Pygame has some data files (fonts, images, etc.) that may be needed
datas = collect_data_files('pygame')
binaries = collect_dynamic_libs('pygame')

# No hidden imports needed as pygame is already detected