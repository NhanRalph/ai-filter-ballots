# Hướng Dẫn Kết Nối Thiết Bị Camera Ngoài

## 📹 Các Loại Camera Hỗ Trợ

Hệ thống hỗ trợ nhiều loại camera:

### 1. Webcam Tích Hợp (Built-in)
- ✅ Laptop có webcam sẵn
- ✅ Tự động nhận diện là Camera 0
- ✅ Không cần cài đặt thêm

### 2. Webcam USB Ngoài
- ✅ USB webcam 720p/1080p
- ✅ Logitech, Microsoft, A4Tech, v.v.
- ✅ Plug & Play (cắm là dùng được)

### 3. Camera Điện Thoại (Qua USB/Wireless)
- ✅ Dùng app DroidCam, IP Webcam
- ✅ Kết nối qua USB hoặc WiFi
- ✅ Chất lượng cao, linh hoạt

### 4. Camera IP/Network
- ⚠️ Cần cấu hình RTSP URL
- ⚠️ Yêu cầu sửa code (nâng cao)

---

## 🔌 Hướng Dẫn Kết Nối

### Option 1: Webcam USB (Khuyến Nghị)

#### Bước 1: Cắm Webcam
```
1. Cắm webcam vào cổng USB
2. Windows sẽ tự động cài driver
3. Đợi 10-30 giây để nhận diện
4. Kiểm tra: Windows Settings > Camera
```

#### Bước 2: Kiểm Tra Camera
```
Windows 11/10:
1. Mở "Camera" app từ Start Menu
2. Nếu thấy hình ảnh → Camera OK
3. Nếu không thấy → Xem phần Troubleshooting
```

#### Bước 3: Chạy Ứng Dụng
```
1. Mở BallotVerification.exe
2. Chọn camera từ dropdown:
   - Camera 0 (Default) - Thường là webcam built-in
   - Camera 1 - Thường là USB webcam ngoài
   - Camera 2, 3 - Nếu có nhiều camera
3. Click "🎥 Bật Camera"
4. Nếu lỗi → App sẽ tự động thử các camera khác
```

---

### Option 2: Camera Điện Thoại (DroidCam)

**DroidCam** biến điện thoại thành webcam chất lượng cao.

#### Cài Đặt:

**Trên Máy Tính (Windows):**
1. Download DroidCam Client: https://www.dev47apps.com/droidcam/windows/
2. Cài đặt và khởi động

**Trên Điện Thoại (Android/iOS):**
1. Download app "DroidCam" từ Play Store / App Store
2. Mở app, note IP address hiển thị

#### Kết Nối:

**USB (Ổn định hơn):**
```
1. Cắm điện thoại vào USB
2. Bật USB Debugging trên điện thoại (Developer Options)
3. Mở DroidCam Client trên PC
4. Chọn "USB" → Click "Start"
5. DroidCam sẽ xuất hiện như Camera 1 hoặc Camera 2
```

**WiFi:**
```
1. Kết nối điện thoại và PC cùng WiFi
2. Mở DroidCam app trên điện thoại
3. Mở DroidCam Client trên PC
4. Nhập IP từ điện thoại vào PC client
5. Click "Start"
```

#### Sử Dụng với App:
```
1. Sau khi DroidCam "Start", nó là virtual webcam
2. Mở BallotVerification app
3. Chọn camera (thử từ Camera 1, 2, 3...)
4. Click "Bật Camera"
```

---

### Option 3: IP Webcam (Android)

**IP Webcam** - Alternative cho Android.

#### Cài Đặt:
1. Download "IP Webcam" từ Play Store
2. Mở app → Scroll xuống → "Start server"
3. App hiển thị URL: `http://192.168.x.x:8080`

#### Kết Nối:
```
1. Trên PC, mở browser vào URL trên
2. Hoặc dùng VLC Media Player:
   - Media > Open Network Stream
   - Nhập: http://192.168.x.x:8080/video
```

⚠️ **Lưu ý:** Phương pháp này yêu cầu sửa code để kết nối RTSP. Khuyến nghị dùng DroidCam.

---

## 🛠️ Troubleshooting

### ❌ "Không thể mở camera"

**Giải pháp 1: Kiểm tra quyền truy cập**
```
Windows 11:
Settings > Privacy > Camera > Allow apps to access camera
Bật ON cho tất cả apps
```

**Giải pháp 2: Đóng apps khác đang dùng camera**
```
Các app thường chiếm camera:
- Zoom, Teams, Skype
- Discord
- OBS Studio
- Browser (Google Meet, Messenger Video...)

→ Đóng tất cả trước khi dùng app này
```

**Giải pháp 3: Restart camera service**
```
1. Mở Device Manager (Win + X)
2. Tìm "Cameras" hoặc "Imaging devices"
3. Right-click webcam → Disable
4. Đợi 5 giây
5. Right-click → Enable
```

**Giải pháp 4: Thử các Camera ID khác**
```
App có auto-detect, nhưng bạn có thể thử thủ công:
1. Chọn Camera 1 từ dropdown
2. Click "Bật Camera"
3. Nếu lỗi → Thử Camera 2, 3...
```

---

### ⚠️ Camera mở nhưng không có hình

**Nguyên nhân:** Driver lỗi hoặc camera bị lỗi

**Giải pháp:**
```
1. Kiểm tra với Camera app của Windows
2. Nếu Windows Camera app cũng không có hình:
   → Vấn đề ở driver/hardware
   
3. Update driver:
   - Device Manager > Cameras
   - Right-click > Update driver
   - Hoặc tải driver từ website nhà sản xuất

4. Thử cổng USB khác
5. Restart máy
```

---

### 🐌 Camera lag / FPS thấp

**Nguyên nhân:** CPU/GPU yếu hoặc resolution cao

**Giải pháp:**
```
1. Đóng apps khác đang chạy
2. Giảm resolution camera (nếu có settings)
3. Sử dụng model ONNX (nhanh hơn PyTorch)
4. Upgrade hardware:
   - RAM: 8GB+
   - CPU: Intel i5+ / AMD Ryzen 5+
```

---

### 📱 DroidCam không nhận diện

**USB Method:**
```
1. Bật USB Debugging:
   Settings > Developer Options > USB Debugging
   
2. Chọn USB mode là "File Transfer" hoặc "PTP"

3. Allow USB debugging khi điện thoại hỏi

4. Restart DroidCam Client
```

**WiFi Method:**
```
1. Đảm bảo PC và điện thoại cùng WiFi
2. Tắt VPN (cả PC và điện thoại)
3. Tắt firewall tạm thời để test
4. Ping IP của điện thoại từ PC:
   - Open CMD
   - ping 192.168.x.x
   - Nếu không ping được → vấn đề network
```

---

## 💡 Tips & Best Practices

### Chất Lượng Camera

**Khuyến nghị:**
- ✅ **Resolution:** 720p (1280x720) là đủ
- ✅ **FPS:** 15-30 FPS
- ✅ **Lighting:** Đủ sáng, không chói
- ✅ **Distance:** 30-50cm từ camera đến phiếu
- ✅ **Angle:** Camera song song với phiếu (90 độ)

### Positioning

```
        [Camera]
           📹
           |
         30-50cm
           |
      ┌────────────┐
      │   PHIẾU    │  ← Phiếu nằm phẳng
      │    BẦU     │
      └────────────┘
```

### Lighting Setup

**Tốt:**
```
   💡        💡
   ↘        ↙
     [Phiếu]     ← Ánh sáng từ 2 bên
```

**Không tốt:**
```
      💡
      ↓
   [Phiếu]        ← Ánh sáng trực tiếp → chói, phản quang
```

---

## 📊 Camera Comparison

| Loại | Ưu điểm | Nhược điểm | Giá |
|------|---------|------------|-----|
| **Built-in** | Sẵn có, tiện | Chất lượng trung bình | Free |
| **USB Webcam** | Chất lượng tốt, ổn định | Tốn tiền | 200k-1tr |
| **DroidCam** | Chất lượng cao, linh hoạt | Cần setup | Free |
| **IP Webcam** | Wireless, linh hoạt | Phức tạp, lag | Free |

**Khuyến nghị cho sản xuất:**
- 💼 **Professional:** USB Webcam 1080p (Logitech C920/C922)
- 💰 **Budget:** DroidCam với điện thoại có sẵn
- 🏠 **Home use:** Built-in webcam

---

## 🔧 Advanced: Multiple Cameras

Nếu cần dùng **nhiều camera cùng lúc** (nhiều trạm kiểm phiếu):

### Setup:
```
1. Cắm nhiều USB webcam (Camera 0, 1, 2, 3...)
2. Mỗi máy tính 1 camera → Chạy nhiều instances của app
3. Hoặc 1 máy nhiều camera → Mở nhiều windows app
```

### Code Support:
App hiện tại hỗ trợ chọn camera ID 0-3. Có thể mở nhiều instances với camera khác nhau.

---

## 📞 Hỗ Trợ Camera

**Nếu vẫn gặp vấn đề:**

1. **Check camera với Windows Camera app trước**
   - Nếu Windows Camera OK → Vấn đề ở app
   - Nếu Windows Camera lỗi → Vấn đề driver/hardware

2. **Thông tin cần cung cấp khi báo lỗi:**
   - Loại camera (built-in / USB / DroidCam)
   - Camera ID đã thử (0, 1, 2, 3?)
   - Error message cụ thể
   - Windows version
   - Screenshot nếu có

3. **Workaround:** Dùng chức năng "Import Folder"
   - Chụp ảnh phiếu bằng camera/điện thoại trước
   - Copy ảnh vào máy tính
   - Dùng "📁 Import Folder" để xử lý batch

---

## 🎯 Quick Reference

### Camera Không Hoạt Động?

```
✅ Checklist:
□ Camera đã cắm / bật?
□ Driver đã cài?
□ Quyền truy cập camera đã bật?
□ Apps khác đã đóng? (Zoom, Teams...)
□ Đã thử Camera 1, 2, 3?
□ Windows Camera app hoạt động?
□ Đã restart máy?

❌ Vẫn lỗi?
→ Dùng "📂 Mở 1 ảnh" hoặc "📁 Import Folder"
→ Liên hệ support
```

---

**Chúc bạn kết nối camera thành công! 📹✅**
