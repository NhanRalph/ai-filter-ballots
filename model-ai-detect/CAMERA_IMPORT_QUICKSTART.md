# 🚀 Quick Start: Camera & Import

## TL;DR - Bắt Đầu Nhanh

### ✅ Camera Hoạt Động?

```bash
# Test camera trước
python test_camera.py

# Chọn: 1 (Scan cameras)
# Xem camera nào available → Note lại số
```

### ✅ Chạy App

```bash
python step3_ui_app.py

# Chọn camera từ dropdown (0, 1, 2, 3...)
# Click "🎥 Bật Camera"
```

### ❌ Camera KHÔNG Hoạt Động?

**→ Dùng Import Folder:**

```bash
1. Chụp ảnh phiếu bằng điện thoại/camera
2. Copy vào máy: C:/PhieuBau/
3. Mở app → Click "📁 Import Folder"
4. Chọn folder C:/PhieuBau/
5. Đợi xử lý → Xuất Excel
```

---

## 📹 Camera Issues - Giải Quyết Nhanh

### Issue 1: "Không thể mở camera"

**Fix nhanh:**
```
1. Thử Camera 1, 2, 3... từ dropdown
2. App có auto-detect → Sẽ tự hỏi dùng camera nào
3. Vẫn lỗi? → Dùng Import Folder
```

### Issue 2: Camera mở nhưng không có hình

**Fix:**
```
1. Test với Windows Camera app
   Start Menu → "Camera"
   
2. Nếu Windows Camera OK:
   → Restart app
   → Thử camera ID khác
   
3. Nếu Windows Camera lỗi:
   → Update driver (Device Manager)
   → Restart máy
```

### Issue 3: Muốn dùng USB webcam

**Setup:**
```
1. Cắm USB webcam
2. Đợi 30 giây (Windows cài driver)
3. Test:
   python test_camera.py
   
4. Mở app → Chọn Camera 1 hoặc Camera 2
```

### Issue 4: Muốn dùng điện thoại làm webcam

**DroidCam (Khuyến nghị):**
```
1. Download DroidCam Client (PC):
   https://www.dev47apps.com/droidcam/windows/
   
2. Download DroidCam app (Phone):
   Play Store / App Store
   
3. Kết nối USB hoặc WiFi
   
4. Start DroidCam → Xuất hiện như Camera 1/2
   
5. Mở app → Chọn Camera 1 hoặc 2
```

📖 **Chi tiết:** CAMERA_SETUP_GUIDE.md

---

## 📁 Import Folder - Workflow

### Khi Nào Dùng?

✅ Camera không hoạt động  
✅ Có nhiều ảnh đã chụp sẵn (10-1000+)  
✅ Muốn xử lý nhanh hàng loạt  
✅ Offline: Chụp trước, xử lý sau  

### Các Bước:

```
┌─────────────────────────────────────┐
│  1. CHỤP ẢNH                        │
│     Camera/Điện thoại → Chụp phiếu  │
│     Đủ sáng, rõ nét, góc vuông      │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  2. COPY ẢNH VÀO MÁY                │
│     USB/AirDrop/Email → Folder      │
│     Ví dụ: C:/PhieuBau/             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  3. MỞ APP                          │
│     python step3_ui_app.py          │
│     Click "📁 Import Folder"        │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  4. CHỌN FOLDER                     │
│     Browse → C:/PhieuBau/           │
│     Xác nhận: "Xử lý 150 ảnh?"      │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  5. ĐỢI XỬ LÝ                       │
│     Progress: 45/150 ảnh            │
│     ~1.5s/ảnh → 100 ảnh = 2.5 phút │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  6. XUẤT KẾT QUẢ                    │
│     Click "💾 Xuất Excel"           │
│     Lưu file → Hoàn tất!            │
└─────────────────────────────────────┘
```

### Formats Hỗ Trợ:

```
✅ .jpg, .jpeg  ← Khuyến nghị (nhỏ, phổ biến)
✅ .png         ← OK (lớn hơn jpg)
✅ .bmp         ← OK (rất lớn)
✅ .JPG, .JPEG  ← Uppercase cũng OK
```

### Folder Structure:

```
Option A: Flat (tất cả trong 1 folder)
C:/PhieuBau/
├── IMG_001.jpg
├── IMG_002.jpg
├── ...
└── IMG_150.jpg
✅ Đơn giản nhất

Option B: Subfolder (chia theo nhóm)
C:/PhieuBau/
├── batch1/
│   ├── IMG_001.jpg
│   └── IMG_002.jpg
├── batch2/
│   ├── IMG_003.jpg
│   └── IMG_004.jpg
└── backup/
    └── IMG_005.jpg
✅ App tự động tìm trong tất cả subfolder
```

### Performance:

| Số ảnh | Thời gian | RAM | CPU |
|--------|-----------|-----|-----|
| 10     | ~15s      | 1GB | 50% |
| 50     | ~1.5 phút | 1.5GB | 60% |
| 100    | ~2.5 phút | 2GB | 70% |
| 500    | ~12 phút  | 3GB | 80% |
| 1000   | ~25 phút  | 4GB | 90% |

💡 **Tips:**
- Batch < 500 ảnh: OK
- Batch > 500: Chia nhỏ thành nhiều batch
- Đóng apps khác khi xử lý batch lớn

---

## 🎯 Decision Tree

```
Bạn muốn làm gì?
│
├─ Xử lý PH realtime (camera trực tiếp)
│  │
│  ├─ Camera hoạt động?
│  │  ├─ YES → Dùng Workflow 1 (Camera)
│  │  └─ NO → Fix camera hoặc dùng Import
│  │
│  └─ Có nhiều camera?
│     ├─ YES → Chọn từ dropdown (0,1,2,3)
│     └─ NO → Camera 0 (default)
│
└─ Xử lý phiếu đã chụp sẵn
   │
   ├─ Có bao nhiêu ảnh?
   │  │
   │  ├─ 1-10 ảnh → Dùng "📂 Mở 1 ảnh" (lặp lại)
   │  │
   │  └─ 10+ ảnh → Dùng "📁 Import Folder" (batch)
   │
   └─ Ảnh ở đâu?
      │
      ├─ Trong máy → Chọn folder trực tiếp
      │
      └─ Trong điện thoại
         └─ Copy vào máy trước (USB/AirDrop)
```

---

## 🔧 Troubleshooting Common Issues

### 1. Camera lag / FPS thấp

```
Fix:
- Đóng apps khác
- Giảm số ứng dụng đang chạy
- Dùng model ONNX (nhanh hơn)
- Upgrade RAM/CPU
```

### 2. Import folder: Một số ảnh bị lỗi

```
Normal: 1-2% ảnh lỗi là OK
Reasons:
- Ảnh corrupt
- Format không đúng
- Ảnh quá mờ/tối

Fix:
- Check log để xem ảnh nào lỗi
- Chụp lại ảnh đó
```

### 3. Progress window bị đơ

```
App vẫn đang chạy trong background!
Đừng tắt, đợi thêm vài phút.

Check:
- Task Manager → CPU usage
- Nếu CPU ~70% → App đang xử lý
- Nếu CPU ~0% → App bị crash → Restart
```

### 4. Out of memory khi import lớn

```
Fix:
1. Đóng apps khác
2. Chia nhỏ batch:
   - Thay vì 1000 ảnh 1 lần
   - Import 200 ảnh x 5 lần
3. Restart app sau mỗi batch
```

---

## 📚 Resources

- **CAMERA_SETUP_GUIDE.md** - Chi tiết về kết nối camera ngoài
- **README_STEP3.md** - Documentation đầy đủ UI app
- **USER_GUIDE.md** - Hướng dẫn người dùng cuối
- **test_camera.py** - Test script cho camera

---

## 💬 Support

**Camera issues?**
```
1. Chạy: python test_camera.py
2. Screenshot kết quả
3. Gửi kèm:
   - Camera type (built-in/USB/DroidCam)
   - Windows version
   - Error message
```

**Batch import issues?**
```
1. Số ảnh trong folder?
2. Số ảnh thành công/lỗi?
3. File format?
4. Screenshot progress window
```

---

**Chúc bạn sử dụng hiệu quả! 🎉**
