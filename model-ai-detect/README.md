# HỆ THỐNG AI KIỂM DUYỆT PHIẾU BẦU

## 📁 Cấu trúc Project

```
model-ai-detect/
├── config.py                     # File cấu hình chung
├── requirements.txt              # Danh sách thư viện Python
├── .gitignore                   # Git ignore rules
│
├── step1_roi_detection.py       # ✅ BƯỚC 1: Logic Core & ROI Detection
├── step2_ballot_classifier.py   # ✅ BƯỚC 2: Phân loại & Export Excel
├── step3_ui_app.py              # ✅ BƯỚC 3: Giao diện UI (CustomTkinter)
├── step4_convert_model.py       # ✅ BƯỚC 4: Convert model sang ONNX
├── full_pipeline.py             # Pipeline đầy đủ (Command line)
│
├── demo_step1.py                # Demo BƯỚC 1 (không cần model)
├── demo_step2.py                # Demo BƯỚC 2 (tích hợp 1+2)
├── demo_step3.py                # Demo BƯỚC 3 (UI không cần model)
│
├── build.py                     # Script build .exe (Windows)
├── build.bat                    # Batch script build (Windows)
├── ballot_app.spec              # PyInstaller spec file
│
├── README.md                    # README chính
├── README_STEP1.md              # Hướng dẫn BƯỚC 1
├── README_STEP2.md              # Hướng dẫn BƯỚC 2
├── README_STEP3.md              # Hướng dẫn BƯỚC 3
├── README_STEP4.md              # Hướng dẫn BƯỚC 4
├── QUICKSTART.md                # Hướng dẫn nhanh
├── USER_GUIDE.md                # Hướng dẫn cho người dùng cuối
│
├── models/                      # Thư mục chứa model AI
│   ├── best.pt                 # ← Model YOLOv8 gốc
│   └── best.onnx               # ← Model ONNX (sau convert)
│
├── output/                      # Thư mục chứa file Excel kết quả
│   └── *.xlsx                  # File Excel output
│
└── test_images/                # Thư mục chứa ảnh test
    └── (đặt ảnh phiếu bầu test vào đây)
```

## 🚀 Quick Start

### 1. Cài đặt môi trường

```bash
# Di chuyển vào thư mục project
cd model-ai-detect

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Chạy Demo (Không cần model)

```bash
# Demo UI - Xem giao diện và flow
python demo_step3.py

# Demo BƯỚC 1 - ROI Detection
python demo_step1.py

# Demo BƯỚC 2 - Classification & Excel
python demo_step2.py
```

### 3. Chạy ứng dụng chính

#### 🎨 Giao diện UI (Khuyến nghị):
```bash
# Đặt model best.pt vào models/ trước
python step3_ui_app.py
```

**Tính năng:**
- 📹 Camera preview real-time
- 📸 Chụp & phân tích phiếu
- 📊 Thống kê trực quan
- 💾 Xuất Excel
- ⚙️ Cài đặt ROI & Confidence

#### 💻 Command Line (Alternative):
```bash
python full_pipeline.py
```

**Menu:**
```
1. Xử lý 1 ảnh
2. Xử lý folder ảnh
3. Webcam real-time
4. Xem thống kê
5. Xuất Excel
0. Thoát
```

## ✅ Tiến độ

- [x] **BƯỚC 1**: Logic Core & OpenCV (ROI Mapping) ✅
- [x] **BƯỚC 2**: Logic Phân loại Phiếu & Export Excel ✅
- [x] **BƯỚC 3**: Xây dựng Giao diện UI ✅
- [x] **BƯỚC 4**: Tối ưu Model & Đóng gói .exe ✅

## 📝 Chi tiết các BƯỚC
### BƯỚC 1: ROI Detection - ✅ Hoàn thành

✅ Load model YOLOv8 từ file `.pt`  
✅ Chia ảnh làm 5 vùng ROI (HORIZONTAL/VERTICAL)  
✅ Detect vết gạch trên phiếu bầu  
✅ Mapping bounding box vào ROI  
✅ Trả về mảng kết quả `[1,0,0,1,1]`  
✅ Visualization với OpenCV  
✅ Test với ảnh tĩnh  
✅ Test với webcam real-time  
& webcam  

### BƯỚC 2: Classification & Exceliếu hợp lệ/không hợp lệ  
✅ Class `BallotDataCollector` - Thu thập dữ liệu nhiều phiếu  
✅ Class `ExcelExporter` - Xuất Excel 3 sheets (Chi tiết, Thống kê, Kết quả)  
✅ Tích hợp BƯỚC 1 + BƯỚC 2  
✅ Thống kê tổng hợp (tổng phiếu, hợp lệ, không hợp lệ, xếp hạng ứng viên)  
✅ Demo với visualization  
✅ Interactive mode  

### Cách sử dụng tích hợp:

```python
from step1_roi_detection import BallotROIDetector
from full_pipeline import BallotProcessingPipeline

# Khởi tạo
pipeline = BallotProcessingPipeline()

# Xử lý folder
pipeline.process_folder("test_images/", pattern="*.jpg")

# Hoặc webcam
pipeline.process_webcam(camera_id=0, max_ballots=10)

# Xuất Excel
pipeline.export_results("output/results.xlsx")

## 🎯 Quy tắc Bầu cử

- **Bầu 1 người**: Gạch 4 người (4 vết gạch)
- **Bầu 2 người**: Gạch 3 người (3 vết gạch)
- **Bầu 3 người**: Gạch 2 người (2 vết gạch)
- **Không hợp l& 2 hoạt động tốt, tiếp tục với:

```
BƯỚC 3: Xây dựng Giao diện UI với CustomTkinter
```

Yêu cầu AI generate code bằng cách gõ: **"Tiếp tục BƯỚC 3
# Layout ROI
ROI_LAYOUT = "HORIZONTAL"  # hoặc "VERTICAL"

# Tên ứng viên
CANDIDATE_NAMES = [
    "Nguyễn Văn A",
    "Trần Thị B",
    "Lê Văn C",
    "Phạm Thị D",
    "Hoàng Văn E"
]

# Ngưỡng confidence
CONFIDENCE_THRESHOLD = 0.5
```ệ**: 0, 1 hoặc 5 vết gạch
## 🔜 Bước tiếp theo
## 🔜 Bước tiếp theo

Hệ thống đã hoàn thiện! 🎉

### BƯỚC 4: Tối Ưu & Đóng Gói - ✅ Hoàn thành

✅ Convert model sang ONNX (nhanh hơn, nhỏ hơn)  
✅ Script tự động convert với `step4_convert_model.py`  
✅ Benchmark tốc độ ONNX vs PyTorch  
✅ PyInstaller configuration (`ballot_app.spec`)  
✅ Build script (`build.py`, `build.bat`)  
✅ Đóng gói thành `.exe` standalone cho Windows  
✅ Hướng dẫn cho người dùng cuối (`USER_GUIDE.md`)  

**Để build .exe:**

```bash
# Trên Windows
build.bat

# Hoặc
python build.py
```

**Xem chi tiết:**
- [README_STEP4.md](README_STEP4.md) - Hướng dẫn chi tiết BƯỚC 4
- [USER_GUIDE.md](USER_GUIDE.md) - Hướng dẫn cho người dùng cuối

---

## 📚 Tài liệu

- [README_STEP1.md](README_STEP1.md) - Hướng dẫn chi tiết BƯỚC 1
- [README_STEP2.md](README_STEP2.md) - Hướng dẫn chi tiết BƯỚC 2
- [README_STEP3.md](README_STEP3.md) - Hướng dẫn chi tiết BƯỚC 3
- [README_STEP4.md](README_STEP4.md) - Hướng dẫn chi tiết BƯỚC 4
- [QUICKSTART.md](QUICKSTART.md) - Hướng dẫn nhanh
- [USER_GUIDE.md](USER_GUIDE.md) - Hướng dẫn cho người dùng cuối
- [MASTER_PROMPT.md](../MASTER_PROMPT.md) - Tài liệu tổng quan hệ thống
Yêu cầu AI generate code bằng cách gõ: **"Tiếp tục BƯỚC 4"**

BƯỚC 4 sẽ bao gồm:
- Convert model sang ONNX/OpenVINO
- Tối ưu tốc độ inference
- Đóng gói PyInstaller thành .exe
- Script installer cho Windows
- Testing trên máy không GPU