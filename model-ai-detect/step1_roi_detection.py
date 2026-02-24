"""
BƯỚC 1: Logic Core & OpenCV (ROI Mapping)
Chức năng:
- Load model YOLOv8 (best.pt)
- Chia ảnh làm 5 vùng ROI
- Detect vết gạch
- Kiểm tra bounding box thuộc ROI nào
- Trả về mảng kết quả [1, 0, 0, 1, 1] (1 = bị gạch, 0 = không gạch)
"""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Dict
import config


class BallotROIDetector:
    """Class chính để xử lý phát hiện vết gạch trên phiếu bầu"""
    
    def __init__(self, model_path: str = None, confidence: float = None):
        """
        Khởi tạo detector
        
        Args:
            model_path: Đường dẫn đến file model YOLOv8 (.pt)
            confidence: Ngưỡng confidence (0-1)
        """
        self.model_path = model_path or config.MODEL_PATH
        self.confidence = confidence or config.CONFIDENCE_THRESHOLD
        self.model = None
        self.roi_layout = config.ROI_LAYOUT
        
    def load_model(self):
        """Load model YOLOv8"""
        try:
            print(f"Loading model from: {self.model_path}")
            self.model = YOLO(self.model_path)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def calculate_roi_zones(self, frame_height: int, frame_width: int) -> List[Tuple[int, int, int, int]]:
        """
        Tính toán 5 vùng ROI dựa trên kích thước ảnh
        
        Args:
            frame_height: Chiều cao ảnh
            frame_width: Chiều rộng ảnh
            
        Returns:
            List of 5 ROI zones: [(x1, y1, x2, y2), ...]
        """
        roi_zones = []
        
        if self.roi_layout == "HORIZONTAL":
            # Chia 5 vùng theo chiều ngang (từ trái sang phải)
            zone_width = frame_width // 5
            for i in range(5):
                x1 = i * zone_width
                x2 = (i + 1) * zone_width if i < 4 else frame_width
                y1 = 0
                y2 = frame_height
                roi_zones.append((x1, y1, x2, y2))
                
        elif self.roi_layout == "VERTICAL":
            # Chia 5 vùng theo chiều dọc (từ trên xuống dưới)
            zone_height = frame_height // 5
            for i in range(5):
                x1 = 0
                x2 = frame_width
                y1 = i * zone_height
                y2 = (i + 1) * zone_height if i < 4 else frame_height
                roi_zones.append((x1, y1, x2, y2))
        
        return roi_zones
    
    def check_bbox_in_roi(self, bbox: Tuple[int, int, int, int], 
                          roi: Tuple[int, int, int, int]) -> bool:
        """
        Kiểm tra bounding box có nằm trong ROI không
        Sử dụng tâm của bbox để xác định
        
        Args:
            bbox: (x1, y1, x2, y2) của vết gạch
            roi: (x1, y1, x2, y2) của vùng ROI
            
        Returns:
            True nếu tâm bbox nằm trong ROI
        """
        # Tính tâm của bbox
        bbox_center_x = (bbox[0] + bbox[2]) // 2
        bbox_center_y = (bbox[1] + bbox[3]) // 2
        
        # Kiểm tra tâm có nằm trong ROI không
        roi_x1, roi_y1, roi_x2, roi_y2 = roi
        
        if (roi_x1 <= bbox_center_x <= roi_x2 and 
            roi_y1 <= bbox_center_y <= roi_y2):
            return True
        return False
    
    def detect_marks_on_frame(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Phát hiện vết gạch trên frame
        
        Args:
            frame: Ảnh đầu vào (BGR format)
            
        Returns:
            List of detections: [(x1, y1, x2, y2, confidence), ...]
        """
        if self.model is None:
            print("Model chưa được load! Gọi load_model() trước.")
            return []
        
        # Chạy detection
        results = self.model(frame, conf=self.confidence, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Lấy tọa độ bbox
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                confidence = float(box.conf[0])
                detections.append((x1, y1, x2, y2, confidence))
        
        return detections
    
    def process_ballot(self, frame: np.ndarray, visualize: bool = False) -> Tuple[List[int], np.ndarray]:
        """
        Xử lý 1 phiếu bầu - HÀM CHÍNH
        
        Args:
            frame: Ảnh phiếu bầu (BGR format)
            visualize: True nếu muốn vẽ ROI và detection lên ảnh
            
        Returns:
            Tuple gồm:
            - crossed_status: List[int] - [1,0,0,1,1] (1=bị gạch, 0=không gạch)
            - annotated_frame: np.ndarray - Ảnh có vẽ ROI và detection (nếu visualize=True)
        """
        # 1. Tính toán 5 vùng ROI
        h, w = frame.shape[:2]
        roi_zones = self.calculate_roi_zones(h, w)
        
        # 2. Detect vết gạch
        detections = self.detect_marks_on_frame(frame)
        
        # 3. Khởi tạo trạng thái: 0 = không bị gạch
        crossed_status = [0, 0, 0, 0, 0]
        
        # 4. Kiểm tra từng detection xem nằm trong ROI nào
        for detection in detections:
            bbox = detection[:4]  # (x1, y1, x2, y2)
            
            for roi_idx, roi in enumerate(roi_zones):
                if self.check_bbox_in_roi(bbox, roi):
                    crossed_status[roi_idx] = 1
                    break  # 1 detection chỉ thuộc 1 ROI
        
        # 5. Vẽ visualization nếu cần
        annotated_frame = frame.copy()
        if visualize:
            annotated_frame = self.draw_visualization(
                frame, roi_zones, detections, crossed_status
            )
        
        return crossed_status, annotated_frame
    
    def draw_visualization(self, frame: np.ndarray, 
                          roi_zones: List[Tuple[int, int, int, int]],
                          detections: List[Tuple[int, int, int, int, float]],
                          crossed_status: List[int]) -> np.ndarray:
        """
        Vẽ ROI zones và detections lên ảnh
        
        Args:
            frame: Ảnh gốc
            roi_zones: List các vùng ROI
            detections: List các vết gạch phát hiện được
            crossed_status: Trạng thái bị gạch [1,0,0,1,1]
            
        Returns:
            Ảnh đã vẽ
        """
        annotated = frame.copy()
        
        # 1. Vẽ các vùng ROI
        for idx, roi in enumerate(roi_zones):
            x1, y1, x2, y2 = roi
            
            # Vẽ khung ROI
            color = (0, 255, 0) if crossed_status[idx] == 0 else (0, 0, 255)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Vẽ label
            label = f"{config.CANDIDATE_NAMES[idx]}"
            status = "GẠCH" if crossed_status[idx] == 1 else "OK"
            text = f"{idx+1}. {label}: {status}"
            
            # Vị trí text
            text_y = y1 + 30 if self.roi_layout == "VERTICAL" else y1 - 10
            cv2.putText(annotated, text, (x1 + 5, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE, 
                       config.COLOR_TEXT, config.FONT_THICKNESS)
        
        # 2. Vẽ các detection
        for detection in detections:
            x1, y1, x2, y2, conf = detection
            cv2.rectangle(annotated, (x1, y1), (x2, y2), 
                         config.COLOR_DETECTION, config.BBOX_THICKNESS)
            cv2.putText(annotated, f"{conf:.2f}", (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                       config.COLOR_DETECTION, 2)
        
        # 3. Thêm tổng kết
        total_crossed = sum(crossed_status)
        summary = f"Total crossed: {total_crossed}/5"
        cv2.putText(annotated, summary, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        
        return annotated


def test_with_image(image_path: str):
    """
    Hàm test với ảnh tĩnh
    
    Args:
        image_path: Đường dẫn đến ảnh test
    """
    print("=" * 50)
    print("TESTING BALLOT ROI DETECTOR")
    print("=" * 50)
    
    # 1. Khởi tạo detector
    detector = BallotROIDetector()
    
    # 2. Load model
    if not detector.load_model():
        print("Không thể load model! Kiểm tra đường dẫn model.")
        return
    
    # 3. Đọc ảnh
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Không thể đọc ảnh: {image_path}")
        return
    
    print(f"\nXử lý ảnh: {image_path}")
    print(f"Kích thước: {frame.shape[1]}x{frame.shape[0]}")
    
    # 4. Process ballot
    crossed_status, annotated_frame = detector.process_ballot(frame, visualize=True)
    
    # 5. In kết quả
    print(f"\n{'='*50}")
    print("KẾT QUẢ PHÁT HIỆN:")
    print(f"{'='*50}")
    print(f"Trạng thái gạch: {crossed_status}")
    print(f"Tổng số người bị gạch: {sum(crossed_status)}/5")
    print(f"\nChi tiết:")
    for idx, status in enumerate(crossed_status):
        name = config.CANDIDATE_NAMES[idx]
        result = "BỊ GẠCH ❌" if status == 1 else "ĐƯỢC CHỌN ✓"
        print(f"  {idx+1}. {name}: {result}")
    
    # 6. Hiển thị ảnh
    # Resize nếu ảnh quá lớn
    h, w = annotated_frame.shape[:2]
    if h > 800:
        scale = 800 / h
        new_w = int(w * scale)
        annotated_frame = cv2.resize(annotated_frame, (new_w, 800))
    
    cv2.imshow("Ballot Detection Result", annotated_frame)
    print("\nNhấn phím bất kỳ để đóng cửa sổ...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # 7. Lưu ảnh kết quả
    output_path = image_path.replace(".", "_result.")
    cv2.imwrite(output_path, annotated_frame)
    print(f"\nĐã lưu kết quả vào: {output_path}")


def test_with_webcam(camera_id: int = 0):
    """
    Hàm test với webcam real-time
    
    Args:
        camera_id: ID của camera (mặc định 0)
    """
    print("=" * 50)
    print("TESTING WITH WEBCAM")
    print("=" * 50)
    
    # 1. Khởi tạo detector
    detector = BallotROIDetector()
    
    # 2. Load model
    if not detector.load_model():
        print("Không thể load model!")
        return
    
    # 3. Mở camera
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Không thể mở camera {camera_id}")
        return
    
    print("\nCamera đã mở!")
    print("Hướng dẫn:")
    print("  - Nhấn SPACE để chụp và phân tích")
    print("  - Nhấn 'q' để thoát")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame từ camera")
            break
        
        # Tính ROI zones và vẽ sơ bộ
        h, w = frame.shape[:2]
        roi_zones = detector.calculate_roi_zones(h, w)
        
        display_frame = frame.copy()
        for idx, roi in enumerate(roi_zones):
            x1, y1, x2, y2 = roi
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), 
                         config.COLOR_ROI, 1)
            label = f"{idx+1}. {config.CANDIDATE_NAMES[idx]}"
            text_y = y1 + 30 if detector.roi_layout == "VERTICAL" else y1 - 10
            cv2.putText(display_frame, label, (x1 + 5, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.putText(display_frame, "Press SPACE to analyze | 'q' to quit", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow("Webcam - Ballot Detector", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # SPACE - Chụp và phân tích
            print("\n" + "="*50)
            print("ANALYZING FRAME...")
            print("="*50)
            
            crossed_status, annotated_frame = detector.process_ballot(frame, visualize=True)
            
            print(f"Trạng thái gạch: {crossed_status}")
            print(f"Tổng số người bị gạch: {sum(crossed_status)}/5")
            
            cv2.imshow("Analysis Result", annotated_frame)
            print("Nhấn phím bất kỳ để tiếp tục...")
            cv2.waitKey(0)
            cv2.destroyWindow("Analysis Result")
            
        elif key == ord('q'):  # Quit
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\nĐã đóng camera.")


if __name__ == "__main__":
    """
    Test script
    Bạn có thể chọn 1 trong 2 cách test:
    """
    
    import sys
    
    print("\n" + "="*60)
    print("BƯỚC 1: BALLOT ROI DETECTION TEST")
    print("="*60)
    print("\nChọn chế độ test:")
    print("1. Test với ảnh tĩnh")
    print("2. Test với webcam real-time")
    
    choice = input("\nNhập lựa chọn (1/2): ").strip()
    
    if choice == "1":
        image_path = input("Nhập đường dẫn ảnh test: ").strip()
        if image_path:
            test_with_image(image_path)
        else:
            print("Vui lòng cung cấp đường dẫn ảnh!")
            
    elif choice == "2":
        camera_id = input("Nhập ID camera (mặc định 0): ").strip()
        camera_id = int(camera_id) if camera_id else 0
        test_with_webcam(camera_id)
        
    else:
        print("Lựa chọn không hợp lệ!")
