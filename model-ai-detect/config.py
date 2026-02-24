"""
CONFIG FILE - Cấu hình hệ thống Kiểm duyệt Phiếu bầu
"""

# ==================== CẤU HÌNH MODEL ====================
MODEL_PATH = "models/best.pt"  # Đường dẫn model YOLOv8
CONFIDENCE_THRESHOLD = 0.5  # Ngưỡng confidence để detect vết gạch

# ==================== CẤU HÌNH ROI ====================
# Có 2 cách chia ROI:
# 1. HORIZONTAL: Chia 5 vùng theo chiều ngang (từ trái sang phải)
# 2. VERTICAL: Chia 5 vùng theo chiều dọc (từ trên xuống dưới)
ROI_LAYOUT = "HORIZONTAL"  # Chọn "HORIZONTAL" hoặc "VERTICAL"

# Tên 5 ứng viên (theo thứ tự tương ứng với 5 vùng ROI)
CANDIDATE_NAMES = [
    "Nguyễn Văn A",
    "Trần Thị B", 
    "Lê Văn C",
    "Phạm Thị D",
    "Hoàng Văn E"
]

# ==================== CẤU HÌNH QUY TẮC BẦU CỬ ====================
# Số gạch hợp lệ cho mỗi loại phiếu
VALID_BALLOT_RULES = {
    4: "Bầu 1 người",  # 4 gạch = 1 người được chọn
    3: "Bầu 2 người",  # 3 gạch = 2 người được chọn
    2: "Bầu 3 người"   # 2 gạch = 3 người được chọn
}

# ==================== CẤU HÌNH HIỂN THỊ ====================
# Màu sắc cho bounding box và ROI
COLOR_ROI = (0, 255, 0)  # Màu xanh lá - vùng ROI
COLOR_DETECTION = (0, 0, 255)  # Màu đỏ - vết gạch phát hiện
COLOR_TEXT = (255, 255, 255)  # Màu trắng - text
BBOX_THICKNESS = 2
FONT_SCALE = 0.6
FONT_THICKNESS = 2
