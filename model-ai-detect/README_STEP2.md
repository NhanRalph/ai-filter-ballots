# BƯỚC 2: Logic Phân loại Phiếu & Export Excel

## ✅ Các file đã tạo:
- `step2_ballot_classifier.py` - Logic phân loại và xuất Excel
- `demo_step2.py` - Demo tích hợp BƯỚC 1 + BƯỚC 2

## 📋 Chức năng đã hoàn thành:

### 1. **BallotClassifier** - Phân loại phiếu bầu

```python
from step2_ballot_classifier import BallotClassifier

classifier = BallotClassifier()

# Nhận kết quả từ BƯỚC 1
crossed_status = [1, 0, 0, 1, 1]  # 3 gạch = Bầu 2 người

# Phân loại
result = classifier.classify_ballot(crossed_status)

print(result)
# {
#     'is_valid': True,
#     'ballot_type': 'Bầu 2 người',
#     'num_crossed': 3,
#     'num_voted': 2,
#     'voted_for': ['Trần Thị B', 'Lê Văn C'],
#     'crossed_for': ['Nguyễn Văn A', 'Phạm Thị D', 'Hoàng Văn E'],
#     'status_message': '✅ Hợp lệ - Bầu 2 người'
# }
```

### 2. **BallotDataCollector** - Thu thập dữ liệu nhiều phiếu

```python
from step2_ballot_classifier import BallotDataCollector

collector = BallotDataCollector()

# Thêm phiếu
collector.add_ballot([1, 1, 0, 1, 1])  # Phiếu 1
collector.add_ballot([1, 0, 0, 1, 1])  # Phiếu 2
collector.add_ballot([0, 0, 1, 1, 0])  # Phiếu 3

# Xem thống kê
collector.print_statistics()
# Output:
# ================================
# THỐNG KÊ TỔNG HỢP
# ================================
# Tổng số phiếu: 3
# Phiếu hợp lệ: 3 (100.0%)
# ...
```

### 3. **ExcelExporter** - Xuất dữ liệu ra Excel

```python
from step2_ballot_classifier import ExcelExporter

exporter = ExcelExporter()

# Xuất với 3 sheets:
# - Chi tiết phiếu
# - Thống kê
# - Kết quả ứng viên
output_file = exporter.export_to_excel(
    collector.get_ballots(),
    output_path="output/results.xlsx",
    include_statistics=True
)
```

## 🎯 Quy tắc Phân loại:

| Số gạch | Số người được bầu | Loại phiếu | Hợp lệ |
|---------|-------------------|------------|--------|
| 4 | 1 | Bầu 1 người | ✅ |
| 3 | 2 | Bầu 2 người | ✅ |
| 2 | 3 | Bầu 3 người | ✅ |
| 0 | 5 | Không xác định | ❌ |
| 1 | 4 | Không xác định | ❌ |
| 5 | 0 | Không xác định | ❌ |

## 📊 Format Excel Output:

### Sheet 1: Chi tiết phiếu
| STT | ID Phiếu | Thời gian | Nguyễn Văn A | Trần Thị B | Lê Văn C | Phạm Thị D | Hoàng Văn E | Trạng thái | Loại phiếu |
|-----|----------|-----------|--------------|------------|----------|------------|-------------|------------|------------|
| 1 | Phiếu_0001 | 2026-02-24 10:30:00 | | X | X | | | Hợp lệ | Bầu 2 người |
| 2 | Phiếu_0002 | 2026-02-24 10:31:00 | | | X | | | Hợp lệ | Bầu 1 người |

**Chú thích:** `X` = Người được bầu, Rỗng = Người bị gạch

### Sheet 2: Thống kê
| Chỉ số | Giá trị |
|--------|---------|
| Tổng số phiếu | 10 |
| Phiếu hợp lệ | 8 |
| Phiếu không hợp lệ | 2 |
| Tỷ lệ hợp lệ (%) | 80.00 |
| Bầu 1 người | 2 |
| Bầu 2 người | 4 |
| Bầu 3 người | 2 |

### Sheet 3: Kết quả ứng viên
| Thứ hạng | Tên ứng viên | Số phiếu bầu | Tỷ lệ (%) |
|----------|--------------|--------------|-----------|
| 1 | Lê Văn C | 6 | 75.00 |
| 2 | Trần Thị B | 5 | 62.50 |
| 3 | Phạm Thị D | 4 | 50.00 |
| 4 | Nguyễn Văn A | 3 | 37.50 |
| 5 | Hoàng Văn E | 2 | 25.00 |

## 🚀 Cách sử dụng:

### Test đơn lẻ:

```bash
# Test classifier
python step2_ballot_classifier.py
# Chọn option 1 hoặc 2
```

### Demo tích hợp đầy đủ:

```bash
# Demo với 10 phiếu mẫu
python demo_step2.py
# Chọn option 1: Full Pipeline
```

### Demo với visualization:

```bash
python demo_step2.py
# Chọn option 2: With Visualization
# Nhấn phím bất kỳ để xem từng phiếu
```

### Demo tương tác:

```bash
python demo_step2.py
# Chọn option 3: Interactive Mode
# Nhập trạng thái gạch thủ công
# Ví dụ: 1,0,0,1,1
```

## 🔗 Tích hợp với BƯỚC 1:

```python
from step1_roi_detection import BallotROIDetector
from step2_ballot_classifier import (
    BallotClassifier,
    BallotDataCollector,
    ExcelExporter
)
import cv2

# Khởi tạo
detector = BallotROIDetector()
detector.load_model()

classifier = BallotClassifier()
collector = BallotDataCollector()

# Xử lý ảnh
frame = cv2.imread("ballot.jpg")

# BƯỚC 1: Detect vết gạch
crossed_status, annotated = detector.process_ballot(frame, visualize=True)
print(f"Phát hiện: {crossed_status}")

# BƯỚC 2: Phân loại
classification = classifier.classify_ballot(crossed_status)
print(f"Kết quả: {classification['status_message']}")

# Thu thập dữ liệu
collector.add_ballot(crossed_status, ballot_id="PHIEU_001")

# Xuất Excel sau khi xử lý nhiều phiếu
exporter = ExcelExporter()
exporter.export_to_excel(collector.get_ballots(), "output/results.xlsx")
```

## 📁 Cấu trúc thư mục sau BƯỚC 2:

```
model-ai-detect/
├── config.py
├── requirements.txt
├── step1_roi_detection.py     # BƯỚC 1
├── step2_ballot_classifier.py # BƯỚC 2 ✨
├── demo_step1.py
├── demo_step2.py              # Demo tích hợp ✨
│
├── models/
│   └── best.pt
│
├── output/                     # Thư mục Excel output ✨
│   ├── test_results.xlsx
│   ├── demo_full_results.xlsx
│   └── ...
│
└── test_images/
```

## 🧪 Kết quả Test:

Chạy `python step2_ballot_classifier.py` và chọn "3. Chạy tất cả tests":

```
TEST: BALLOT CLASSIFIER
======================================
Test 1: Phiếu hợp lệ - Bầu 1 người
  ✅ PASS
Test 2: Phiếu hợp lệ - Bầu 2 người
  ✅ PASS
...
SUMMARY: 6 passed, 0 failed out of 6 tests
======================================

TEST: DATA COLLECTION & EXCEL EXPORT
======================================
Đã thêm 8 phiếu

THỐNG KÊ TỔNG HỢP
======================================
Tổng số phiếu: 8
Phiếu hợp lệ: 6 (75.0%)
...
✅ Test hoàn tất! File đã được lưu tại: output/test_results.xlsx
```

## 💡 Lưu ý:

1. **Thư mục output**: Sẽ tự động tạo nếu chưa có
2. **Timestamp**: Mỗi phiếu được ghi nhận thời gian thêm vào
3. **Metadata**: Có thể thêm thông tin bổ sung (đường dẫn ảnh, camera ID, etc.)
4. **Stats**: Chỉ tính phiếu hợp lệ khi tổng hợp kết quả ứng viên

## ⏭️ Tiếp theo:

**BƯỚC 3**: Xây dựng giao diện UI với CustomTkinter

Yêu cầu AI generate code: **"Tiếp tục BƯỚC 3"**
