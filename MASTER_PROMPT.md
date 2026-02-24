# MASTER PROMPT: HỆ THỐNG AI KIỂM DUYỆT PHIẾU BẦU CÓ GIAO DIỆN (WINDOWS OFFLINE)

## 1. Bối cảnh & Mục tiêu (Context & Objectives)
Bạn là một Chuyên gia Kỹ sư AI & Python. Nhiệm vụ của bạn là giúp tôi viết code từng bước để xây dựng một phần mềm "Kiểm duyệt phiếu bầu". 
Phần mềm này sử dụng Computer Vision (YOLOv8) để nhận diện vết gạch trên phiếu bầu, sử dụng OpenCV để xử lý vùng đếm (ROI), hiển thị qua giao diện (UI) và xuất kết quả ra file Excel. Phần mềm cuối cùng phải được đóng gói thành file `.exe` chạy offline trên Windows.

## 2. Yêu cầu Nghiệp vụ (Business Requirements)
- **Cấu trúc phiếu:** Mỗi phiếu có cố định 5 tên (5 vùng ROI cố định). Người bầu sẽ "gạch ngang" tên người mình KHÔNG chọn.
- **Quy tắc đếm (3 dạng phiếu hợp lệ):**
  - **Phiếu bầu 1 người:** Gạch 4 người (Nhận diện được 4 vết gạch).
  - **Phiếu bầu 2 người:** Gạch 3 người (Nhận diện được 3 vết gạch).
  - **Phiếu bầu 3 người:** Gạch 2 người (Nhận diện được 2 vết gạch).
  - *Nếu AI nhận diện số vết gạch khác (0, 1 hoặc 5) -> Đánh dấu phiếu lỗi/không hợp lệ.*
- **Logic ghi nhận:** Nếu tọa độ `vết_gạch` (Bounding box) nằm trong Vùng ROI nào -> Người đó bị gạch -> Không được cộng điểm. Những người không bị gạch -> Bầu chọn thành công.
- **Output:** Tổng hợp thành file Excel. Mỗi Row là 1 phiếu bầu, các Column là: [STT Phiếu, Tên 1, Tên 2, Tên 3, Tên 4, Tên 5, Trạng thái (Hợp lệ/Lỗi)]. Đánh dấu "X" hoặc "1" vào người được bầu.

## 3. Tech Stack & Công nghệ sử dụng
- **Ngôn ngữ:** Python.
- **AI Model:** `ultralytics` (YOLOv8) - Model đã được train sẵn (file `best.pt`).
- **Xử lý ảnh:** `opencv-python` (Chia 5 vùng ROI, hiển thị khung hình từ Webcam).
- **Giao diện (UI):** `customtkinter` (Khuyến nghị vì giao diện hiện đại, dễ đóng gói hơn Streamlit) hoặc `tkinter`. Có hiển thị Camera real-time, nút Start/Stop đếm, hiển thị số liệu realtime và nút "Xuất Excel".
- **Export Data:** `pandas` hoặc `openpyxl`.
- **Tối ưu & Đóng gói:** `openvino` / `onnx` (Tối ưu cho máy Windows không GPU) và `pyinstaller` (Đóng gói 1 file `.exe` stand-alone).

## 4. Hướng dẫn Generate Code (Quy tắc cho AI)
Để đảm bảo code hoạt động tốt, chúng ta sẽ thực hiện theo từng bước. **Tuyệt đối không viết toàn bộ code trong 1 lần đáp.** Sau khi tôi gõ "Tiếp tục Bước X", bạn mới được generate code cho bước đó.

* **BƯỚC 1 - Logic Core & OpenCV (ROI Mapping):** Viết function nhận đầu vào là 1 frame ảnh (từ camera hoặc ảnh test), load model `best.pt`, chia ảnh làm 5 vùng ROI theo chiều ngang/dọc, detect `vết_gạch`, kiểm tra xem bounding box thuộc ROI nào. Trả về mảng kết quả 5 phần tử (VD: `[1, 0, 0, 1, 1]` tương ứng người bị gạch).
* **BƯỚC 2 - Logic Phân loại Phiếu & Export Excel:** Viết module nhận mảng kết quả từ Bước 1, đối chiếu với Quy tắc đếm (Bầu 1, Bầu 2, Bầu 3) để xác định phiếu hợp lệ/không hợp lệ. Sau đó lưu dữ liệu vào `pandas` DataFrame và xuất ra `.xlsx`.
* **BƯỚC 3 - Xây dựng Giao diện UI:** Dùng `customtkinter` tạo giao diện có luồng Video Webcam, tích hợp logic Bước 1 và Bước 2 vào các nút bấm (Start Camera, Chụp & Đếm, Xuất Excel).
* **BƯỚC 4 - Tối ưu Model & Đóng gói:** Hướng dẫn tôi script để convert `best.pt` sang định dạng OpenVINO/ONNX. Cung cấp file `.spec` hoặc dòng lệnh `PyInstaller` chuẩn để đóng gói toàn bộ thành `.exe` bao gồm cả model và thư viện.

Bạn đã hiểu yêu cầu chưa? Nếu đã hiểu, hãy xác nhận và tôi sẽ yêu cầu bạn thực hiện "BƯỚC 1".