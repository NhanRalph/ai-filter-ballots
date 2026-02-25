# DATASET README

## 📁 Dataset Structure

```
dataset/
├── images/
│   ├── train/          # Training images (70% of total)
│   ├── val/            # Validation images (15%)
│   └── test/           # Test images (15%)
├── labels/
│   ├── train/          # Training labels (.txt files)
│   ├── val/            # Validation labels
│   └── test/           # Test labels
├── data.yaml           # Dataset configuration
└── README.md           # This file
```

## 🎯 Cách Sử Dụng

### Bước 1: Thu thập ảnh

1. **Chụp/scan phiếu bầu:**
   - Minimum: **100 ảnh** (khuyến nghị: **500+ ảnh**)
   - Độ phân giải: 640x640 pixels trở lên
   - Format: JPG, PNG
   - Đa dạng: Các loại dấu X khác nhau, độ sáng khác nhau

2. **Phân chia dataset:**
   - 70% → `images/train/`
   - 15% → `images/val/`
   - 15% → `images/test/`

### Bước 2: Gán nhãn (Annotation)

Chọn 1 trong 3 công cụ:

#### Option 1: Label Studio (Khuyến nghị - Free, Local)

```bash
# Install
pip install label-studio

# Start
label-studio start

# Browser mở tự động: http://localhost:8080
```

**Workflow:**
1. Tạo project mới "Ballot Cross Detection"
2. Import ảnh từ `dataset/images/train/`
3. Chọn template: Object Detection with Bounding Boxes
4. Vẽ bounding box quanh mỗi dấu X
5. Label: "cross"
6. Export → YOLO format
7. Copy labels vào `dataset/labels/train/`

#### Option 2: Roboflow (Dễ nhất - Cloud)

1. Đăng ký tài khoản miễn phí: https://roboflow.com/
2. Tạo project: "Ballot Cross Detection"
3. Upload ảnh
4. Annotate online (vẽ bounding box)
5. Generate dataset → Export format: **YOLOv8**
6. Download về → Tự động có cấu trúc đúng

#### Option 3: LabelImg (Đơn giản - Local)

```bash
pip install labelImg
labelImg
```

### Bước 3: Kiểm tra format

**File nhãn (.txt) format:**

```
class_id x_center y_center width height
```

**Ví dụ `phieu_001.txt`:**
```
0 0.512 0.345 0.089 0.123
0 0.678 0.456 0.098 0.145
```

- `class_id`: 0 (cross)
- Tọa độ: Normalized (0-1)

**Tính toán normalized coordinates:**

```python
x_center = (x_min + x_max) / 2 / image_width
y_center = (y_min + y_max) / 2 / image_height
width = (x_max - x_min) / image_width
height = (y_max - y_min) / image_height
```

**Mỗi ảnh PHẢI có file .txt tương ứng:**
- `phieu_001.jpg` → `phieu_001.txt`
- `phieu_002.png` → `phieu_002.txt`

### Bước 4: Training

```bash
python train_model.py
```

Hoặc chạy trực tiếp:

```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(data='dataset/data.yaml', epochs=100)
```

## 📊 Dataset Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Total images | 100 | 500+ |
| Train images | 50 | 350+ |
| Val images | 25 | 75+ |
| Test images | 25 | 75+ |
| Image size | 640x640 | 1280x720 |
| Diversity | 3 types | 10+ types |

## 🔍 Validation Checklist

- [ ] Mỗi ảnh có file .txt tương ứng
- [ ] File .txt đúng YOLO format (5 số trên mỗi dòng)
- [ ] Tọa độ normalized (0-1)
- [ ] Minimum 100 ảnh
- [ ] Split train/val/test đúng tỷ lệ
- [ ] data.yaml đúng cấu hình

## 🛠️ Tools

### Label Studio
- Website: https://labelstud.io/
- Install: `pip install label-studio`
- Type: Local
- Price: Free

### Roboflow
- Website: https://roboflow.com/
- Type: Cloud
- Price: Free tier (1000 images)
- Features: Auto-augmentation, format conversion

### LabelImg
- Install: `pip install labelImg`
- Type: Local desktop
- Price: Free
- Simple GUI

## ❓ Troubleshooting

**Q: Ảnh đã có nhưng không train được?**
- Check: Mỗi ảnh phải có file .txt cùng tên
- Check: Format .txt đúng YOLO (5 số mỗi dòng)

**Q: Tọa độ > 1 hay < 0?**
- Error: Chưa normalize
- Fix: Chia cho width/height của ảnh

**Q: Model train xong mAP thấp?**
- Thu thập thêm ảnh (500+)
- Re-label kỹ hơn
- Tăng epochs (200-300)

**Q: Không biết vẽ bounding box?**
- Vẽ hình chữ nhật bao quanh dấu X
- Không cần chính xác 100%, gần đúng là được
- Bao cả viền của dấu X

## 📖 More Info

Xem hướng dẫn chi tiết:
- `README_STEP0_TRAINING.md` - Complete training guide
- `train_model.py` - Training script
- `validate_model.py` - Validation script
- `test_model.py` - Testing script
