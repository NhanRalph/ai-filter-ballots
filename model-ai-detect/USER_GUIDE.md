# Hướng Dẫn Sử Dụng Hệ Thống Xác Minh Phiếu Bầu

## 📖 Mục Lục

1. [Giới Thiệu](#giới-thiệu)
2. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
3. [Cài Đặt](#cài-đặt)
4. [Sử Dụng](#sử-dụng)
5. [Khắc Phục Sự Cố](#khắc-phục-sự-cố)
6. [Câu Hỏi Thường Gặp](#câu-hỏi-thường-gặp)

---

## Giới Thiệu

**Hệ Thống Xác Minh Phiếu Bầu** là ứng dụng tự động phát hiện và kiểm tra tính hợp lệ của phiếu bầu bằng trí tuệ nhân tạo (AI).

### Tính Năng Chính

✅ **Tự động phát hiện dấu X** trên phiếu bầu  
✅ **Xác định tính hợp lệ** theo quy tắc bầu cử  
✅ **Hỗ trợ nhiều nguồn**: Webcam hoặc file ảnh  
✅ **Xuất báo cáo Excel** chi tiết  
✅ **Thống kê real-time** số phiếu hợp lệ/không hợp lệ  
✅ **Giao diện đơn giản**, dễ sử dụng

### Quy Tắc Bầu Cử

Phiếu được chia thành **5 vùng ứng viên**:

| Dấu X | Ý Nghĩa |
|-------|---------|
| ❌ CÓ dấu X | Ứng viên bị **gạch bỏ** (KHÔNG được bầu) |
| ✅ KHÔNG có X | Ứng viên được **chọn** (được bầu) |

**Phiếu hợp lệ:**
- 4 dấu X = Bầu 1 người (1 ứng viên không có X)
- 3 dấu X = Bầu 2 người (2 ứng viên không có X)
- 2 dấu X = Bầu 3 người (3 ứng viên không có X)

**Phiếu không hợp lệ:**
- 0, 1, hoặc 5 dấu X = Vi phạm quy tắc

---

## Yêu Cầu Hệ Thống

### Phần Cứng

- **Hệ điều hành**: Windows 10 hoặc Windows 11 (64-bit)
- **RAM**: Tối thiểu 4GB, khuyến nghị 8GB
- **Ổ cứng**: 500MB dung lượng trống
- **Webcam**: Cần có nếu sử dụng chức năng camera (optional)
- **Màn hình**: Độ phân giải tối thiểu 1280x720

### Phần Mềm

- ✅ **Không cần cài Python**
- ✅ **Không cần cài thư viện**
- ✅ Ứng dụng standalone, chạy ngay

---

## Cài Đặt

### Cách 1: Từ File .exe (Khuyến Nghị)

1. **Tải về** file `BallotVerification_v1.0.zip`

2. **Giải nén** file zip
   - Right-click → Extract All...
   - Chọn thư mục đích

3. **Mở thư mục** `BallotVerification/`

4. **Chạy ứng dụng**
   - Double-click `BallotVerification.exe`
   - Nếu Windows SmartScreen cảnh báo:
     - Click "More info"
     - Click "Run anyway"

### Cách 2: Từ Installer (Nếu Có)

1. **Chạy** `BallotVerification_Setup.exe`
2. **Follow** wizard cài đặt
3. **Launch** từ Desktop hoặc Start Menu

---

## Sử Dụng

### Khởi Động

1. Double-click `BallotVerification.exe`
2. Ứng dụng sẽ mở ra với giao diện chính

### Giao Diện Chính

```
┌─────────────────────────────────────────┐
│  [Camera Preview]   │   [Control Panel] │
│                     │                   │
│                     │   Thống Kê:       │
│   [Video/Image]     │   - Tổng: 0       │
│                     │   - Hợp lệ: 0     │
│                     │   - Không hợp lệ: 0│
│                     │                   │
│  [Khởi động Camera] │   Kết quả:        │
│  [Chụp & Phân tích] │   - Ứng viên A: 0 │
│  [Tải ảnh]          │   - Ứng viên B: 0 │
│                     │   ...             │
│                     │                   │
│                     │   [Xuất Excel]    │
│                     │   [Reset]         │
│                     │   [Cài đặt]       │
└─────────────────────────────────────────┘
```

### Workflow 1: Sử Dụng Webcam

**Bước 0: Chọn Camera (nếu có nhiều camera)**
- Trên giao diện có dropdown "Camera"
- Chọn camera bạn muốn dùng:
  - **Camera 0 (Default)**: Webcam built-in của laptop
  - **Camera 1**: USB webcam ngoài thứ nhất
  - **Camera 2**: USB webcam ngoài thứ hai
  - **Camera 3**: Camera bổ sung
- **Không biết camera nào?** → Thử lần lượt từ Camera 0, nếu lỗi thử Camera 1, 2, 3...

**Bước 1: Khởi động Camera**
- Click nút **"🎥 Bật Camera"**
- **Nếu camera không mở:**
  - Ứng dụng sẽ tự động tìm các camera khác (0-4)
  - Hiển thị dialog hỏi bạn có muốn dùng camera tìm được không
  - Nếu không tìm thấy → Xem [Khắc Phục Sự Cố: Camera](#camera-không-hoạt-động)
- Camera sẽ bắt đầu hiển thị preview
- Các vùng ROI (5 ứng viên) được hiển thị bằng khung màu xanh

**Bước 2: Đặt Phiếu Bầu**
- Đặt phiếu bầu trước camera (30-50cm)
- Đảm bảo phiếu nằm trong khung hình
- Phiếu phẳng, không nhăn
- Ánh sáng đầy đủ, không chói, không bị mờ/nhòe

**Bước 3: Chụp & Phân Tích**
- Click nút **"📸 Chụp & Phân tích"**
- Hệ thống sẽ:
  - Phát hiện các dấu X trên phiếu
  - Xác định phiếu hợp lệ/không hợp lệ
  - Cập nhật thống kê
  - Hiển thị kết quả trong popup

**Bước 4: Lặp Lại**
- Tiếp tục với phiếu bầu tiếp theo
- Thống kê tự động cập nhật

**Bước 5: Xuất Kết Quả**
- Click nút **"💾 Xuất Excel"**
- Chọn vị trí lưu file
- File Excel sẽ được tạo với 3 sheets:
  - **Chi tiết phiếu**: Danh sách tất cả phiếu
  - **Thống kê**: Tổng hợp số liệu
  - **Kết quả ứng viên**: Số phiếu của từng người

### Workflow 2: Sử Dụng File Ảnh

**Bước 1: Tải Ảnh**
- Click nút **"📂 Mở 1 ảnh"**
- Chọn file ảnh phiếu bầu (JPG, PNG, BMP)

**Bước 2: Phân Tích**
- Ảnh sẽ tự động được phân tích
- Kết quả hiện trong popup
- Thống kê tự động cập nhật

**Bước 3: Lặp Lại**
- Tải thêm ảnh khác
- Hoặc chuyển sang dùng camera

**Bước 4: Xuất Kết Quả**
- Click nút **"💾 Xuất Excel"**
- Chọn vị trí lưu

### Workflow 3: Batch Import - Xử Lý Nhiều Ảnh Cùng Lúc

**Khi nào dùng Batch Import?**
- ✅ Có nhiều ảnh phiếu đã chụp sẵn (10-1000+ ảnh)
- ✅ Camera không hoạt động, đã chụp bằng điện thoại/camera khác
- ✅ Muốn xử lý nhanh hàng loạt
- ✅ Ảnh được lưu trong một folder

**Bước 1: Chuẩn Bị Ảnh**
- Chụp tất cả phiếu bằng camera/điện thoại
- Copy ảnh vào máy tính
- Đặt trong một folder (ví dụ: `C:/PhieuBau/`)
- Có thể có subfolder (app tự động tìm)

**Bước 2: Import Folder**
- Click nút **"📁 Import Folder"**
- Chọn folder chứa ảnh phiếu bầu
- Ứng dụng sẽ tự động scan tất cả ảnh (.jpg, .jpeg, .png, .bmp)

**Bước 3: Xác Nhận**
- Dialog hiển thị: *"Tìm thấy 150 ảnh trong folder. Bạn có muốn xử lý tất cả?"*
- Click **"Yes"** để bắt đầu

**Bước 4: Theo Dõi Tiến Độ**
- Cửa sổ Progress hiển thị:
  - Số ảnh đang xử lý: "45/150 ảnh"
  - Thanh tiến độ (progress bar)
  - Số ảnh thành công / lỗi: "✅ 44 | ❌ 1"
- Thời gian: ~1.5 giây/ảnh
  - 10 ảnh: ~15 giây
  - 100 ảnh: ~2.5 phút
  - 500 ảnh: ~12 phút

**Bước 5: Hoàn Tất**
- Dialog kết quả: *"Hoàn tất xử lý 150 ảnh! ✅ Thành công: 148 | ❌ Lỗi: 2"*
- Thống kê tự động cập nhật
- Click **"💾 Xuất Excel"** để lưu kết quả

**Ví dụ thực tế:**
```
Folder structure:
C:/PhieuBau/
├── IMG_001.jpg
├── IMG_002.jpg
├── IMG_003.jpg
├── ...
├── IMG_150.jpg
└── backup/
    ├── IMG_151.jpg  ← App cũng tìm trong subfolder
    └── IMG_152.jpg

Kết quả:
→ Tìm thấy 152 ảnh
→ Xử lý trong ~4 phút
→ Xuất Excel với 152 phiếu
```

### Workflow 4: Batch Processing (Nhiều Ảnh Cùng Lúc)

**Ghi chú:** Chức năng này chỉ có trong command-line interface

```bash
# Chạy từ terminal/command prompt
cd BallotVerification/
./full_pipeline.exe

# Chọn option 2: Process folder
# Nhập đường dẫn folder chứa ảnh
```

---

## Cài Đặt (Settings)

Click nút **"Cài đặt"** để điều chỉnh:

### 1. ROI Layout

Chọn cách chia vùng phiếu bầu:

- **HORIZONTAL**: 5 vùng ngang (mặc định)
  ```
  ┌─────────┐
  │ Ứng viên A │
  ├─────────┤
  │ Ứng viên B │
  ├─────────┤
  │ ...     │
  └─────────┘
  ```

- **VERTICAL**: 5 vùng dọc
  ```
  ┌──┬──┬──┬──┬──┐
  │A │B │C │D │E │
  └──┴──┴──┴──┴──┘
  ```

### 2. Confidence Threshold

Điều chỉnh độ nhạy phát hiện dấu X:

- **Thấp (0.3)**: Phát hiện nhiều hơn, có thể nhầm
- **Trung bình (0.5)**: Cân bằng (mặc định)
- **Cao (0.7)**: Chỉ phát hiện khi chắc chắn

**Lưu ý:** Sau khi thay đổi, nhấn "Lưu" và khởi động lại ứng dụng.

---🎥 Bật Camera" nhưng không có hình hoặc báo lỗi

**Giải Pháp:**

**1. Thử Camera Devices Khác:**
```
1. Chọn "Camera 1" từ dropdown
2. Click "🎥 Bật Camera"
3. Nếu lỗi → Thử Camera 2, Camera 3...
4. App có auto-detect → Sẽ tự động hỏi dùng camera nào nếu tìm thấy
```

**2. Kiểm Tra Webcam:**
- ✅ Webcam đã cắm USB? (nếu dùng USB webcam)
- ✅ Webcam đang được dùng bởi app khác?
  - Đóng: Zoom, Teams, Skype, Discord, OBS
  - Đóng: Browser tabs có video call (Google Meet, Messenger)
- ✅ Thử mở **Camera app** của Windows để test:
  - Start Menu → gõ "Camera" → Mở app
  - Nếu Windows Camera app OK → Vấn đề ở app
  - Nếu Windows Camera lỗi → Vấn đề driver/hardware

**3. Kiểm Tra Quyền:**
```
Windows 11/10:
Settings > Privacy > Camera
→ Bật "Allow apps to access camera"
→ Scroll xuống → Bật cho "Desktop apps"
```

**4. Kết Nối USB Webcam Ngoài:**
```
Nếu dùng webcam USB:
1. Cắm webcam vào cổng USB
2. Đợi Windows cài driver (~30 giây)
3. Kiểm tra Device Manager:
   - Win + X → Device Manager
   - Tìm "Cameras" hoặc "Imaging devices"
   - Thấy webcam → OK
   - Có dấu ! vàng → Driver lỗi, cần update
4. Chạy lại app, chọn Camera 1 hoặc Camera 2
```

**5. Dùng Điện Thoại Làm Webcam (DroidCam):**
```
1. Download DroidCam Client: https://www.dev47apps.com/droidcam/windows/
2. Download app "DroidCam" trên điện thoại (Play Store/App Store)
3. Kết nối qua USB hoặc WiFi
4. DroidCam sẽ xuất hiện như Camera 1 hoặc Camera 2
5. Chọn camera đó trong app

📖 Chi tiết: Xem CAMERA_SETUP_GUIDE.md
```

**6. Phương Án Thay Thế:**
```
Nếu camera không hoạt động:
→ Dùng chức năng "📁 Import Folder"
→ Chụp ảnh phiếu bằng điện thoại/camera
→ Copy ảnh vào máy tính
→ Import cả folder để xử lý batch
```

**📚 Xem thêm:**
- [CAMERA_SETUP_GUIDE.md](CAMERA_SETUP_GUIDE.md) - Hướng dẫn chi tiết kết nối thiết bị camera ngoài------|------------|-----|------------|
| 1   | PH_001   | 14:30:15  | X            |            | X   | Hợp lệ - Bầu 2 người |
| 2   | PH_002   | 14:30:28  |              | X          | X   | Hợp lệ - Bầu 3 người |

- ✅ **KHÔNG có X** = Ứng viên được bầu
- ❌ **Có X** = Ứng viên bị gạch bỏ

#### Sheet 2: Thống kê

```
Tổng số phiếu:         100
Phiếu hợp lệ:          95   (95%)
Phiếu không hợp lệ:    5    (5%)

Phân loại phiếu hợp lệ:
- Bầu 1 người: 40
- Bầu 2 người: 35
- Bầu 3 người: 20
```

#### Sheet 3: Kết quả ứng viên

| Ứng viên | Số phiếu bầu | Tỷ lệ |
|----------|--------------|-------|
| Nguyễn Văn A | 65 | 68.4% |
| Trần Thị B   | 55 | 57.9% |
| ...          | ... | ... |

---

## Khắc Phục Sự Cố

### Ứng Dụng Không Khởi Động

**Triệu chứng:** Double-click .exe không có gì xảy ra

**Giải pháp:**
1. Check Windows SmartScreen: Click "More info" → "Run anyway"
2. Check antivirus: Whitelist ứng dụng
3. Chạy as Administrator: Right-click → "Run as administrator"
4. Kiểm tra log file: `BallotVerification/logs/app.log`

### Camera Không Hoạt Động

**Triệu chứng:** Nhấn "Khởi động Camera" nhưng không có hình

**Giải pháp:**
1. **Kiểm tra webcam:**
   - Webcam đã cắm USB?
   - Webcam đang được dùng bởi app khác? (Zoom, Teams...)
   - Thử mở Camera app của Windows để test

2. **Thử camera khác:**
   - Settings → Chọn Camera Index khác (0, 1, 2...)

3. **Phân quyền:**
   - Windows Settings → Privacy → Camera
   - Bật "Allow apps to access camera"

### Model Không Load Được

**Triệu chứng:** Lỗi "Cannot find model" hoặc "Model load failed"

**Giải pháp:**
1. Kiểm tra file model tồn tại:
   - `BallotVerification/models/best.pt`
   - Hoặc `BallotVerification/models/best.onnx`

2. Kiểm tra permissions:
   - Đảm bảo folder có quyền read

3. Re-extract:
   - Giải nén lại file .zip, có thể bị corrupt

### Phát Hiện Không Chính Xác

**Triệu chứng:** Hệ thống không nhận diện hoặc nhận sai

**Giải pháp:**
1. **Cải thiện điều kiện chụp:**
   - Ánh sáng đầy đủ, không bóng đổ
   - Camera ổn định, không rung
   - Phiếu phẳng, không nhăn
   - Đủ gần để thấy rõ dấu X

2. **Điều chỉnh settings:**
   - Giảm Confidence Threshold xuống 0.3-0.4
   - Thử đổi ROI Layout

3. **Kiểm tra định dạng phiếu:**
   - Đảm bảo phiếu giống với format train model
   - 5 vùng ứng viên rõ ràng

### Excel Export Lỗi

**Triệu chứng:** Nhấn "Xuất Excel" báo lỗi

**Giải pháp:**
1. **File đang mở:**
   - Đóng Excel nếu đang mở file output
   - Chọn tên file khác

2. **Không có quyền ghi:**
   - Chọn folder khác (Desktop, Documents)
   - Chạy app as Administrator

3. **Disk full:**
   - Kiểm tra dung lượng ổ đĩa

### Ứng Dụng Chạy Chậm

**Triệu chứng:** Lag, inference lâu

**Giải pháp:**
1. **Đóng apps khác** đang chạy

2. **Sử dụng ONNX model** (nhanh hơn PyTorch):
   - Liên hệ admin để cập nhật

3. **Giảm resolution camera:**
   - Settings → Camera Resolution → Thấp hơn

4. **Upgrade hardware:**
   - RAM: 8GB+ khuyến nghị
   - CPU: Intel i5+ hoặc AMD Ryzen 5+

---

## Câu Hỏi Thường Gặp

### Q1: Ứng dụng có cần Internet không?

**A:** Không. Ứng dụng hoạt động **hoàn toàn offline**, không cần kết nối mạng.

### Q2: Dữ liệu có được gửi đi đâu không?

**A:** Không. Tất cả xử lý diễn ra **local trên máy bạn**. Không có dữ liệu được gửi ra ngoài.

### Q3: Có thể sử dụng trên Mac/Linux không?

**A:** Hiện tại chỉ hỗ trợ Windows. Mac/Linux có thể chạy từ source code (cần Python).

### Q4: Model AI có chính xác không?

**A:** Độ chính xác phụ thuộc vào:
- Chất lượng ảnh/camera
- Điều kiện ánh sáng
- Độ rõ của dấu X

Trong điều kiện tốt: ~95-98% accuracy.

### Q5: Có thể tùy chỉnh số lượng ứng viên không?

**A:** Hiện tại cố định 5 ứng viên. Để thay đổi cần sửa source code.

### Q6: Có thể thêm logo/tên tổ chức không?

**A:** Có thể tùy chỉnh bằng cách sửa file `config.py` (cần kiến thức Python).

### Q7: Làm sao backup dữ liệu?

**A:** Copy toàn bộ thư mục `output/` để backup các file Excel đã xuất.

### Q8: Có hỗ trợ kỹ thuật không?

**A:** Liên hệ qua email/phone được cung cấp trong package.

### Q9: Update version mới như thế nào?

**A:** Tải version mới → Extract → Chạy. Dữ liệu cũ trong `output/` vẫn giữ nguyên.

### Q10: License sử dụng?

**A:** Xem file `LICENSE.txt` trong package.

---

## 📞 Liên Hệ

**Hỗ trợ kỹ thuật:**
- Email: dnhnhan2003@gmail.com
- Phone: 0908961308
- Giờ làm việc: 8:30-18:00 (T2-T6)

**Báo lỗi:**
- GitHub: https://github.com/yourrepo/issues
- Email: bugs@example.com

**Góp ý:**
- Email: feedback@example.com

---

## 📝 Ghi Chú Phiên Bản

### Version 1.0.0 (2024-01-xx)
- ✅ Release đầu tiên
- ✅ Hỗ trợ camera và file ảnh
- ✅ Xuất Excel 3 sheets
- ✅ Model YOLOv8 tối ưu
- ✅ Giao diện CustomTkinter

---

## 📄 License

Copyright © 2024. All rights reserved.

Xem chi tiết trong file `LICENSE.txt`.

---

**Chúc bạn sử dụng hiệu quả! 🎉**
