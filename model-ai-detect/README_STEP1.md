# BƯỚC 1: Logic Core & OpenCV (ROI Mapping)

## ✅ Các file đã tạo:
- `config.py` - File cấu hình (đường dẫn model, tên ứng viên, màu sắc...)
- `step1_roi_detection.py` - Logic chính cho ROI detection
- `requirements.txt` - Danh sách thư viện cần cài đặt

## 📋 Hướng dẫn sử dụng:

### 1. Chuẩn bị môi trường:

```bash
# Cài đặt các thư viện
pip install -r requirements.txt
```

### 2. Chuẩn bị Model:

Tạo thư mục `models/` và đặt file `best.pt` vào đó:

```
model-ai-detect/
├── models/
│   └── best.pt          ← Đặt model YOLOv8 vào đây
├── config.py
├── step1_roi_detection.py
└── requirements.txt
```

### 3. Cấu hình (Tùy chọn):

Mở file `config.py` và chỉnh sửa:

- **ROI_LAYOUT**: Chọn `"HORIZONTAL"` (chia ngang) hoặc `"VERTICAL"` (chia dọc)
- **CANDIDATE_NAMES**: Thay đổi tên 5 ứng viên
- **CONFIDENCE_THRESHOLD**: Điều chỉnh ngưỡng confidence (0.3 - 0.7)

### 4. Chạy Test:

#### Test với ảnh tĩnh:
```bash
python step1_roi_detection.py
# Chọn option 1, nhập đường dẫn ảnh test
```

#### Test với Webcam:
```bash
python step1_roi_detection.py
# Chọn option 2
# Nhấn SPACE để chụp và phân tích
# Nhấn 'q' để thoát
```

## 🎯 Chức năng chính:

### Class `BallotROIDetector`:

```python
from step1_roi_detection import BallotROIDetector
import cv2

# 1. Khởi tạo detector
detector = BallotROIDetector()
detector.load_model()

# 2. Đọc ảnh
frame = cv2.imread("ballot_image.jpg")

# 3. Xử lý phiếu bầu
crossed_status, annotated_frame = detector.process_ballot(frame, visualize=True)

print(f"Kết quả: {crossed_status}")
# Output: [1, 0, 0, 1, 1]
# Giải thích: Người 1, 4, 5 bị gạch. Người 2, 3 được chọn
```

### Output:

- **crossed_status**: `List[int]` - Mảng 5 phần tử
  - `1` = Người này BỊ GẠCH (không được chọn)
  - `0` = Người này KHÔNG BỊ GẠCH (được chọn)
  
- **annotated_frame**: `np.ndarray` - Ảnh có vẽ ROI và detection

### Ví dụ kết quả:

```
Trạng thái gạch: [1, 0, 0, 1, 1]
Tổng số người bị gạch: 3/5

Chi tiết:
  1. Nguyễn Văn A: BỊ GẠCH ❌
  2. Trần Thị B: ĐƯỢC CHỌN ✓
  3. Lê Văn C: ĐƯỢC CHỌN ✓
  4. Phạm Thị D: BỊ GẠCH ❌
  5. Hoàng Văn E: BỊ GẠCH ❌
```

## 🔧 Các hàm chính:

| Hàm | Mô tả |
|-----|-------|
| `load_model()` | Load model YOLOv8 từ file .pt |
| `calculate_roi_zones()` | Tính toán 5 vùng ROI dựa trên kích thước ảnh |
| `detect_marks_on_frame()` | Phát hiện vết gạch trong ảnh |
| `check_bbox_in_roi()` | Kiểm tra bbox có nằm trong ROI nào |
| `process_ballot()` | **HÀM CHÍNH** - Xử lý 1 phiếu bầu hoàn chỉnh |
| `draw_visualization()` | Vẽ ROI và detection lên ảnh |

## 📝 Lưu ý:

1. **Model path**: Đảm bảo file `best.pt` nằm đúng vị trí trong `models/`
2. **ROI Layout**: 
   - HORIZONTAL: Phù hợp với phiếu bầu có tên xếp ngang
   - VERTICAL: Phù hợp với phiếu bầu có tên xếp dọc
3. **Confidence**: Nếu phát hiện không chính xác, thử giảm threshold xuống 0.3-0.4

## ⏭️ Tiếp theo:

Sau khi BƯỚC 1 hoạt động tốt, bạn có thể yêu cầu tôi thực hiện:
- **BƯỚC 2**: Logic phân loại phiếu & Export Excel
- **BƯỚC 3**: Xây dựng giao diện UI
- **BƯỚC 4**: Tối ưu Model & Đóng gói .exe
