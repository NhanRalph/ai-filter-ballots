# 🚀 QUICK START GUIDE - BƯỚC 1 & 2

## Bạn vừa hoàn thành BƯỚC 1 + BƯỚC 2!

### ✅ Đã có:
- ✅ Logic ROI Detection (BƯỚC 1)
- ✅ Logic Classification & Excel Export (BƯỚC 2)
- ✅ Full pipeline integration
- ✅ Demo scripts
- ✅ Test functions

---

## 🎯 Các cách test hệ thống:

### 1️⃣ Test NGAY (Không cần model):

```bash
# Demo BƯỚC 1 - Tạo ảnh mẫu và giả lập detection
python demo_step1.py

# Demo BƯỚC 2 - Test classifier và xuất Excel
python demo_step2.py
# Chọn option 1: Full Pipeline
```

**Kết quả:**
- File Excel được tạo tại `output/demo_full_results.xlsx`
- Có 3 sheets: Chi tiết phiếu, Thống kê, Kết quả ứng viên

---

### 2️⃣ Test với Model thật:

**Bước 1:** Đặt model vào thư mục:
```
model-ai-detect/
└── models/
    └── best.pt   ← Đặt file model vào đây
```

**Bước 2:** Chạy pipeline đầy đủ:
```bash
python full_pipeline.py
```

**Menu sẽ hiện ra:**
```
1. Xử lý 1 ảnh
2. Xử lý tất cả ảnh trong folder
3. Xử lý từ webcam real-time
4. Xem thống kê hiện tại
5. Xuất Excel
6. Reset dữ liệu
0. Thoát
```

---

### 3️⃣ Test từng bước:

#### Test BƯỚC 1 (ROI Detection):
```bash
python step1_roi_detection.py
# Chọn 1: Test với ảnh
# Chọn 2: Test với webcam
```

#### Test BƯỚC 2 (Classification):
```bash
python step2_ballot_classifier.py
# Chọn 1: Test classifier
# Chọn 2: Test data collection & Excel export
# Chọn 3: Chạy tất cả
```

---

## 📁 Cấu trúc Project:

```
model-ai-detect/
├── 📄 config.py                    # Cấu hình (ROI layout, tên ứng viên, etc.)
├── 📄 requirements.txt             # Thư viện cần cài
│
├── 🔧 step1_roi_detection.py      # BƯỚC 1: ROI Detection
├── 🔧 step2_ballot_classifier.py  # BƯỚC 2: Classification & Excel
├── 🔧 full_pipeline.py            # Pipeline đầy đủ (1+2)
│
├── 🎮 demo_step1.py               # Demo BƯỚC 1 (không cần model)
├── 🎮 demo_step2.py               # Demo BƯỚC 2 (tích hợp)
│
├── 📖 README.md                   # Tổng quan
├── 📖 README_STEP1.md             # Chi tiết BƯỚC 1
├── 📖 README_STEP2.md             # Chi tiết BƯỚC 2
├── 📖 QUICKSTART.md              # File này
│
├── 📁 models/                     # Chứa model YOLOv8
│   └── best.pt                   # ← Đặt model vào đây
│
├── 📁 test_images/               # Chứa ảnh test
│
└── 📁 output/                    # File Excel output
    └── *.xlsx
```

---

## 🔧 Cài đặt môi trường:

```bash
# 1. Cài thư viện
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Test không cần model
python demo_step2.py

# 3. Nếu có model, chạy full pipeline
python full_pipeline.py
```

---

## 📊 Output Excel Format:

File Excel có 3 sheets:

### Sheet 1: Chi tiết phiếu
| STT | ID Phiếu | Thời gian | Nguyễn Văn A | Trần Thị B | ... | Trạng thái |
|-----|----------|-----------|--------------|------------|-----|------------|
| 1   | PHIEU_0001 | 2026-02-24 10:30 | | X | X | ... | Hợp lệ |

**X** = Được bầu, **Rỗng** = Bị gạch

### Sheet 2: Thống kê tổng hợp
- Tổng số phiếu
- Phiếu hợp lệ/không hợp lệ
- Bầu 1/2/3 người

### Sheet 3: Kết quả ứng viên
- Thứ hạng
- Tên ứng viên
- Số phiếu bầu
- Tỷ lệ %

---

## ⚙️ Cấu hình (config.py):

```python
# Layout: "HORIZONTAL" hoặc "VERTICAL"
ROI_LAYOUT = "HORIZONTAL"

# Tên 5 ứng viên
CANDIDATE_NAMES = [
    "Nguyễn Văn A",
    "Trần Thị B",
    "Lê Văn C",
    "Phạm Thị D",
    "Hoàng Văn E"
]

# Ngưỡng confidence
CONFIDENCE_THRESHOLD = 0.5
```

---

## 🎯 Use Case Examples:

### Use Case 1: Xử lý 1 ảnh
```python
from full_pipeline import BallotProcessingPipeline

pipeline = BallotProcessingPipeline()
pipeline.process_image("test_images/ballot1.jpg", show_result=True)
pipeline.export_results("output/result.xlsx")
```

### Use Case 2: Xử lý folder ảnh
```python
pipeline = BallotProcessingPipeline()
pipeline.process_folder("test_images/", pattern="*.jpg")
pipeline.export_results("output/batch_results.xlsx")
```

### Use Case 3: Xử lý webcam
```python
pipeline = BallotProcessingPipeline()
pipeline.process_webcam(camera_id=0, max_ballots=10)
pipeline.export_results("output/webcam_results.xlsx")
```

---

## 🐛 Troubleshooting:

### ❌ Lỗi: "Model không load được"
**Giải pháp:**
- Kiểm tra file `best.pt` có tồn tại trong `models/`
- Kiểm tra đường dẫn trong `config.py`

### ❌ Lỗi: "Import không được module"
**Giải pháp:**
```bash
pip install -r requirements.txt
```

### ❌ Lỗi: "Camera không mở được"
**Giải pháp:**
- Kiểm tra camera ID (thử 0, 1, 2)
- Kiểm tra quyền truy cập camera
- Đảm bảo không app nào đang dùng camera

### ⚠️ Phát hiện không chính xác
**Giải pháp:**
- Giảm `CONFIDENCE_THRESHOLD` trong `config.py` (0.3 - 0.4)
- Kiểm tra ROI_LAYOUT phù hợp với phiếu
- Train lại model với dữ liệu tốt hơn

---

## 🔜 Tiếp theo:

Sau khi BƯỚC 1 & 2 hoạt động ổn định:

```bash
# Yêu cầu AI generate BƯỚC 3
"Tiếp tục BƯỚC 3"
```

**BƯỚC 3:** Xây dựng giao diện UI với CustomTkinter
- Camera preview real-time
- Nút Start/Stop
- Hiển thị thống kê
- Xuất Excel từ UI

**BƯỚC 4:** Tối ưu & Đóng gói
- Convert model sang ONNX/OpenVINO
- Đóng gói thành file .exe
- Chạy offline trên Windows

---

## 📞 Support:

Nếu gặp vấn đề, kiểm tra:
1. **README.md** - Tổng quan hệ thống
2. **README_STEP1.md** - Chi tiết BƯỚC 1
3. **README_STEP2.md** - Chi tiết BƯỚC 2
4. **Demo scripts** - Chạy demo để hiểu flow

---

## ✨ Features Highlights:

✅ **Tự động phát hiện** vết gạch trên phiếu bầu  
✅ **Phân loại thông minh** theo quy tắc bầu cử  
✅ **Xuất Excel đầy đủ** 3 sheets với thống kê chi tiết  
✅ **Hỗ trợ nhiều nguồn** ảnh tĩnh, folder, webcam  
✅ **Visualization** ROI và detection boxes  
✅ **Flexible configuration** dễ dàng tùy chỉnh  
✅ **Production-ready** code có error handling đầy đủ  

---

**Happy Coding! 🎉**
