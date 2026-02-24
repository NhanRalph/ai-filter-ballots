"""
FULL PIPELINE: Tích hợp BƯỚC 1 + BƯỚC 2
Script này tích hợp đầy đủ từ:
- Load model (BƯỚC 1)
- Detect vết gạch từ ảnh/webcam (BƯỚC 1)
- Phân loại phiếu (BƯỚC 2)
- Thu thập và xuất Excel (BƯỚC 2)

Sử dụng script này khi bạn đã có model best.pt
"""

import cv2
import os
from pathlib import Path
from step1_roi_detection import BallotROIDetector
from step2_ballot_classifier import BallotClassifier, BallotDataCollector, ExcelExporter
import config


class BallotProcessingPipeline:
    """Pipeline xử lý đầy đủ từ ảnh đến Excel"""
    
    def __init__(self, model_path=None):
        """
        Khởi tạo pipeline
        
        Args:
            model_path: Đường dẫn model (mặc định lấy từ config)
        """
        print("="*70)
        print("KHỞI TẠO BALLOT PROCESSING PIPELINE")
        print("="*70)
        
        # Khởi tạo các components
        print("\n1. Khởi tạo ROI Detector...")
        self.detector = BallotROIDetector(model_path=model_path)
        
        print("2. Load model YOLOv8...")
        if not self.detector.load_model():
            raise Exception("Không thể load model! Kiểm tra đường dẫn.")
        
        print("3. Khởi tạo Classifier...")
        self.classifier = BallotClassifier()
        
        print("4. Khởi tạo Data Collector...")
        self.collector = BallotDataCollector()
        
        print("5. Khởi tạo Excel Exporter...")
        self.exporter = ExcelExporter()
        
        print("\n✅ Pipeline đã sẵn sàng!")
        
    def process_image(self, image_path, ballot_id=None, show_result=True):
        """
        Xử lý 1 ảnh phiếu bầu
        
        Args:
            image_path: Đường dẫn ảnh
            ballot_id: ID phiếu (tùy chọn)
            show_result: Hiển thị kết quả lên màn hình
            
        Returns:
            Dict chứa kết quả đầy đủ
        """
        # Đọc ảnh
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"❌ Không thể đọc ảnh: {image_path}")
            return None
        
        # BƯỚC 1: Detect vết gạch
        crossed_status, annotated_frame = self.detector.process_ballot(
            frame, visualize=True
        )
        
        # BƯỚC 2: Phân loại
        classification = self.classifier.classify_ballot(crossed_status)
        
        # Tạo ID tự động nếu không có
        if ballot_id is None:
            ballot_id = f"PHIEU_{len(self.collector.ballots) + 1:04d}"
        
        # Thu thập dữ liệu
        self.collector.add_ballot(
            crossed_status,
            ballot_id=ballot_id,
            metadata={
                'image_path': image_path,
                'image_name': os.path.basename(image_path)
            }
        )
        
        # Hiển thị kết quả
        if show_result:
            print(f"\n{'='*50}")
            print(f"Phiếu: {ballot_id}")
            print(f"Ảnh: {os.path.basename(image_path)}")
            print(f"{'='*50}")
            print(f"Trạng thái gạch: {crossed_status}")
            print(f"Kết quả: {classification['status_message']}")
            print(f"Người được bầu: {', '.join(classification['voted_for']) if classification['voted_for'] else 'Không có'}")
            
            # Hiển thị ảnh
            cv2.imshow(f"Result - {ballot_id}", annotated_frame)
            cv2.waitKey(1000)  # Hiển thị 1 giây
        
        return {
            'ballot_id': ballot_id,
            'crossed_status': crossed_status,
            'classification': classification,
            'annotated_frame': annotated_frame
        }
    
    def process_folder(self, folder_path, pattern="*.jpg", show_result=False):
        """
        Xử lý tất cả ảnh trong thư mục
        
        Args:
            folder_path: Đường dẫn thư mục
            pattern: Pattern file (*.jpg, *.png, etc.)
            show_result: Hiển thị từng kết quả
            
        Returns:
            List kết quả
        """
        print(f"\n{'='*70}")
        print(f"XỬ LÝ FOLDER: {folder_path}")
        print(f"{'='*70}")
        
        # Tìm tất cả ảnh
        folder = Path(folder_path)
        image_files = list(folder.glob(pattern))
        
        if not image_files:
            print(f"❌ Không tìm thấy ảnh nào với pattern: {pattern}")
            return []
        
        print(f"Tìm thấy {len(image_files)} ảnh")
        
        results = []
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] Xử lý: {image_path.name}")
            
            result = self.process_image(
                str(image_path),
                ballot_id=f"PHIEU_{idx:04d}",
                show_result=show_result
            )
            
            if result:
                results.append(result)
        
        cv2.destroyAllWindows()
        
        print(f"\n✅ Đã xử lý xong {len(results)}/{len(image_files)} ảnh")
        return results
    
    def process_webcam(self, camera_id=0, max_ballots=None):
        """
        Xử lý từ webcam real-time
        
        Args:
            camera_id: ID camera (mặc định 0)
            max_ballots: Số phiếu tối đa (None = không giới hạn)
        """
        print(f"\n{'='*70}")
        print("XỬ LÝ TỪ WEBCAM")
        print(f"{'='*70}")
        
        # Mở camera
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print(f"❌ Không thể mở camera {camera_id}")
            return
        
        print("\nCamera đã mở!")
        print("Hướng dẫn:")
        print("  - Nhấn SPACE để chụp và phân tích phiếu")
        print("  - Nhấn 's' để xem thống kê hiện tại")
        print("  - Nhấn 'q' để thoát và xuất Excel")
        
        ballot_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Không thể đọc frame")
                break
            
            # Hiển thị frame
            display_frame = frame.copy()
            
            # Thêm thông tin lên frame
            info_text = f"Phieu da xu ly: {ballot_count}"
            if max_ballots:
                info_text += f"/{max_ballots}"
            
            cv2.putText(display_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "SPACE: Chup | 's': Thong ke | 'q': Thoat", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.imshow("Webcam - Ballot Processing", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # SPACE - Chụp và xử lý
                ballot_count += 1
                ballot_id = f"WEBCAM_{ballot_count:04d}"
                
                print(f"\n{'='*50}")
                print(f"CHỤP PHIẾU #{ballot_count}")
                print(f"{'='*50}")
                
                # Xử lý
                result = self.process_image(
                    None,  # Không cần đường dẫn
                    ballot_id=ballot_id,
                    show_result=False
                )
                
                # Sử dụng frame hiện tại
                crossed_status, annotated_frame = self.detector.process_ballot(
                    frame, visualize=True
                )
                
                classification = self.classifier.classify_ballot(crossed_status)
                
                self.collector.add_ballot(
                    crossed_status,
                    ballot_id=ballot_id,
                    metadata={'source': 'webcam', 'camera_id': camera_id}
                )
                
                print(f"Kết quả: {classification['status_message']}")
                print(f"Người được bầu: {', '.join(classification['voted_for']) if classification['voted_for'] else 'Không có'}")
                
                # Hiển thị kết quả
                cv2.imshow("Detection Result", annotated_frame)
                
                # Kiểm tra giới hạn
                if max_ballots and ballot_count >= max_ballots:
                    print(f"\n✅ Đã đạt giới hạn {max_ballots} phiếu")
                    break
            
            elif key == ord('s'):  # Thống kê
                self.collector.print_statistics()
            
            elif key == ord('q'):  # Thoát
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✅ Đã xử lý {ballot_count} phiếu từ webcam")
    
    def export_results(self, output_path=None, include_stats=True):
        """
        Xuất kết quả ra Excel
        
        Args:
            output_path: Đường dẫn file output
            include_stats: Include statistics sheet
            
        Returns:
            Đường dẫn file đã xuất
        """
        if len(self.collector.ballots) == 0:
            print("❌ Không có dữ liệu để xuất!")
            return None
        
        print(f"\n{'='*70}")
        print("XUẤT KẾT QUẢ RA EXCEL")
        print(f"{'='*70}")
        
        # Hiển thị thống kê trước khi xuất
        self.collector.print_statistics()
        
        # Xuất Excel
        output_file = self.exporter.export_to_excel(
            self.collector.get_ballots(),
            output_path=output_path,
            include_statistics=include_stats
        )
        
        return output_file
    
    def reset(self):
        """Reset dữ liệu đã thu thập"""
        self.collector.clear()
        print("\n🔄 Đã reset dữ liệu")


# ==================== MAIN INTERFACE ====================

def main():
    """Giao diện chính"""
    
    print("\n" + "="*70)
    print("BALLOT PROCESSING PIPELINE - FULL SYSTEM")
    print("BƯỚC 1 + BƯỚC 2: ROI Detection -> Classification -> Excel Export")
    print("="*70)
    
    # Kiểm tra model tồn tại
    if not os.path.exists(config.MODEL_PATH):
        print(f"\n❌ CẢNH BÁO: Không tìm thấy model tại: {config.MODEL_PATH}")
        print("Vui lòng đặt file best.pt vào thư mục models/")
        return
    
    # Khởi tạo pipeline
    try:
        pipeline = BallotProcessingPipeline()
    except Exception as e:
        print(f"\n❌ Lỗi khởi tạo: {e}")
        return
    
    # Menu
    while True:
        print("\n" + "="*70)
        print("CHỌN CHỨC NĂNG:")
        print("="*70)
        print("1. Xử lý 1 ảnh")
        print("2. Xử lý tất cả ảnh trong folder")
        print("3. Xử lý từ webcam real-time")
        print("4. Xem thống kê hiện tại")
        print("5. Xuất Excel")
        print("6. Reset dữ liệu")
        print("0. Thoát")
        
        choice = input("\nNhập lựa chọn: ").strip()
        
        if choice == "1":
            image_path = input("Nhập đường dẫn ảnh: ").strip()
            if os.path.exists(image_path):
                pipeline.process_image(image_path, show_result=True)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print(f"❌ File không tồn tại: {image_path}")
        
        elif choice == "2":
            folder_path = input("Nhập đường dẫn folder: ").strip()
            if os.path.isdir(folder_path):
                pattern = input("Pattern (mặc định *.jpg): ").strip() or "*.jpg"
                pipeline.process_folder(folder_path, pattern=pattern, show_result=True)
            else:
                print(f"❌ Folder không tồn tại: {folder_path}")
        
        elif choice == "3":
            camera_id = input("ID Camera (mặc định 0): ").strip()
            camera_id = int(camera_id) if camera_id else 0
            
            max_str = input("Số phiếu tối đa (Enter = không giới hạn): ").strip()
            max_ballots = int(max_str) if max_str else None
            
            pipeline.process_webcam(camera_id=camera_id, max_ballots=max_ballots)
        
        elif choice == "4":
            pipeline.collector.print_statistics()
        
        elif choice == "5":
            output_path = input("Đường dẫn file output (Enter = tự động): ").strip()
            output_path = output_path if output_path else None
            pipeline.export_results(output_path=output_path)
        
        elif choice == "6":
            confirm = input("Xác nhận reset tất cả dữ liệu? (y/n): ").strip().lower()
            if confirm == 'y':
                pipeline.reset()
        
        elif choice == "0":
            # Hỏi có muốn xuất Excel trước khi thoát
            if len(pipeline.collector.ballots) > 0:
                export = input("\nCó dữ liệu chưa xuất. Xuất Excel trước khi thoát? (y/n): ").strip().lower()
                if export == 'y':
                    pipeline.export_results()
            
            print("\n👋 Tạm biệt!")
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
