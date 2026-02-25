# BƯỚC 0: TRAINING MODEL - Huấn Luyện Model YOLOv8

## 📋 Tổng Quan

**BƯỚC 0** là bước **QUAN TRỌNG NHẤT** - Training model AI để nhận diện dấu X trên phiếu bầu.

**Kết quả:** File `models/best.pt` - Model đã train sẵn để dùng cho BƯỚC 1-4.

---

## 🎯 Quy Trình Training

```
Dataset (Ảnh + Nhãn)
        ↓
    Annotate (Label ảnh)
        ↓
    Config YOLOv8
        ↓
    Training
        ↓
    Validation
        ↓
    Export best.pt
        ↓
    Sử dụng trong BƯỚC 1-4
```

---

## 📁 PHẦN 1: Chuẩn Bị Dataset

### 1.1. Thu Thập Ảnh Phiếu Bầu

**Số lượng khuyến nghị:**
- ✅ **Minimum:** 100 ảnh phiếu (50 train, 25 val, 25 test)
- ✅ **Tốt:** 300-500 ảnh
- ✅ **Ideal:** 1000+ ảnh

**Yêu cầu ảnh:**
- Chụp phiếu bầu thật với dấu X rõ ràng
- Đa dạng: Nhiều kiểu viết X, nhiều góc chụp
- Đủ sáng, không mờ
- Resolution: 640x640 trở lên

**Cách chụp:**
```
1. Chuẩn bị 100 phiếu bầu mẫu
2. Mỗi phiếu: Vẽ dấu X khác nhau (mỏng, đậm, chéo, ngang...)
3. Chụp mỗi phiếu 2-3 góc độ khác nhau
4. Lưu format: .jpg hoặc .png
5. Đặt tên: phieu_001.jpg, phieu_002.jpg, ...
```

**Folder structure:**
```
dataset/
├── images/
│   ├── train/
│   │   ├── phieu_001.jpg
│   │   ├── phieu_002.jpg
│   │   └── ...
│   ├── val/
│   │   ├── phieu_051.jpg
│   │   └── ...
│   └── test/
│       ├── phieu_076.jpg
│       └── ...
└── labels/
    ├── train/
    │   ├── phieu_001.txt
    │   ├── phieu_002.txt
    │   └── ...
    ├── val/
    │   └── ...
    └── test/
        └── ...
```

---

### 1.2. Label/Annotate Ảnh

**Công cụ khuyến nghị:** [Label Studio](https://labelstud.io/) hoặc [Roboflow](https://roboflow.com/)

#### Option A: Label Studio (Free, Local)

**Cài đặt:**
```bash
pip install label-studio

# Khởi động
label-studio

# Truy cập: http://localhost:8080
```

**Labeling:**
1. Tạo project mới
2. Import ảnh từ `dataset/images/train/`
3. Chọn template: "Object Detection with Bounding Boxes"
4. Vẽ bounding box quanh mỗi dấu X
5. Label: "crossed_mark" hoặc "X"
6. Export format: **YOLO**

**Export:**
- File → Export → YOLO format
- Lưu vào: `dataset/labels/train/`

#### Option B: Roboflow (Cloud, Easier)

**Setup:**
1. Đăng ký: https://roboflow.com/
2. Create project: "Ballot Cross Detection"
3. Upload ảnh
4. Annotate từng ảnh (vẽ box quanh dấu X)
5. Generate dataset → Export format: **YOLOv8**
6. Download về

**Ưu điểm:**
- Giao diện đẹp, dễ dùng
- Auto-split train/val/test
- Augmentation tự động
- Export trực tiếp cho YOLOv8

---

### 1.3. Format Nhãn YOLO

**File label:** `phieu_001.txt`

**Format mỗi dòng:**
```
<class_id> <x_center> <y_center> <width> <height>
```

**Ví dụ:** (Ảnh 640x640, có 2 dấu X)
```
0 0.3125 0.2500 0.0625 0.0468
0 0.6875 0.7500 0.0781 0.0625
```

- `class_id`: 0 (chỉ có 1 class: "crossed_mark")
- `x_center, y_center, width, height`: **normalized** (0-1)

**Cách tính:**
```python
# Absolute coordinates
x1, y1, x2, y2 = 180, 140, 220, 170  # pixels
img_width, img_height = 640, 640

# Normalize to YOLO format
x_center = ((x1 + x2) / 2) / img_width   # 0.3125
y_center = ((y1 + y2) / 2) / img_height  # 0.2500
width = (x2 - x1) / img_width            # 0.0625
height = (y2 - y1) / img_height          # 0.0468
```

---

### 1.4. Config File - data.yaml

Tạo file `dataset/data.yaml`:

```yaml
# Dataset paths (absolute hoặc relative)
path: ./dataset  # Root folder
train: images/train
val: images/val
test: images/test

# Classes
nc: 1  # Number of classes
names: ['crossed_mark']  # Class names

# Optional
download: null
```

**Giải thích:**
- `path`: Thư mục gốc dataset
- `train/val/test`: Subfolder chứa ảnh
- `nc`: Số lượng class (1 = chỉ detect dấu X)
- `names`: Tên class

---

## 🔥 PHẦN 2: Training Model

### 2.1. Cài Đặt Ultralytics

```bash
# Cài đặt
pip install ultralytics

# Kiểm tra
yolo version
# Output: Ultralytics YOLOv8.x.x
```

---

### 2.2. Training Script

Tạo file `train_model.py`:

```python
"""
Script training YOLOv8 cho cross mark detection
"""

from ultralytics import YOLO
import torch


def train_ballot_detector():
    """Train YOLOv8 model for ballot cross detection"""
    
    print("="*70)
    print("TRAINING YOLOV8 - BALLOT CROSS DETECTION")
    print("="*70)
    
    # Check GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\n🔧 Device: {device}")
    
    if device == 'cuda':
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("   ⚠️  No GPU detected. Training will be slower.")
    
    # Load pretrained model
    print("\n📦 Loading pretrained YOLOv8n model...")
    model = YOLO('yolov8n.pt')  # Nano model (fastest)
    # Alternatives:
    # model = YOLO('yolov8s.pt')  # Small
    # model = YOLO('yolov8m.pt')  # Medium (better accuracy)
    
    # Training configuration
    print("\n⚙️  Training configuration:")
    config = {
        'data': 'dataset/data.yaml',  # Path to data.yaml
        'epochs': 100,                 # Number of epochs
        'imgsz': 640,                  # Image size
        'batch': 16,                   # Batch size (adjust based on GPU)
        'device': device,              # cuda or cpu
        'workers': 4,                  # Dataloader workers
        'project': 'runs/train',       # Output folder
        'name': 'ballot_cross',        # Experiment name
        'exist_ok': True,              # Overwrite existing
        
        # Hyperparameters
        'patience': 20,                # Early stopping patience
        'save': True,                  # Save checkpoints
        'save_period': 10,             # Save every N epochs
        'cache': False,                # Cache images (True = faster, more RAM)
        'optimizer': 'SGD',            # SGD or Adam
        'lr0': 0.01,                   # Initial learning rate
        'lrf': 0.01,                   # Final learning rate
        'momentum': 0.937,             # SGD momentum
        'weight_decay': 0.0005,        # Weight decay
        'warmup_epochs': 3.0,          # Warmup epochs
        'warmup_momentum': 0.8,        # Warmup momentum
        'box': 7.5,                    # Box loss gain
        'cls': 0.5,                    # Class loss gain
        'dfl': 1.5,                    # DFL loss gain
        
        # Augmentation
        'hsv_h': 0.015,                # Hue augmentation
        'hsv_s': 0.7,                  # Saturation
        'hsv_v': 0.4,                  # Value
        'degrees': 10.0,               # Rotation degrees
        'translate': 0.1,              # Translation
        'scale': 0.5,                  # Scale
        'shear': 0.0,                  # Shear
        'perspective': 0.0,            # Perspective
        'flipud': 0.0,                 # Flip up-down
        'fliplr': 0.5,                 # Flip left-right
        'mosaic': 1.0,                 # Mosaic augmentation
        'mixup': 0.0,                  # Mixup augmentation
    }
    
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Start training
    print("\n🚀 Starting training...")
    print("="*70)
    
    results = model.train(**config)
    
    # Training complete
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    
    # Best model path
    best_model = f"runs/train/ballot_cross/weights/best.pt"
    print(f"\n📦 Best model saved: {best_model}")
    
    # Metrics
    print(f"\n📊 Final Metrics:")
    print(f"   mAP50: {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
    print(f"   mAP50-95: {results.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")
    print(f"   Precision: {results.results_dict.get('metrics/precision(B)', 'N/A')}")
    print(f"   Recall: {results.results_dict.get('metrics/recall(B)', 'N/A')}")
    
    print("\n💡 Next steps:")
    print(f"   1. Copy {best_model} to models/best.pt")
    print("   2. Run validation: python validate_model.py")
    print("   3. Test with app: python step3_ui_app.py")
    
    return results


if __name__ == "__main__":
    train_ballot_detector()
```

---

### 2.3. Chạy Training

```bash
# Chạy training
python train_model.py

# Output:
# 🔧 Device: cuda
# 📦 Loading pretrained YOLOv8n model...
# 🚀 Starting training...
# Epoch 1/100: 100%|████████| 50/50 [00:15<00:00, 3.21it/s]
# ...
# ✅ TRAINING COMPLETE!
```

**Thời gian:**
- GPU (GTX 1060+): 30-60 phút (100 epochs)
- CPU: 3-5 giờ

---

### 2.4. Monitoring Training

**TensorBoard:**
```bash
# Xem training progress
tensorboard --logdir runs/train

# Truy cập: http://localhost:6006
```

**Metrics quan trọng:**
- **mAP50**: Mean Average Precision @ IoU=0.5 (cao càng tốt, >0.8 là tốt)
- **Precision**: Độ chính xác (cao = ít false positive)
- **Recall**: Độ phủ (cao = ít false negative)
- **Loss**: Giảm dần theo epoch

---

### 2.5. Hyperparameter Tuning

Nếu kết quả chưa tốt:

**Increase accuracy:**
```python
# Dùng model lớn hơn
model = YOLO('yolov8m.pt')  # Medium instead of Nano

# Increase epochs
'epochs': 200

# Reduce learning rate
'lr0': 0.005
```

**Prevent overfitting:**
```python
# More augmentation
'degrees': 15.0
'translate': 0.2

# Dropout (nếu có)
'dropout': 0.1
```

**Faster training:**
```python
# Cache images to RAM
'cache': True

# Increase batch size (if GPU allows)
'batch': 32

# Use more workers
'workers': 8
```

---

## 📊 PHẦN 3: Validation & Testing

### 3.1. Validation Script

Tạo file `validate_model.py`:

```python
"""
Validate trained model on validation set
"""

from ultralytics import YOLO
import os


def validate_model():
    """Validate model on val dataset"""
    
    print("="*70)
    print("MODEL VALIDATION")
    print("="*70)
    
    # Load best model
    model_path = "runs/train/ballot_cross/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("   Run training first: python train_model.py")
        return
    
    print(f"\n📦 Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Validate
    print("\n🔍 Running validation...")
    results = model.val(
        data='dataset/data.yaml',
        split='val',
        imgsz=640,
        batch=16,
        conf=0.25,
        iou=0.6,
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    
    # Print metrics
    print("\n" + "="*70)
    print("📊 VALIDATION RESULTS")
    print("="*70)
    
    print(f"\nmAP50: {results.box.map50:.4f}")
    print(f"mAP50-95: {results.box.map:.4f}")
    print(f"Precision: {results.box.mp:.4f}")
    print(f"Recall: {results.box.mr:.4f}")
    
    # Interpretation
    print("\n💡 Interpretation:")
    
    map50 = results.box.map50
    if map50 > 0.9:
        print("   ✅ EXCELLENT - Model rất tốt!")
    elif map50 > 0.8:
        print("   ✅ GOOD - Model tốt, có thể dùng production")
    elif map50 > 0.6:
        print("   ⚠️  OK - Model tạm được, nên cải thiện")
    else:
        print("   ❌ POOR - Model chưa tốt, cần train lại")
        print("      Suggestions:")
        print("      - Thu thập thêm ảnh")
        print("      - Label chính xác hơn")
        print("      - Tăng epochs hoặc dùng model lớn hơn")
    
    return results


if __name__ == "__main__":
    import torch
    validate_model()
```

```bash
# Chạy validation
python validate_model.py
```

---

### 3.2. Test Với Ảnh Mới

Tạo file `test_model.py`:

```python
"""
Test model with new images
"""

from ultralytics import YOLO
import cv2
import os


def test_on_images(model_path, image_folder):
    """Test model on folder of images"""
    
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Get all images
    images = [f for f in os.listdir(image_folder) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"\nTesting on {len(images)} images...")
    
    for img_name in images:
        img_path = os.path.join(image_folder, img_name)
        
        # Predict
        results = model(img_path, conf=0.5)
        
        # Draw results
        annotated = results[0].plot()
        
        # Show
        cv2.imshow(f"Test: {img_name}", annotated)
        key = cv2.waitKey(0)
        
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test
    model_path = "runs/train/ballot_cross/weights/best.pt"
    image_folder = "dataset/images/test/"
    
    test_on_images(model_path, image_folder)
```

```bash
# Test
python test_model.py
```

---

## 📦 PHẦN 4: Deploy Model

### 4.1. Copy Model Vào Project

```bash
# Copy best.pt vào models/
cp runs/train/ballot_cross/weights/best.pt models/best.pt

# Verify
ls -lh models/best.pt
# Should see: ~6-12 MB file
```

---

### 4.2. Test With App

```bash
# Test model trong app
python step3_ui_app.py

# Nếu model tốt → Tiếp tục BƯỚC 4 (Optimization & Packaging)
```

---

## 🔧 PHẦN 5: Troubleshooting

### Issue 1: mAP thấp (<0.6)

**Nguyên nhân:**
- Dataset nhỏ (<100 ảnh)
- Label không chính xác
- Ảnh chất lượng kém
- Hyperparameters chưa tốt

**Fix:**
```
1. Thu thập thêm ảnh (goal: 500+)
2. Re-label với Label Studio/Roboflow
3. Increase epochs: 200-300
4. Dùng model lớn hơn: yolov8m.pt
```

---

### Issue 2: Overfitting

**Triệu chứng:** Train loss giảm nhưng val loss tăng

**Fix:**
```python
# Augmentation
'degrees': 20.0
'translate': 0.2
'scale': 0.7

# Early stopping
'patience': 15
```

---

### Issue 3: GPU Out of Memory

**Fix:**
```python
# Giảm batch size
'batch': 8  # Hoặc 4

# Giảm image size (không khuyến nghị)
'imgsz': 320
```

---

### Issue 4: Training quá chậm (CPU)

**Fix:**
```
1. Dùng Google Colab (Free GPU)
2. Giảm epochs: 50-80
3. Cache images: 'cache': True
4. Dùng yolov8n (nano - fastest)
```

---

## 📚 Google Colab Training (Free GPU)

### Colab Notebook

```python
# Install ultralytics
!pip install ultralytics

# Upload dataset
from google.colab import drive
drive.mount('/content/drive')

# Or upload via Colab files
!unzip dataset.zip

# Train
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model.train(
    data='/content/dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# Download best.pt
from google.colab import files
files.download('runs/train/exp/weights/best.pt')
```

**Link Colab template:** https://colab.research.google.com/github/ultralytics/ultralytics/blob/main/examples/tutorial.ipynb

---

## 🎯 Summary Checklist

### Chuẩn Bị Dataset
- [ ] Thu thập 100-500 ảnh phiếu bầu
- [ ] Label/annotate với Label Studio hoặc Roboflow
- [ ] Tạo data.yaml
- [ ] Split train/val/test (70/15/15)

### Training
- [ ] Cài ultralytics: `pip install ultralytics`
- [ ] Tạo train_model.py
- [ ] Chạy training: `python train_model.py`
- [ ] Monitor với TensorBoard
- [ ] Đợi 100 epochs (~30-60 phút GPU)

### Validation
- [ ] Chạy validation: `python validate_model.py`
- [ ] Check mAP50 > 0.8
- [ ] Test với ảnh mới: `python test_model.py`

### Deploy
- [ ] Copy best.pt → models/best.pt
- [ ] Test trong app: `python step3_ui_app.py`
- [ ] ✅ Model ready cho BƯỚC 1-4!

---

## 📖 Resources

- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **Label Studio:** https://labelstud.io/
- **Roboflow:** https://roboflow.com/
- **YOLO Format:** https://docs.ultralytics.com/datasets/detect/
- **Google Colab:** https://colab.research.google.com/

---

**Sau khi hoàn tất BƯỚC 0, bạn sẽ có file `models/best.pt` để dùng cho BƯỚC 1-4! 🚀**
