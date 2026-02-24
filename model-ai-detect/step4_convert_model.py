"""
BƯỚC 4: Convert Model sang ONNX
Script để convert YOLOv8 model (.pt) sang ONNX format
ONNX nhanh hơn và tương thích tốt hơn cho deployment
"""

import os
import sys
from pathlib import Path
from ultralytics import YOLO
import config


def convert_to_onnx(
    model_path: str = None,
    output_path: str = None,
    simplify: bool = True,
    dynamic: bool = False,
    opset: int = 12
):
    """
    Convert YOLOv8 model sang ONNX format
    
    Args:
        model_path: Đường dẫn model .pt (mặc định từ config)
        output_path: Đường dẫn output .onnx (mặc định models/best.onnx)
        simplify: Simplify model (giảm kích thước)
        dynamic: Dynamic batch size
        opset: ONNX opset version
    """
    
    # Default paths
    if model_path is None:
        model_path = config.MODEL_PATH
    
    if output_path is None:
        model_dir = Path(model_path).parent
        output_path = str(model_dir / "best.onnx")
    
    print("="*70)
    print("CONVERT YOLOV8 MODEL TO ONNX")
    print("="*70)
    
    # Kiểm tra model tồn tại
    if not os.path.exists(model_path):
        print(f"❌ Lỗi: Không tìm thấy model tại: {model_path}")
        print("Vui lòng đặt file best.pt vào thư mục models/")
        return False
    
    print(f"\n📂 Input model: {model_path}")
    print(f"📂 Output path: {output_path}")
    print(f"⚙️ Settings:")
    print(f"   - Simplify: {simplify}")
    print(f"   - Dynamic: {dynamic}")
    print(f"   - Opset: {opset}")
    
    try:
        # Load model
        print(f"\n⏳ Loading model...")
        model = YOLO(model_path)
        print("✅ Model loaded successfully!")
        
        # Get model info
        print(f"\n📊 Model info:")
        print(f"   - Task: {model.task}")
        
        # Export to ONNX
        print(f"\n⏳ Converting to ONNX...")
        print("This may take a few minutes...")
        
        export_path = model.export(
            format='onnx',
            simplify=simplify,
            dynamic=dynamic,
            opset=opset
        )
        
        # Rename if needed
        if export_path != output_path:
            import shutil
            shutil.move(export_path, output_path)
        
        # Check output
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"\n✅ CONVERSION SUCCESSFUL!")
            print(f"📂 Output: {output_path}")
            print(f"📦 Size: {file_size:.2f} MB")
            
            print(f"\n💡 Để sử dụng model ONNX:")
            print(f"   1. Cài đặt: pip install onnxruntime")
            print(f"   2. Update config.py: MODEL_PATH = '{output_path}'")
            print(f"   3. Chạy lại ứng dụng")
            
            return True
        else:
            print(f"\n❌ Lỗi: Không tìm thấy file output")
            return False
            
    except Exception as e:
        print(f"\n❌ Lỗi khi convert: {e}")
        import traceback
        traceback.print_exc()
        return False


def convert_to_openvino(
    model_path: str = None,
    output_dir: str = None,
    half: bool = False
):
    """
    Convert YOLOv8 model sang OpenVINO format
    OpenVINO tối ưu cho Intel CPU
    
    Args:
        model_path: Đường dẫn model .pt
        output_dir: Thư mục output (mặc định models/openvino/)
        half: Sử dụng FP16 (giảm kích thước 50%)
    """
    
    if model_path is None:
        model_path = config.MODEL_PATH
    
    if output_dir is None:
        model_dir = Path(model_path).parent
        output_dir = str(model_dir / "openvino")
    
    print("="*70)
    print("CONVERT YOLOV8 MODEL TO OPENVINO")
    print("="*70)
    
    if not os.path.exists(model_path):
        print(f"❌ Lỗi: Không tìm thấy model tại: {model_path}")
        return False
    
    print(f"\n📂 Input model: {model_path}")
    print(f"📂 Output dir: {output_dir}")
    print(f"⚙️ Half precision: {half}")
    
    try:
        print(f"\n⏳ Loading model...")
        model = YOLO(model_path)
        print("✅ Model loaded!")
        
        print(f"\n⏳ Converting to OpenVINO...")
        print("This may take a few minutes...")
        
        export_path = model.export(
            format='openvino',
            half=half
        )
        
        print(f"\n✅ CONVERSION SUCCESSFUL!")
        print(f"📂 Output: {export_path}")
        
        print(f"\n💡 Để sử dụng OpenVINO model:")
        print(f"   1. Cài đặt: pip install openvino")
        print(f"   2. Model files trong: {export_path}")
        print(f"   3. Update code để load OpenVINO model")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_onnx_speed(onnx_path: str = None, pt_path: str = None):
    """
    So sánh tốc độ inference giữa ONNX và PyTorch
    
    Args:
        onnx_path: Đường dẫn model ONNX
        pt_path: Đường dẫn model PyTorch
    """
    
    import time
    import cv2
    import numpy as np
    
    print("="*70)
    print("BENCHMARK: ONNX vs PyTorch")
    print("="*70)
    
    # Tạo dummy image
    test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    results = {}
    
    # Test PyTorch
    if pt_path and os.path.exists(pt_path):
        print(f"\n🔥 Testing PyTorch model...")
        model_pt = YOLO(pt_path)
        
        # Warmup
        for _ in range(3):
            _ = model_pt(test_image, verbose=False)
        
        # Benchmark
        times = []
        for i in range(10):
            start = time.time()
            _ = model_pt(test_image, verbose=False)
            times.append(time.time() - start)
        
        avg_time = np.mean(times) * 1000  # ms
        fps = 1000 / avg_time
        
        results['pytorch'] = {
            'avg_time_ms': avg_time,
            'fps': fps
        }
        
        print(f"✅ PyTorch: {avg_time:.2f}ms ({fps:.1f} FPS)")
    
    # Test ONNX
    if onnx_path and os.path.exists(onnx_path):
        print(f"\n⚡ Testing ONNX model...")
        
        try:
            import onnxruntime as ort
            
            # Load ONNX
            session = ort.InferenceSession(onnx_path)
            
            # Prepare input
            input_name = session.get_inputs()[0].name
            
            # Preprocess
            img = cv2.resize(test_image, (640, 640))
            img = img.transpose(2, 0, 1)  # HWC -> CHW
            img = np.expand_dims(img, 0)  # Add batch
            img = img.astype(np.float32) / 255.0
            
            # Warmup
            for _ in range(3):
                _ = session.run(None, {input_name: img})
            
            # Benchmark
            times = []
            for i in range(10):
                start = time.time()
                _ = session.run(None, {input_name: img})
                times.append(time.time() - start)
            
            avg_time = np.mean(times) * 1000  # ms
            fps = 1000 / avg_time
            
            results['onnx'] = {
                'avg_time_ms': avg_time,
                'fps': fps
            }
            
            print(f"✅ ONNX: {avg_time:.2f}ms ({fps:.1f} FPS)")
            
        except ImportError:
            print("❌ onnxruntime chưa được cài đặt")
            print("Cài đặt: pip install onnxruntime")
    
    # Summary
    if len(results) == 2:
        print(f"\n{'='*70}")
        print("📊 SUMMARY")
        print(f"{'='*70}")
        
        speedup = results['pytorch']['avg_time_ms'] / results['onnx']['avg_time_ms']
        
        print(f"PyTorch: {results['pytorch']['avg_time_ms']:.2f}ms")
        print(f"ONNX:    {results['onnx']['avg_time_ms']:.2f}ms")
        print(f"\n⚡ ONNX is {speedup:.2f}x faster!")
        
        if speedup > 1.5:
            print("✅ Khuyến nghị: Sử dụng ONNX cho production")
        else:
            print("ℹ️  Tốc độ tương đương, cả 2 đều OK")
    
    return results


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("BƯỚC 4: MODEL OPTIMIZATION")
    print("="*70)
    print("\nChọn chức năng:")
    print("1. Convert to ONNX (khuyến nghị)")
    print("2. Convert to OpenVINO (cho Intel CPU)")
    print("3. Benchmark: ONNX vs PyTorch")
    print("4. Convert cả 2 formats")
    
    choice = input("\nNhập lựa chọn (1/2/3/4): ").strip()
    
    if choice == "1":
        print("\n🔄 Converting to ONNX...")
        success = convert_to_onnx()
        
        if success:
            print("\n✅ Hoàn tất! Model ONNX đã sẵn sàng.")
            
            # Ask for benchmark
            test = input("\nBạn có muốn test tốc độ ONNX? (y/n): ").strip().lower()
            if test == 'y':
                onnx_path = "models/best.onnx"
                pt_path = config.MODEL_PATH
                test_onnx_speed(onnx_path, pt_path)
    
    elif choice == "2":
        print("\n🔄 Converting to OpenVINO...")
        success = convert_to_openvino()
        
        if success:
            print("\n✅ Hoàn tất! Model OpenVINO đã sẵn sàng.")
    
    elif choice == "3":
        onnx_path = input("Đường dẫn ONNX model (Enter = models/best.onnx): ").strip()
        onnx_path = onnx_path if onnx_path else "models/best.onnx"
        
        pt_path = input("Đường dẫn PyTorch model (Enter = config.MODEL_PATH): ").strip()
        pt_path = pt_path if pt_path else config.MODEL_PATH
        
        test_onnx_speed(onnx_path, pt_path)
    
    elif choice == "4":
        print("\n🔄 Converting to both formats...")
        
        print("\n" + "="*70)
        print("1/2: ONNX")
        print("="*70)
        onnx_success = convert_to_onnx()
        
        print("\n" + "="*70)
        print("2/2: OpenVINO")
        print("="*70)
        openvino_success = convert_to_openvino()
        
        if onnx_success and openvino_success:
            print("\n✅ Cả 2 format đã được convert thành công!")
        elif onnx_success:
            print("\n⚠️  ONNX OK, OpenVINO failed")
        elif openvino_success:
            print("\n⚠️  OpenVINO OK, ONNX failed")
        else:
            print("\n❌ Cả 2 đều failed")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
