"""
DEMO BƯỚC 2: Tích hợp BƯỚC 1 + BƯỚC 2
Demo xử lý phiếu bầu từ đầu đến cuối:
1. Load model (BƯỚC 1)
2. Detect vết gạch (BƯỚC 1)
3. Phân loại phiếu (BƯỚC 2)
4. Thu thập dữ liệu (BƯỚC 2)
5. Xuất Excel (BƯỚC 2)
"""

import cv2
import numpy as np
from step1_roi_detection import BallotROIDetector
from step2_ballot_classifier import (
    BallotClassifier, 
    BallotDataCollector, 
    ExcelExporter,
    process_and_classify_ballot
)
import config


def create_sample_ballots():
    """
    Tạo 10 phiếu bầu mẫu để test
    """
    ballots = []
    
    # Tạo các trường hợp khác nhau
    samples = [
        ([1, 1, 0, 1, 1], "Phiếu 1 - Bầu 1 người (Lê Văn C)"),
        ([1, 0, 0, 1, 1], "Phiếu 2 - Bầu 2 người (Trần Thị B, Lê Văn C)"),
        ([0, 0, 1, 1, 0], "Phiếu 3 - Bầu 3 người (A, B, E)"),
        ([1, 0, 1, 0, 1], "Phiếu 4 - Bầu 2 người (Trần Thị B, Phạm Thị D)"),
        ([0, 1, 1, 0, 1], "Phiếu 5 - Bầu 2 người (Nguyễn Văn A, Phạm Thị D)"),
        ([1, 1, 1, 0, 0], "Phiếu 6 - Bầu 2 người (Phạm Thị D, Hoàng Văn E)"),
        ([0, 1, 0, 1, 1], "Phiếu 7 - Bầu 2 người (Nguyễn Văn A, Lê Văn C)"),
        ([1, 1, 0, 1, 0], "Phiếu 8 - Bầu 2 người (Lê Văn C, Hoàng Văn E)"),
        ([0, 0, 0, 0, 0], "Phiếu 9 - KHÔNG HỢP LỆ (không gạch ai)"),
        ([1, 1, 1, 1, 1], "Phiếu 10 - KHÔNG HỢP LỆ (gạch tất cả)"),
    ]
    
    for crossed_status, description in samples:
        ballots.append({
            'crossed_status': crossed_status,
            'description': description
        })
    
    return ballots


def create_visual_ballot(crossed_status, ballot_desc, width=1200, height=600):
    """
    Tạo ảnh phiếu bầu có visualization
    """
    # Tạo ảnh nền trắng
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Tính ROI zones (vertical layout)
    zone_height = height // 5
    roi_zones = []
    for i in range(5):
        y1 = i * zone_height
        y2 = (i + 1) * zone_height if i < 4 else height
        roi_zones.append((0, y1, width, y2))
    
    # Vẽ header
    cv2.putText(img, ballot_desc, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    # Vẽ từng vùng ROI
    for idx, (x1, y1, x2, y2) in enumerate(roi_zones):
        name = config.CANDIDATE_NAMES[idx]
        is_crossed = crossed_status[idx] == 1
        
        # Vẽ khung
        color = (0, 0, 255) if is_crossed else (0, 255, 0)
        cv2.rectangle(img, (x1 + 10, y1 + 10), (x2 - 10, y2 - 10), color, 2)
        
        # Vẽ tên ứng viên
        center_y = (y1 + y2) // 2
        cv2.putText(img, f"{idx+1}. {name}", (30, center_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Vẽ vết gạch nếu có
        if is_crossed:
            line_y = center_y + 10
            cv2.line(img, (50, line_y), (width - 50, line_y), (0, 0, 255), 8)
            cv2.putText(img, "GACH", (width - 150, center_y + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(img, "OK", (width - 150, center_y + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return img


def demo_full_pipeline():
    """
    Demo đầy đủ pipeline từ BƯỚC 1 đến BƯỚC 2
    """
    print("\n" + "="*70)
    print("DEMO: FULL PIPELINE - BƯỚC 1 + BƯỚC 2")
    print("="*70)
    
    # Khởi tạo các components
    print("\n1. Khởi tạo components...")
    classifier = BallotClassifier()
    collector = BallotDataCollector()
    exporter = ExcelExporter()
    
    # Tạo dữ liệu mẫu
    print("2. Tạo 10 phiếu bầu mẫu...")
    sample_ballots = create_sample_ballots()
    
    # Xử lý từng phiếu
    print("\n3. Xử lý từng phiếu:")
    print("="*70)
    
    for idx, ballot in enumerate(sample_ballots, 1):
        crossed_status = ballot['crossed_status']
        description = ballot['description']
        
        print(f"\n{description}")
        print(f"  Trạng thái gạch: {crossed_status}")
        
        # Phân loại (BƯỚC 2)
        classification = classifier.classify_ballot(crossed_status)
        print(f"  -> {classification['status_message']}")
        print(f"  -> Người được bầu: {', '.join(classification['voted_for']) if classification['voted_for'] else 'Không có'}")
        
        # Thu thập dữ liệu
        collector.add_ballot(
            crossed_status,
            ballot_id=f"PHIEU_{idx:04d}",
            metadata={
                'description': description,
                'source': 'demo_generated'
            }
        )
    
    # Hiển thị thống kê
    print("\n" + "="*70)
    print("4. THỐNG KÊ TỔNG HỢP:")
    collector.print_statistics()
    
    # Xuất Excel
    print("\n5. Xuất dữ liệu ra Excel...")
    output_file = exporter.export_to_excel(
        collector.get_ballots(),
        output_path="output/demo_full_results.xlsx",
        include_statistics=True
    )
    
    if output_file:
        print(f"\n✅ DEMO HOÀN TẤT!")
        print(f"File Excel đã được lưu tại: {output_file}")
        print("\nFile Excel bao gồm 3 sheets:")
        print("  1. Chi tiết phiếu - Dữ liệu từng phiếu bầu")
        print("  2. Thống kê - Tổng hợp số liệu")
        print("  3. Kết quả ứng viên - Thứ hạng và số phiếu")
    else:
        print("\n❌ Có lỗi khi xuất file")


def demo_with_visualization():
    """
    Demo có hiển thị ảnh visualization
    """
    print("\n" + "="*70)
    print("DEMO: WITH VISUALIZATION")
    print("="*70)
    print("\nDemo này sẽ tạo và hiển thị ảnh cho từng phiếu bầu")
    print("Nhấn phím bất kỳ để xem phiếu tiếp theo, 'q' để thoát")
    
    # Khởi tạo
    classifier = BallotClassifier()
    collector = BallotDataCollector()
    
    # Tạo dữ liệu mẫu
    sample_ballots = create_sample_ballots()
    
    print(f"\nTổng số phiếu: {len(sample_ballots)}")
    input("\nNhấn Enter để bắt đầu...")
    
    for idx, ballot in enumerate(sample_ballots, 1):
        crossed_status = ballot['crossed_status']
        description = ballot['description']
        
        # Tạo ảnh visualization
        img = create_visual_ballot(crossed_status, description)
        
        # Phân loại
        classification = classifier.classify_ballot(crossed_status)
        
        # Thêm kết quả vào ảnh
        result_y = img.shape[0] - 80
        cv2.putText(img, f"Ket qua: {classification['status_message']}", 
                   (20, result_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        voted_names = ', '.join(classification['voted_for']) if classification['voted_for'] else 'Khong co'
        cv2.putText(img, f"Duoc bau: {voted_names}", 
                   (20, result_y + 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 128, 0), 2)
        
        # Hiển thị
        cv2.imshow("Ballot Visualization", img)
        
        # In ra console
        print(f"\n[{idx}/{len(sample_ballots)}] {description}")
        print(f"  {classification['status_message']}")
        
        # Đợi phím bấm
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        
        # Thu thập dữ liệu
        collector.add_ballot(crossed_status, ballot_id=f"PHIEU_{idx:04d}")
    
    cv2.destroyAllWindows()
    
    # Thống kê và xuất
    collector.print_statistics()
    
    exporter = ExcelExporter()
    output_file = exporter.export_to_excel(
        collector.get_ballots(),
        output_path="output/demo_visual_results.xlsx"
    )
    
    print(f"\n✅ Đã xuất file: {output_file}")


def demo_interactive():
    """
    Demo tương tác: Người dùng nhập trạng thái gạch
    """
    print("\n" + "="*70)
    print("DEMO: INTERACTIVE MODE")
    print("="*70)
    print("\nNhập trạng thái gạch cho 5 người (1=gạch, 0=không gạch)")
    print("Ví dụ: 1,0,0,1,1 (nghĩa là gạch người 1, 4, 5)")
    
    classifier = BallotClassifier()
    collector = BallotDataCollector()
    
    ballot_count = 0
    
    while True:
        print("\n" + "-"*70)
        print(f"Phiếu số {ballot_count + 1}")
        print("Tên ứng viên:")
        for i, name in enumerate(config.CANDIDATE_NAMES, 1):
            print(f"  {i}. {name}")
        
        user_input = input("\nNhập trạng thái gạch (hoặc 'x' để kết thúc): ").strip()
        
        if user_input.lower() == 'x':
            break
        
        # Parse input
        try:
            values = [int(x.strip()) for x in user_input.split(',')]
            if len(values) != 5:
                print("❌ Lỗi: Cần nhập đúng 5 giá trị!")
                continue
            if not all(v in [0, 1] for v in values):
                print("❌ Lỗi: Chỉ được nhập 0 hoặc 1!")
                continue
            
            crossed_status = values
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            continue
        
        # Phân loại
        classification = classifier.classify_ballot(crossed_status)
        
        # Hiển thị kết quả
        print("\n" + "="*50)
        print("KẾT QUẢ:")
        print("="*50)
        print(f"Trạng thái: {classification['status_message']}")
        print(f"\nNgười ĐƯỢC BẦU:")
        for name in classification['voted_for']:
            print(f"  ✓ {name}")
        print(f"\nNgười BỊ GẠCH:")
        for name in classification['crossed_for']:
            print(f"  ✗ {name}")
        
        # Thu thập
        ballot_count += 1
        collector.add_ballot(crossed_status, ballot_id=f"PHIEU_{ballot_count:04d}")
        
        print(f"\n✅ Đã thêm phiếu {ballot_count}")
    
    # Kết thúc
    if ballot_count > 0:
        collector.print_statistics()
        
        # Xuất Excel
        export = input("\nXuất ra Excel? (y/n): ").strip().lower()
        if export == 'y':
            exporter = ExcelExporter()
            output_file = exporter.export_to_excel(
                collector.get_ballots(),
                output_path="output/interactive_results.xlsx"
            )
            print(f"\n✅ Đã xuất file: {output_file}")
    else:
        print("\nKhông có phiếu nào được thêm.")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("DEMO BƯỚC 2: BALLOT CLASSIFICATION & EXCEL EXPORT")
    print("="*70)
    print("\nChọn chế độ demo:")
    print("1. Full Pipeline (tự động xử lý 10 phiếu mẫu)")
    print("2. With Visualization (hiển thị ảnh từng phiếu)")
    print("3. Interactive Mode (nhập thủ công)")
    
    choice = input("\nNhập lựa chọn (1/2/3): ").strip()
    
    if choice == "1":
        demo_full_pipeline()
    elif choice == "2":
        demo_with_visualization()
    elif choice == "3":
        demo_interactive()
    else:
        print("Lựa chọn không hợp lệ!")
        demo_full_pipeline()  # Mặc định chạy full pipeline
