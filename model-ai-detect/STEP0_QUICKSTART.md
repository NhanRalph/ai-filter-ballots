# 🎓 BƯỚC 0: TRAINING QUICK START

## 📋 Tóm tắt Nhanh

BƯỚC 0 là bước **BẮT BUỘC** trước khi chạy BƯỚC 1-4. Bạn cần train model YOLOv8 để detect dấu X trên phiếu bầu.

**Kết quả:** File `models/best.pt` (model trained)

**Thời gian:** 30-60 phút (GPU) hoặc 3-5 giờ (CPU)

---

## 🚀 Quick Start (5 Steps)

### Step 1: Thu thập ảnh (15-30 phút)

**Minimum:** 100 ảnh  
**Recommend:** 500+ ảnh

```bash
# Chụp/scan phiếu bầu với dấu X
# - Độ phân giải: 640x640+ pixels
# - Format: JPG, PNG
# - Đa dạng: Các loại dấu X khác nhau
```

**Tips:**
- Dùng smartphone chụp: 10-15 phiếu/phút
- Hoặc scan nhiều phiếu: Nhanh hơn
- Ảnh rõ, không bị mờ, nghiêng

---

### Step 2: Gán nhãn (30-60 phút cho 100 ảnh)

**Option A: Label Studio (Khuyến nghị - Free, Local)**

```bash
# Install
pip install label-studio

# Start
label-studio start
# Browser tự mở: http://localhost:8080
```

**Workflow:**
1. Create project "Ballot Cross Detection"
2. Import ảnh
3. Template: Object Detection with Bounding Boxes
4. Vẽ box quanh mỗi dấu X
5. Export → YOLO format
6. Copy vào `dataset/labels/train/`

**Option B: Roboflow (Dễ nhất - Cloud)**

1. Đăng ký: https://roboflow.com/ (Free)
2. Create project
3. Upload ảnh → Annotate online
4. Export: YOLOv8 format
5. Download → Tự động có structure đúng

---

### Step 3: Chuẩn bị dataset (5 phút)

```bash
# Chia ảnh theo tỷ lệ 70:15:15
cp dataset_raw/*.jpg dataset/images/train/   # 70 ảnh
cp dataset_raw/*.jpg dataset/images/val/     # 15 ảnh
cp dataset_raw/*.jpg dataset/images/test/    # 15 ảnh

# Copy labels tương ứng
cp labels_raw/*.txt dataset/labels/train/
cp labels_raw/*.txt dataset/labels/val/
cp labels_raw/*.txt dataset/labels/test/
```

**Check:**
- [ ] `dataset/data.yaml` có sẵn ✅
- [ ] Mỗi ảnh .jpg có file .txt tương ứng
- [ ] Format file .txt: `0 x_center y_center width height`

---

### Step 4: Training (30-60 phút GPU)

```bash
python train_model.py
```

**Interactive menu:**
```
Chọn cấu hình training:

1. Quick (Fast training)
   - Model: yolov8n (Nano)
   - Epochs: 50
   - Time: ~15-30 phút (GPU)

2. Standard (Khuyến nghị)     ← CHỌN NÀY
   - Model: yolov8n (Nano)
   - Epochs: 100
   - Time: ~30-60 phút (GPU)

3. High Quality
   - Model: yolov8m (Medium)
   - Epochs: 200
   - Time: ~2-3 giờ (GPU)
```

**Chọn 2 (Standard)** → Enter → Enter → Enter → y

**Monitor training:**
```bash
# Terminal khác
tensorboard --logdir runs/train
# Mở browser: http://localhost:6006
```

**⚠️ Nếu không có GPU:**
```
# Dùng Google Colab (Free GPU)
# Xem: README_STEP0_TRAINING.md, section "Google Colab"
```

---

### Step 5: Validate & Test (5 phút)

```bash
# Validate model
python validate_model.py

# Kết quả mong muốn:
# mAP50: > 0.8 (Good)
# mAP50: > 0.9 (Excellent)

# Test trên ảnh mới
python test_model.py
# Chọn mode 1 (test single image)
```

**✅ Hoàn thành!**

Model đã được copy vào: `models/best.pt`

---

## 📊 Expected Results

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| mAP50 | 0.6 | 0.8 | 0.9+ |
| Precision | 0.7 | 0.8 | 0.9+ |
| Recall | 0.7 | 0.8 | 0.9+ |

**Nếu mAP50 < 0.8:**
- Thu thập thêm ảnh (500+)
- Re-label kỹ hơn
- Train lâu hơn (200 epochs)
- Dùng model lớn hơn (yolov8m)

---

## 🔧 Troubleshooting

### ❓ "Không có GPU, training chậm quá"

**Giải pháp:** Google Colab (Free GPU)

1. Mở: https://colab.research.google.com/
2. Runtime → Change runtime type → GPU
3. Upload dataset lên Google Drive
4. Xem code: README_STEP0_TRAINING.md, section "Google Colab"

### ❓ "Training bị lỗi CUDA out of memory"

```bash
# Giảm batch size
python train_model.py
# Chọn 4 (Custom)
# Batch size: 8 (hoặc 4)
```

### ❓ "mAP50 quá thấp (<0.6)"

**Nguyên nhân:**
- Dataset quá ít (< 100 ảnh)
- Label sai
- Epochs quá ít
- Data không đa dạng

**Giải pháp:**
1. Thu thập thêm ảnh (goal: 500+)
2. Re-check labels (xem EXAMPLE_LABEL_FORMAT.txt)
3. Train lại với 200 epochs
4. Augmentation mạnh hơn

### ❓ "Model overfitting (train tốt, val kém)"

```python
# Edit train_model.py, tăng augmentation:
'hsv_s': 0.9,      # Tăng từ 0.7
'degrees': 15.0,   # Tăng từ 10.0
'patience': 30,    # Tăng từ 20
```

---

## ⏭️ Next Steps

**Sau khi có models/best.pt:**

```bash
# BƯỚC 1: Test ROI detection
python step1_roi_detection.py

# BƯỚC 2: Test classification
python step2_ballot_classifier.py

# BƯỚC 3: Chạy UI app
python step3_ui_app.py

# BƯỚC 4: Optimize model
python step4_convert_model.py
```

---

## 📖 Full Documentation

Xem hướng dẫn đầy đủ: **[README_STEP0_TRAINING.md](README_STEP0_TRAINING.md)**

- Dataset preparation chi tiết
- Label format specification
- Training hyperparameters
- Google Colab notebook
- Troubleshooting đầy đủ
- Performance optimization

---

## 📞 Quick Reference

| Task | Command | Time |
|------|---------|------|
| Install | `pip install ultralytics label-studio` | 2 min |
| Annotate | `label-studio start` | 30-60 min |
| Train | `python train_model.py` | 30-60 min |
| Validate | `python validate_model.py` | 1 min |
| Test | `python test_model.py` | 2 min |

**Total time: 1-2 giờ** (có GPU) hoặc **4-6 giờ** (CPU)

---

## ✅ Checklist

Trước khi chuyển sang BƯỚC 1, check:

- [ ] Dataset có 100+ ảnh
- [ ] Mỗi ảnh có file .txt label
- [ ] Training completed (100 epochs)
- [ ] mAP50 > 0.8
- [ ] File `models/best.pt` exists
- [ ] Test model trên ảnh mới OK

**✅ All done?** → Chuyển sang BƯỚC 1!

```bash
python step3_ui_app.py
```
