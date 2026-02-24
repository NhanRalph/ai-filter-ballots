# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file cho Ballot Verification System
Sử dụng: pyinstaller ballot_app.spec
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules
import sys
import os

# Đảm bảo thư mục hiện tại
block_cipher = None
app_name = 'BallotVerification'

# Thu thập tất cả dependencies
ultralytics_datas, ultralytics_binaries, ultralytics_hiddenimports = collect_all('ultralytics')
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')
customtkinter_datas, customtkinter_binaries, customtkinter_hiddenimports = collect_all('customtkinter')

# Thêm hidden imports cho các packages
hiddenimports = []
hiddenimports += ultralytics_hiddenimports
hiddenimports += cv2_hiddenimports
hiddenimports += customtkinter_hiddenimports
hiddenimports += [
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'openpyxl',
    'openpyxl.cell._writer',
    'openpyxl.styles',
    'pandas',
    'numpy',
    'yaml',
    'torch',
    'torchvision',
]

# Thêm ONNX nếu sử dụng
# hiddenimports += ['onnxruntime', 'onnx']

# Data files cần đóng gói
datas = []
datas += ultralytics_datas
datas += cv2_datas
datas += customtkinter_datas

# Thêm model (nếu có)
if os.path.exists('models/best.pt'):
    datas += [('models/best.pt', 'models')]
if os.path.exists('models/best.onnx'):
    datas += [('models/best.onnx', 'models')]

# Thêm config
datas += [('config.py', '.')]

# Binaries
binaries = []
binaries += ultralytics_binaries
binaries += cv2_binaries
binaries += customtkinter_binaries

a = Analysis(
    ['step3_ui_app.py'],  # Main script
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Loại bỏ matplotlib nếu không dùng
        'pytest',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Nén với UPX (giảm size)
    console=False,  # Không hiện console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # Thêm icon nếu có
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
