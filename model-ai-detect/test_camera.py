"""
Script test camera - Kiểm tra camera devices available
Chạy script này trước để xem máy có những camera nào
"""

import cv2
import sys


def test_camera_devices():
    """Test các camera devices từ 0-9"""
    
    print("="*70)
    print("KIỂM TRA CAMERA DEVICES")
    print("="*70)
    print("\nĐang scan các camera device từ 0 đến 9...")
    print("(Có thể mất vài giây)\n")
    
    available_cameras = []
    
    for cam_id in range(10):
        print(f"Đang thử Camera {cam_id}... ", end="", flush=True)
        
        cap = cv2.VideoCapture(cam_id)
        
        if cap.isOpened():
            # Thử đọc 1 frame để chắc chắn
            ret, frame = cap.read()
            
            if ret and frame is not None:
                h, w, c = frame.shape
                print(f"✅ OK - Resolution: {w}x{h}")
                
                available_cameras.append({
                    'id': cam_id,
                    'width': w,
                    'height': h,
                    'fps': cap.get(cv2.CAP_PROP_FPS),
                })
            else:
                print("⚠️  Mở được nhưng không đọc được frame")
            
            cap.release()
        else:
            print("❌ Không khả dụng")
    
    print("\n" + "="*70)
    print("KẾT QUẢ")
    print("="*70)
    
    if available_cameras:
        print(f"\n✅ Tìm thấy {len(available_cameras)} camera(s):\n")
        
        for cam in available_cameras:
            print(f"📹 Camera {cam['id']}:")
            print(f"   - Resolution: {cam['width']}x{cam['height']}")
            print(f"   - FPS: {cam['fps']:.1f}")
            print()
        
        print("💡 Khuyến nghị:")
        print(f"   → Sử dụng Camera {available_cameras[0]['id']} trong ứng dụng")
        print(f"   → Hoặc thử các Camera khác: {[c['id'] for c in available_cameras]}")
        
    else:
        print("\n❌ KHÔNG TÌM THẤY CAMERA NÀO!\n")
        print("🔧 Các bước khắc phục:")
        print("   1. Kiểm tra webcam đã cắm USB (nếu dùng USB webcam)")
        print("   2. Kiểm tra quyền truy cập camera:")
        print("      Windows Settings > Privacy > Camera > Allow apps")
        print("   3. Đóng các app khác đang dùng camera:")
        print("      - Zoom, Teams, Skype, Discord")
        print("      - Browser (Google Meet, Messenger)")
        print("   4. Restart máy tính")
        print("   5. Update driver camera:")
        print("      Device Manager > Cameras > Update driver")
        print("\n📖 Xem thêm: CAMERA_SETUP_GUIDE.md")
    
    print("\n" + "="*70)
    return available_cameras


def test_specific_camera(cam_id: int):
    """Test chi tiết 1 camera cụ thể"""
    
    print(f"\n{'='*70}")
    print(f"TEST CHI TIẾT CAMERA {cam_id}")
    print("="*70)
    
    cap = cv2.VideoCapture(cam_id)
    
    if not cap.isOpened():
        print(f"\n❌ Không thể mở Camera {cam_id}!")
        return False
    
    print(f"\n✅ Camera {cam_id} đã mở thành công!")
    
    # Get properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"\n📊 Thông số:")
    print(f"   - Resolution: {width}x{height}")
    print(f"   - FPS: {fps:.1f}")
    print(f"   - Backend: {cap.getBackendName()}")
    
    # Capture và show preview
    print(f"\n📸 Đang capture 5 frames để test...")
    
    success_count = 0
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            success_count += 1
            print(f"   Frame {i+1}: ✅ OK ({frame.shape})")
        else:
            print(f"   Frame {i+1}: ❌ FAILED")
    
    cap.release()
    
    print(f"\n📈 Kết quả: {success_count}/5 frames thành công")
    
    if success_count >= 4:
        print("✅ Camera hoạt động TỐT!")
        return True
    elif success_count >= 2:
        print("⚠️  Camera hoạt động CHƯA ỔN ĐỊNH")
        return True
    else:
        print("❌ Camera hoạt động KÉM hoặc LỖI")
        return False


def interactive_test():
    """Test camera với preview window"""
    
    print("\n" + "="*70)
    print("INTERACTIVE CAMERA TEST")
    print("="*70)
    
    cam_id = input("\nNhập Camera ID muốn test (0-9, Enter = 0): ").strip()
    cam_id = int(cam_id) if cam_id else 0
    
    print(f"\nĐang mở Camera {cam_id}...")
    print("(Nhấn 'q' để thoát)")
    
    cap = cv2.VideoCapture(cam_id)
    
    if not cap.isOpened():
        print(f"\n❌ Không thể mở Camera {cam_id}!")
        return
    
    print("\n✅ Camera đã mở!")
    print("📹 Preview window sẽ hiện ra...")
    print("   - Nhấn 'q' để thoát")
    print("   - Nhấn 's' để capture screenshot")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Không đọc được frame!")
            break
        
        frame_count += 1
        
        # Draw info
        h, w = frame.shape[:2]
        cv2.putText(frame, f"Camera {cam_id} - Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Resolution: {w}x{h}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit, 's' to screenshot", 
                   (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow(f"Camera {cam_id} Test", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Thoát...")
            break
        elif key == ord('s'):
            filename = f"camera_{cam_id}_test_{frame_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Screenshot saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Đã capture {frame_count} frames")


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("🎥 CAMERA TEST UTILITY")
    print("="*70)
    print("\nChức năng:")
    print("1. Scan tất cả camera devices (0-9)")
    print("2. Test chi tiết 1 camera cụ thể")
    print("3. Interactive test với preview window")
    print("0. Thoát")
    
    choice = input("\nChọn chức năng (1/2/3/0): ").strip()
    
    if choice == '1':
        cameras = test_camera_devices()
        
        if cameras:
            # Ask to test specific
            test_more = input("\nBạn có muốn test chi tiết camera nào không? (y/n): ").strip().lower()
            if test_more == 'y':
                cam_id = input(f"Nhập Camera ID ({[c['id'] for c in cameras]}): ").strip()
                if cam_id and cam_id.isdigit():
                    test_specific_camera(int(cam_id))
    
    elif choice == '2':
        cam_id = input("Nhập Camera ID muốn test (0-9): ").strip()
        if cam_id and cam_id.isdigit():
            test_specific_camera(int(cam_id))
        else:
            print("❌ Camera ID không hợp lệ!")
    
    elif choice == '3':
        interactive_test()
    
    elif choice == '0':
        print("\n👋 Bye!")
        sys.exit(0)
    
    else:
        print("\n❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Bye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
