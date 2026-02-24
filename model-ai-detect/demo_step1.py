"""
QUICK START - Test nhanh BƯỚC 1
File này giúp bạn test nhanh logic ROI detection mà không cần model thật
(Sử dụng dummy detections để mô phỏng)
"""

import cv2
import numpy as np
from step1_roi_detection import BallotROIDetector
import config


def create_sample_ballot_image(width=1000, height=600):
    """
    Tạo ảnh phiếu bầu mẫu với các vết gạch giả lập
    """
    # Tạo ảnh trắng
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Tính ROI zones
    detector = BallotROIDetector()
    roi_zones = detector.calculate_roi_zones(height, width)
    
    # Vẽ các vùng ROI
    for idx, roi in enumerate(roi_zones):
        x1, y1, x2, y2 = roi
        
        # Vẽ khung ROI
        cv2.rectangle(img, (x1, y1), (x2, y2), (200, 200, 200), 2)
        
        # Vẽ tên ứng viên
        name = config.CANDIDATE_NAMES[idx]
        text_x = x1 + 10
        text_y = (y1 + y2) // 2
        
        cv2.putText(img, f"{idx+1}. {name}", (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Vẽ một số vết gạch giả lập (màu đỏ)
    # Giả sử gạch người 1, 3, 5
    crossed_indices = [0, 2, 4]  # Index của người bị gạch
    
    for idx in crossed_indices:
        x1, y1, x2, y2 = roi_zones[idx]
        
        # Vẽ vết gạch ngang
        center_y = (y1 + y2) // 2
        line_x1 = x1 + 20
        line_x2 = x2 - 20
        cv2.line(img, (line_x1, center_y), (line_x2, center_y), 
                (0, 0, 255), 5)
    
    # Thêm tiêu đề
    cv2.putText(img, "SAMPLE BALLOT - Crossed: Person 1, 3, 5", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    
    return img


def demo_without_model():
    """
    Demo BƯỚC 1 mà không cần model thật
    """
    print("="*60)
    print("DEMO - BƯỚC 1: ROI Detection (Without Real Model)")
    print("="*60)
    
    # 1. Tạo ảnh mẫu
    print("\n1. Tạo ảnh phiếu bầu mẫu...")
    sample_img = create_sample_ballot_image()
    
    # 2. Khởi tạo detector (không load model)
    print("2. Khởi tạo detector...")
    detector = BallotROIDetector()
    
    # 3. Tính ROI zones
    h, w = sample_img.shape[:2]
    roi_zones = detector.calculate_roi_zones(h, w)
    print(f"3. Tính toán {len(roi_zones)} vùng ROI")
    print(f"   Layout: {detector.roi_layout}")
    
    # 4. Giả lập detections (vết gạch)
    # Giả sử model phát hiện được 3 vết gạch ở người 1, 3, 5
    print("\n4. Giả lập detections (model phát hiện)...")
    
    dummy_detections = []
    crossed_indices = [0, 2, 4]  # Người 1, 3, 5
    
    for idx in crossed_indices:
        x1, y1, x2, y2 = roi_zones[idx]
        # Tạo bbox giả ở giữa ROI
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        bbox_w, bbox_h = 100, 30
        
        bbox = (
            center_x - bbox_w//2,
            center_y - bbox_h//2,
            center_x + bbox_w//2,
            center_y + bbox_h//2,
            0.95  # confidence
        )
        dummy_detections.append(bbox)
    
    print(f"   Phát hiện: {len(dummy_detections)} vết gạch")
    
    # 5. Xử lý logic mapping
    print("\n5. Mapping detections -> ROI...")
    crossed_status = [0, 0, 0, 0, 0]
    
    for detection in dummy_detections:
        bbox = detection[:4]
        for roi_idx, roi in enumerate(roi_zones):
            if detector.check_bbox_in_roi(bbox, roi):
                crossed_status[roi_idx] = 1
                print(f"   ✓ Phát hiện vết gạch trong ROI #{roi_idx+1} ({config.CANDIDATE_NAMES[roi_idx]})")
                break
    
    # 6. Vẽ visualization
    print("\n6. Vẽ visualization...")
    annotated = detector.draw_visualization(
        sample_img, roi_zones, dummy_detections, crossed_status
    )
    
    # 7. Hiển thị kết quả
    print("\n" + "="*60)
    print("KẾT QUẢ:")
    print("="*60)
    print(f"Trạng thái gạch: {crossed_status}")
    print(f"Tổng số người bị gạch: {sum(crossed_status)}/5")
    print(f"\nChi tiết:")
    
    for idx, status in enumerate(crossed_status):
        name = config.CANDIDATE_NAMES[idx]
        result = "BỊ GẠCH ❌" if status == 1 else "ĐƯỢC CHỌN ✓"
        print(f"  {idx+1}. {name}: {result}")
    
    # 8. Xác định loại phiếu
    num_crossed = sum(crossed_status)
    if num_crossed in config.VALID_BALLOT_RULES:
        ballot_type = config.VALID_BALLOT_RULES[num_crossed]
        print(f"\n✅ Phiếu HỢP LỆ: {ballot_type}")
    else:
        print(f"\n❌ Phiếu KHÔNG HỢP LỆ (Số gạch: {num_crossed})")
    
    # 9. Hiển thị ảnh
    cv2.imshow("Original Sample", sample_img)
    cv2.imshow("Detection Result", annotated)
    print("\nNhấn phím bất kỳ để đóng...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # 10. Lưu ảnh
    cv2.imwrite("models/sample_ballot.jpg", sample_img)
    cv2.imwrite("models/sample_result.jpg", annotated)
    print("\n✅ Đã lưu ảnh mẫu vào models/sample_ballot.jpg và models/sample_result.jpg")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("QUICK START - DEMO BƯỚC 1 (Không cần model thật)")
    print("="*70)
    print("\nDemo này sẽ:")
    print("  1. Tạo ảnh phiếu bầu mẫu")
    print("  2. Giả lập việc detect vết gạch")
    print("  3. Mapping vết gạch vào 5 vùng ROI")
    print("  4. Hiển thị kết quả visualization")
    print("\n" + "="*70)
    
    input("\nNhấn Enter để bắt đầu demo...")
    demo_without_model()
    
    print("\n" + "="*70)
    print("✅ DEMO HOÀN TẤT!")
    print("="*70)
    print("\nBước tiếp theo:")
    print("  1. Đặt model 'best.pt' vào thư mục models/")
    print("  2. Chạy: python step1_roi_detection.py")
    print("  3. Test với ảnh thật hoặc webcam")
    print("\nHoặc tiếp tục với BƯỚC 2!")
