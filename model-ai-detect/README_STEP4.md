# BƯỚC 4: Tối Ưu Hóa & Đóng Gói

## 📋 Mục Tiêu

Hoàn thiện hệ thống bằng cách:
1. **Tối ưu hóa model**: Chuyển YOLOv8 sang ONNX format (nhanh hơn, nhỏ hơn)
2. **Đóng gói ứng dụng**: Tạo file `.exe` standalone cho Windows
3. **Chuẩn bị phân phối**: Tạo installer hoặc package dễ cài đặt

## 🎯 Kết Quả Đạt Được

Sau BƯỚC 4, bạn sẽ có:
- ✅ Model ONNX tối ưu (nhỏ hơn, nhanh hơn PyTorch)
- ✅ File `.exe` chạy được trên Windows mà không cần Python
- ✅ Package hoàn chỉnh để phân phối cho người dùng cuối
- ✅ Hướng dẫn cài đặt và sử dụng

---

## PHẦN 1: Tối Ưu Hóa Model

### 1.1. Tại Sao Cần ONNX?

**PyTorch (.pt):**
- ✅ Dễ train và debug
- ❌ Kích thước lớn (~10MB model + 1GB PyTorch runtime)
- ❌ Inference chậm hơn
- ❌ Phụ thuộc vào PyTorch

**ONNX (.onnx):**
- ✅ Kích thước nhỏ (~10MB model + 50MB ONNXRuntime)
- ✅ Inference nhanh hơn 1.5-3x
- ✅ Không phụ thuộc PyTorch
- ✅ Tương thích đa nền tảng

### 1.2. Convert Model sang ONNX

#### Cách 1: Sử dụng script tự động

```bash
# Chạy script convert
python step4_convert_model.py

# Chọn option:
# 1. Convert to ONNX (khuyến nghị)
# 3. Benchmark: ONNX vs PyTorch (xem tốc độ)
```

**Output:**
- File: `models/best.onnx`
- Kích thước: ~10-15MB
- Tốc độ: Nhanh hơn 1.5-3x so với .pt

#### Cách 2: Manual convert

```python
from ultralytics import YOLO

# Load model
model = YOLO("models/best.pt")

# Export to ONNX
model.export(
    format='onnx',
    simplify=True,      # Giảm kích thước
    opset=12            # ONNX opset version
)
```

### 1.3. Benchmark Hiệu Suất

```bash
python step4_convert_model.py
# Chọn: 3. Benchmark
```

**Kết quả mẫu:**
```
PyTorch: 45.32ms (22.1 FPS)
ONNX:    18.75ms (53.3 FPS)

⚡ ONNX is 2.42x faster!
```

### 1.4. Sử dụng ONNX Model

**Cập nhật `config.py`:**

```python
# Đổi từ:
MODEL_PATH = "models/best.pt"

# Sang:
MODEL_PATH = "models/best.onnx"
```

**Lưu ý:** Code hiện tại (`step1_roi_detection.py`) đã hỗ trợ cả ONNX, không cần sửa gì thêm.

---

## PHẦN 2: Đóng Gói Thành .exe

### 2.1. Yêu Cầu

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Hoặc
pip install -r requirements.txt
```

### 2.2. Build .exe

#### Cách 1: Sử dụng build script (khuyến nghị)

**Trên Windows:**
```bash
# Chạy script tự động
build.bat

# Hoặc
python build.py
```

**Trên macOS/Linux (để test):**
```bash
python build.py
```

#### Cách 2: Manual build

```bash
# Sử dụng file .spec có sẵn
pyinstaller ballot_app.spec --clean

# Hoặc build từ đầu
pyinstaller --name=BallotVerification \
            --onedir \
            --windowed \
            --add-data=config.py:. \
            --add-data=models:models \
            --collect-all=ultralytics \
            --collect-all=cv2 \
            --collect-all=customtkinter \
            step3_ui_app.py
```

### 2.3. Cấu Trúc File `.spec`

File `ballot_app.spec` chứa cấu hình build:

```python
# Data files cần đóng gói
datas = [
    ('models/best.pt', 'models'),      # Model
    ('models/best.onnx', 'models'),    # ONNX model
    ('config.py', '.'),                # Config
]

# Hidden imports (các module không tự động detect)
hiddenimports = [
    'PIL._tkinter_finder',
    'openpyxl',
    'customtkinter',
    # ... more
]

# Exclude (không cần thiết)
excludes = [
    'matplotlib',
    'pytest',
]
```

### 2.4. Kết Quả Build

Sau khi build thành công:

```
dist/BallotVerification/
├── BallotVerification.exe    # Main executable (~50-100MB)
├── models/
│   └── best.onnx              # AI model
├── _internal/                 # Dependencies (auto-generated)
│   ├── ... (nhiều DLLs và packages)
└── README.txt                 # Hướng dẫn sử dụng
```

**Tổng kích thước:** ~200-500MB (tùy format model)

### 2.5. Test Ứng Dụng

```bash
# Di chuyển vào thư mục dist
cd dist/BallotVerification/

# Chạy .exe
./BallotVerification.exe

# Hoặc double-click file .exe trên Windows
```

**Kiểm tra:**
- ✅ UI hiện ra bình thường
- ✅ Model load được
- ✅ Camera hoạt động
- ✅ Xuất Excel thành công

---

## PHẦN 3: Phân Phối

### 3.1. Zip Package (Đơn giản nhất)

```bash
# Nén thư mục dist
cd dist/
zip -r BallotVerification_v1.0.zip BallotVerification/

# Hoặc trên Windows
# Right-click > Send to > Compressed folder
```

**Hướng dẫn người dùng:**
1. Giải nén file .zip
2. Mở thư mục `BallotVerification/`
3. Double-click `BallotVerification.exe`

### 3.2. Installer (Chuyên nghiệp)

#### Option A: Inno Setup (Windows)

**Download:** https://jrsoftware.org/isinfo.php

**Script mẫu (`installer.iss`):**

```ini
[Setup]
AppName=Ballot Verification System
AppVersion=1.0
DefaultDirName={pf}\BallotVerification
OutputDir=installer
OutputBaseFilename=BallotVerification_Setup

[Files]
Source: "dist\BallotVerification\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{commondesktop}\Ballot Verification"; Filename: "{app}\BallotVerification.exe"
Name: "{group}\Ballot Verification"; Filename: "{app}\BallotVerification.exe"
```

**Build installer:**
```bash
# Compile với Inno Setup
iscc installer.iss
```

#### Option B: NSIS (Nullsoft Scriptable Install System)

Tương tự Inno Setup nhưng có nhiều tùy chỉnh hơn.

### 3.3. Portable Version

Thêm file `PORTABLE.txt` vào thư mục để tạo version portable (không cần cài đặt):

```bash
# Trong dist/BallotVerification/
touch PORTABLE.txt
```

Code có thể detect file này và lưu settings vào thư mục hiện tại thay vì AppData.

---

## PHẦN 4: Tối Ưu Hóa Build

### 4.1. Giảm Kích Thước Package

**1. Sử dụng ONNX thay vì PyTorch:**
- PyTorch: ~1GB
- ONNX: ~50MB
- ⚡ Tiết kiệm: ~950MB

**2. Loại bỏ packages không cần:**

Trong `ballot_app.spec`:
```python
excludes = [
    'matplotlib',
    'pytest',
    'IPython',
    'notebook',
    'scipy',  # Nếu không dùng
]
```

**3. Sử dụng UPX compression:**
```python
# Trong .spec file
exe = EXE(
    ...
    upx=True,  # Bật nén UPX
    ...
)
```

**4. Sử dụng `--onefile` (1 file duy nhất):**

```bash
pyinstaller --onefile ...
```

⚠️ **Trade-off:**
- ✅ 1 file duy nhất, dễ phân phối
- ❌ Khởi động chậm hơn (phải extract)
- ❌ Antivirus hay false-positive

### 4.2. Tăng Tốc Độ Khởi Động

**1. Lazy import:**
```python
# Thay vì import ngay
import ultralytics
import cv2

# Import khi cần
def load_model():
    import ultralytics
    return ultralytics.YOLO(...)
```

**2. Preload model:**
- Đóng gói model đã được optimize
- Cache model predictions

**3. Sử dụng splash screen:**
```python
# Hiển thị loading screen trong khi khởi động
import tkinter as tk
splash = tk.Tk()
# ... show splash
splash.destroy()
```

### 4.3. Tăng Tốc Runtime

**1. Multithreading:**
- Camera capture: riêng 1 thread
- Model inference: riêng 1 thread
- UI update: main thread

**2. Batch processing:**
```python
# Xử lý nhiều frames cùng lúc
frames = [frame1, frame2, frame3]
results = model(frames, stream=True)
```

**3. Giảm resolution:**
```python
# Resize frame trước khi inference
frame_resized = cv2.resize(frame, (640, 640))
```

---

## PHẦN 5: Troubleshooting

### 5.1. Lỗi Build

**Lỗi: "Cannot find module 'xxx'"**

Thêm vào `hiddenimports` trong `.spec`:
```python
hiddenimports = [
    'xxx',
    'xxx.submodule',
]
```

**Lỗi: "Failed to execute script"**

Chạy với console để xem lỗi:
```python
exe = EXE(
    ...
    console=True,  # Hiện console
    ...
)
```

**Lỗi: "Cannot find data file"**

Thêm vào `datas` trong `.spec`:
```python
datas = [
    ('path/to/file', 'destination/folder'),
]
```

### 5.2. Lỗi Runtime

**Lỗi: "Model not found"**

Kiểm tra path trong code:
```python
import sys
import os

if getattr(sys, 'frozen', False):
    # Running as .exe
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(__file__)

MODEL_PATH = os.path.join(base_path, 'models', 'best.onnx')
```

**Lỗi: "OpenCV video capture failed"**

```python
# Thử các camera index khác nhau
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        break
```

### 5.3. Antivirus False Positive

**Giải pháp:**

1. **Code signing:** Ký code với certificate
2. **Submit to vendors:** Gửi file cho antivirus vendors
3. **Whitelist:** Hướng dẫn users whitelist
4. **Open source:** Public code để antivirus check

---

## PHẦN 6: Best Practices

### 6.1. Version Control

**Tag releases:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Semantic versioning:**
- `v1.0.0` - Major.Minor.Patch
- `v1.0.1` - Bug fix
- `v1.1.0` - New feature
- `v2.0.0` - Breaking change

### 6.2. Release Checklist

- [ ] Code hoàn chỉnh và đã test
- [ ] Model đã được optimize (ONNX)
- [ ] Requirements.txt up-to-date
- [ ] Documentation đầy đủ
- [ ] Build thành công trên Windows
- [ ] Test .exe trên máy clean (không có Python)
- [ ] Antivirus scan OK
- [ ] README cho end-users
- [ ] License file (nếu cần)
- [ ] Changelog

### 6.3. Update Strategy

**Cho ứng dụng:**
```python
# Version check
CURRENT_VERSION = "1.0.0"

def check_update():
    # Fetch từ server/GitHub
    latest = fetch_latest_version()
    if latest > CURRENT_VERSION:
        show_update_dialog()
```

**Cho model:**
```python
# Model versioning
MODEL_VERSION = "v2.1"
MODEL_PATH = f"models/best_{MODEL_VERSION}.onnx"
```

---

## 📊 Kết Quả So Sánh

### Trước Tối Ưu (PyTorch)

| Metric | Value |
|--------|-------|
| Package size | ~1.5 GB |
| Startup time | ~8 seconds |
| Inference time | ~45 ms |
| FPS | ~22 |
| Dependencies | PyTorch (large) |

### Sau Tối Ưu (ONNX)

| Metric | Value |
|--------|-------|
| Package size | ~250 MB |
| Startup time | ~3 seconds |
| Inference time | ~18 ms |
| FPS | ~55 |
| Dependencies | ONNXRuntime (small) |

**Cải thiện:**
- 📦 Size: Giảm 83%
- 🚀 Startup: Nhanh hơn 2.7x
- ⚡ Inference: Nhanh hơn 2.5x

---

## 🎯 Checklist Hoàn Thành BƯỚC 4

- [ ] Model đã convert sang ONNX
- [ ] Đã benchmark tốc độ (ONNX vs PyTorch)
- [ ] Config updated để dùng ONNX
- [ ] PyInstaller đã cài đặt
- [ ] Build script (`build.py`, `build.bat`) đã tạo
- [ ] File `.spec` đã configure đúng
- [ ] Build .exe thành công
- [ ] Test .exe trên Windows
- [ ] Package đã nén/installer đã tạo
- [ ] README cho end-users đã viết
- [ ] Documentation đầy đủ

---

## 🚀 Quick Start Commands

```bash
# 1. Convert model sang ONNX
python step4_convert_model.py

# 2. Benchmark (optional)
python step4_convert_model.py
# Choose: 3

# 3. Build executable
python build.py

# 4. Test
cd dist/BallotVerification/
./BallotVerification.exe

# 5. Package
cd dist/
zip -r BallotVerification_v1.0.zip BallotVerification/
```

---

## 📚 Tài Liệu Tham Khảo

- **PyInstaller**: https://pyinstaller.org/
- **ONNX**: https://onnx.ai/
- **ONNXRuntime**: https://onnxruntime.ai/
- **Ultralytics Export**: https://docs.ultralytics.com/modes/export/
- **Inno Setup**: https://jrsoftware.org/isinfo.php

---

## 🎉 Kết Luận

Sau BƯỚC 4, bạn đã có:
- ✅ Hệ thống hoàn chỉnh từ A-Z
- ✅ Model tối ưu, chạy nhanh
- ✅ Ứng dụng standalone không phụ thuộc Python
- ✅ Package sẵn sàng để phân phối

**Hệ thống đã sẵn sàng cho production! 🚀**
