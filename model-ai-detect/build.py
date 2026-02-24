"""
BƯỚC 4: Build Script - Đóng gói ứng dụng thành .exe
Tự động hóa quá trình build với PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_requirements():
    """Kiểm tra requirements đã được cài đặt chưa"""
    print("="*70)
    print("KIỂM TRA YÊU CẦU")
    print("="*70)
    
    required_packages = [
        'pyinstaller',
        'ultralytics',
        'opencv-python',
        'customtkinter',
        'pandas',
        'openpyxl',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Thiếu {len(missing)} package(s)")
        print(f"Cài đặt: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Tất cả requirements đã được cài đặt!")
    return True


def check_model():
    """Kiểm tra model file tồn tại"""
    print("\n" + "="*70)
    print("KIỂM TRA MODEL")
    print("="*70)
    
    model_path = Path("models/best.pt")
    onnx_path = Path("models/best.onnx")
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ PyTorch model: {model_path} ({size_mb:.2f} MB)")
    else:
        print(f"❌ PyTorch model không tồn tại: {model_path}")
    
    if onnx_path.exists():
        size_mb = onnx_path.stat().st_size / (1024 * 1024)
        print(f"✅ ONNX model: {onnx_path} ({size_mb:.2f} MB)")
    else:
        print(f"⚠️  ONNX model chưa có: {onnx_path}")
        print("   Khuyến nghị convert sang ONNX trước khi build (nhỏ hơn, nhanh hơn)")
    
    if not model_path.exists() and not onnx_path.exists():
        print("\n❌ Không tìm thấy model nào!")
        return False
    
    return True


def clean_build():
    """Xóa các thư mục build cũ"""
    print("\n" + "="*70)
    print("DỌN DẸP THỦ MỤC BUILD CŨ")
    print("="*70)
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"🗑️  Xóa: {d}/")
            shutil.rmtree(d)
            print(f"✅ Đã xóa: {d}/")
    
    # Xóa .spec cũ nếu cần
    # if os.path.exists('ballot_app.spec'):
    #     os.remove('ballot_app.spec')
    
    print("✅ Hoàn tất dọn dẹp!")


def build_exe(use_spec=True):
    """Build .exe với PyInstaller"""
    print("\n" + "="*70)
    print("BUILD EXECUTABLE")
    print("="*70)
    
    if use_spec and os.path.exists('ballot_app.spec'):
        print("📄 Sử dụng file .spec có sẵn")
        cmd = ['pyinstaller', 'ballot_app.spec', '--clean']
    else:
        print("🔧 Tạo build mới từ script")
        cmd = [
            'pyinstaller',
            '--name=BallotVerification',
            '--onedir',  # Tạo thư mục (không phải 1 file)
            '--windowed',  # Không hiện console
            '--clean',
            '--add-data=config.py:.',
            '--add-data=models:models',
            '--hidden-import=PIL._tkinter_finder',
            '--hidden-import=openpyxl',
            '--hidden-import=customtkinter',
            '--collect-all=ultralytics',
            '--collect-all=cv2',
            '--collect-all=customtkinter',
            'step3_ui_app.py'
        ]
    
    print(f"🔨 Command: {' '.join(cmd)}")
    print("\n⏳ Building... (có thể mất 5-10 phút)")
    print("="*70)
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        print("\n" + "="*70)
        print("✅ BUILD THÀNH CÔNG!")
        print("="*70)
        
        # Kiểm tra output
        dist_dir = Path("dist/BallotVerification")
        if dist_dir.exists():
            exe_file = dist_dir / "BallotVerification.exe"
            if exe_file.exists():
                size_mb = exe_file.stat().st_size / (1024 * 1024)
                print(f"\n📦 Executable: {exe_file}")
                print(f"📊 Size: {size_mb:.2f} MB")
                
                # Tính tổng size
                total_size = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file())
                total_mb = total_size / (1024 * 1024)
                print(f"📊 Total package size: {total_mb:.2f} MB")
                
                print(f"\n✅ Ứng dụng đã sẵn sàng tại: dist/BallotVerification/")
                print(f"🚀 Để chạy: cd dist/BallotVerification && ./BallotVerification.exe")
                
                return True
        
        print("⚠️  Build hoàn tất nhưng không tìm thấy .exe")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ BUILD FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_readme_dist():
    """Tạo README cho thư mục dist"""
    
    readme_content = """# Ballot Verification System

## Hướng dẫn sử dụng

### Chạy ứng dụng
1. Mở thư mục `BallotVerification/`
2. Double-click `BallotVerification.exe`
3. Ứng dụng sẽ khởi động

### Yêu cầu hệ thống
- Windows 10/11 (64-bit)
- Webcam (nếu dùng chức năng camera)
- RAM: Tối thiểu 4GB, khuyến nghị 8GB
- Không cần cài đặt Python hay bất kỳ thư viện nào

### Thư mục quan trọng
- `output/` - Kết quả xuất Excel
- `models/` - Model AI (đã được đóng gói sẵn)

### Cách sử dụng
1. **Chọn nguồn ảnh**:
   - Nhấn "Khởi động Camera" để dùng webcam
   - Nhấn "Tải ảnh" để chọn ảnh có sẵn

2. **Phân tích phiếu**:
   - Nhấn "Chụp & Phân tích" (nếu dùng camera)
   - Hệ thống sẽ tự động phát hiện dấu X và xác định kết quả

3. **Xuất kết quả**:
   - Nhấn "Xuất Excel" để lưu kết quả
   - File Excel gồm 3 sheet: Chi tiết, Thống kê, Kết quả ứng viên

### Khắc phục sự cố

**Lỗi "Cannot find model"**:
- Đảm bảo thư mục `models/` có file model (best.pt hoặc best.onnx)

**Ứng dụng chạy chậm**:
- Đóng các ứng dụng khác
- Sử dụng model ONNX (nhanh hơn PyTorch)

**Camera không khởi động**:
- Kiểm tra webcam đã được cắm và bật
- Đóng các ứng dụng khác đang dùng camera

### Hỗ trợ
Liên hệ support để được hỗ trợ thêm.
"""
    
    dist_readme = Path("dist/BallotVerification/README.txt")
    if dist_readme.parent.exists():
        dist_readme.write_text(readme_content, encoding='utf-8')
        print(f"📄 Đã tạo: {dist_readme}")


def main():
    """Main build process"""
    
    print("\n" + "="*70)
    print("🚀 BALLOT VERIFICATION SYSTEM - BUILD SCRIPT")
    print("="*70)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("\n❌ Vui lòng cài đặt các package thiếu trước!")
        sys.exit(1)
    
    # Step 2: Check model
    if not check_model():
        print("\n❌ Vui lòng đặt model vào thư mục models/")
        sys.exit(1)
    
    # Step 3: Confirm
    print("\n" + "="*70)
    print("SẴN SÀNG BUILD")
    print("="*70)
    print("⚠️  Quá trình build sẽ:")
    print("   1. Xóa thư mục build/dist cũ")
    print("   2. Đóng gói ứng dụng thành .exe (5-10 phút)")
    print("   3. Tạo thư mục dist/BallotVerification/")
    
    confirm = input("\nTiếp tục? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Đã hủy")
        sys.exit(0)
    
    # Step 4: Clean
    clean_build()
    
    # Step 5: Build
    success = build_exe(use_spec=True)
    
    if success:
        # Step 6: Create README
        create_readme_dist()
        
        print("\n" + "="*70)
        print("🎉 HOÀN TẤT!")
        print("="*70)
        print("\n📦 Package location: dist/BallotVerification/")
        print("\n📋 Bước tiếp theo:")
        print("   1. Test ứng dụng: cd dist/BallotVerification && ./BallotVerification.exe")
        print("   2. Nén thành .zip để phân phối")
        print("   3. Hoặc tạo installer với Inno Setup / NSIS")
        
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
