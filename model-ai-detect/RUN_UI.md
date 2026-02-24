# 🚀 CHẠY GIAO DIỆN UI - HƯỚNG DẪN NHANH

## ✅ BƯỚC 3 đã hoàn thành!

Hệ thống giờ đã có giao diện UI đầy đủ với CustomTkinter.

---

## 🎯 3 cách test UI:

### 1️⃣ Demo UI (Không cần model) - TEST NGAY!

```bash
python demo_step3.py
```

**Mô tả:**
- UI đầy đủ với dữ liệu giả lập
- Xem layout và flow hoạt động
- Không cần model `best.pt`
- Click "Tạo Phiếu Demo" để xem kết quả mẫu

**Thời gian:** < 5 giây

---

### 2️⃣ Ứng dụng chính (Cần model)

```bash
# Đảm bảo có file: models/best.pt
python step3_ui_app.py
```

**Mô tả:**
- UI thật với AI detection
- Camera real-time
- Xử lý phiếu bầu thật
- Xuất Excel đầy đủ

**Yêu cầu:** Model `best.pt` phải có trong `models/`

---

### 3️⃣ Command Line (Alternative)

```bash
python full_pipeline.py
```

**Mô tả:**
- Không có UI đồ họa
- Menu text-based
- Phù hợp cho batch processing

---

## 📸 Tính năng UI chính:

### Panel bên trái - Camera Preview:
```
📹 Camera Preview
- Hiển thị video real-time
- Vẽ 5 vùng ROI tự động
- FPS ~15-20

Nút điều khiển:
🎥 Bật Camera     - Mở camera
📸 Chụp & Phân tích - Analyze phiếu hiện tại
📂 Mở ảnh         - Load ảnh từ file
```

### Panel bên phải - Control Panel:
```
📊 THỐNG KÊ
- Tổng số phiếu
- Phiếu hợp lệ (màu xanh)
- Phiếu không hợp lệ (màu đỏ)

👥 KẾT QUẢ ỨNG VIÊN
- 5 ứng viên
- Số phiếu mỗi người
- Tỷ lệ % realtime

Nút chức năng:
💾 Xuất Excel    - Xuất 3 sheets
🔄 Reset Dữ liệu - Xóa tất cả
⚙️ Cài đặt       - ROI & Confidence
```

### Status Bar (dưới cùng):
```
🟢 Trạng thái hiện tại     │     2026-02-25 10:30:45
```

---

## 🎨 Workflow sử dụng:

### Workflow Camera Real-time:
```
1. Chạy: python step3_ui_app.py
2. Click "🎥 Bật Camera"
3. Đặt phiếu bầu trước camera
4. Click "📸 Chụp & Phân tích"
5. Xem kết quả trong popup
6. Lặp lại 3-5 cho các phiếu khác
7. Click "💾 Xuất Excel"
```

### Workflow File ảnh:
```
1. Chạy: python step3_ui_app.py
2. Click "📂 Mở ảnh"
3. Chọn file ảnh phiếu bầu
4. Xem kết quả
5. Lặp lại 2-4 cho các ảnh khác
6. Click "💾 Xuất Excel"
```

---

## ⚙️ Settings (Cài đặt):

Click nút "⚙️ Cài đặt" để điều chỉnh:

### ROI Layout:
- **HORIZONTAL**: Chia 5 vùng ngang (← →)
- **VERTICAL**: Chia 5 vùng dọc (↑ ↓)

### Confidence Threshold:
- Slider điều chỉnh 0.1 - 0.9
- Giá trị thấp: Nhạy hơn (có thể nhận sai)
- Giá trị cao: Chính xác hơn (có thể bỏ sót)
- Mặc định: **0.5**

Click "Áp dụng" để lưu thay đổi.

---

## 🗂️ File Excel Output:

Khi click "💾 Xuất Excel", file bao gồm:

### Sheet 1: Chi tiết phiếu
```
STT | ID Phiếu | Thời gian | Người 1 | Người 2 | ... | Trạng thái
 1  | PHIEU_0001 | 10:30:00 |    X    |         | ... | Hợp lệ
```
**X** = Được bầu

### Sheet 2: Thống kê
```
Chỉ số              | Giá trị
Tổng số phiếu       | 10
Phiếu hợp lệ        | 8
Phiếu không hợp lệ  | 2
```

### Sheet 3: Kết quả ứng viên
```
Thứ hạng | Tên         | Số phiếu | Tỷ lệ
   1     | Lê Văn C    |    6     | 75.00%
   2     | Trần Thị B  |    5     | 62.50%
```

---

## 💡 Tips:

### Để có kết quả tốt nhất:

1. **Ánh sáng**: Camera cần đủ sáng
2. **Góc nhìn**: Phiếu đặt song song camera
3. **Khoảng cách**: Khoảng 30-50cm
4. **Ổn định**: Giữ phiếu không rung
5. **ROI Layout**: Chọn phù hợp với phiếu của bạn

### Xử lý lỗi:

**❌ Camera không mở:**
- Kiểm tra quyền truy cập camera
- Đóng các app khác đang dùng camera
- Thử camera ID khác (trong code)

**❌ Model không load:**
- Kiểm tra file `models/best.pt` có tồn tại
- Xem log lỗi trong terminal
- Kiểm tra đường dẫn trong `config.py`

**⚠️ Phát hiện không chính xác:**
- Giảm Confidence Threshold xuống 0.3-0.4
- Kiểm tra ROI Layout
- Cải thiện ánh sáng
- Train lại model với data tốt hơn

---

## 📊 Performance:

- **Startup**: ~2-3 giây (load model lần đầu)
- **Camera FPS**: 15-20 FPS
- **Analyze**: ~1-2 giây/phiếu (tùy máy)
- **Export Excel**: < 1 giây (100 phiếu)

---

## 🎯 So sánh 3 cách:

| Feature | Demo UI | UI Chính | Command Line |
|---------|---------|----------|--------------|
| Cần model | ❌ | ✅ | ✅ |
| Giao diện | ✅ | ✅ | ❌ |
| Camera | Giả lập | ✅ | ✅ |
| Excel | Giả lập | ✅ | ✅ |
| Batch | ❌ | ❌ | ✅ |
| Dễ dùng | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 📝 Checklist trước khi chạy:

### Demo UI (demo_step3.py):
- [ ] Python đã cài
- [ ] `pip install customtkinter` đã chạy
- [ ] Chạy: `python demo_step3.py`

### UI Chính (step3_ui_app.py):
- [ ] Python đã cài
- [ ] Tất cả thư viện đã cài (`requirements.txt`)
- [ ] File `models/best.pt` đã có
- [ ] Chạy: `python step3_ui_app.py`

---

## 🎉 Xong BƯỚC 3!

Hệ thống giờ đã hoàn chỉnh với:
- ✅ BƯỚC 1: ROI Detection
- ✅ BƯỚC 2: Classification & Excel
- ✅ BƯỚC 3: Giao diện UI

**Tiếp theo:** BƯỚC 4 - Tối ưu & Đóng gói .exe

Yêu cầu AI: **"Tiếp tục BƯỚC 4"**

---

## 🆘 Cần trợ giúp?

1. Đọc [README_STEP3.md](README_STEP3.md) - Chi tiết đầy đủ
2. Đọc [README.md](README.md) - Tổng quan
3. Chạy demo để xem UI trước
4. Test với ảnh trước khi dùng camera

---

**Happy Coding! 🚀**
