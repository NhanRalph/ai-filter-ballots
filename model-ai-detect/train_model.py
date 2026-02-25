""""""

















































































































































































































































































































        sys.exit(1)        traceback.print_exc()        import traceback        print(f"\n❌ Error: {e}")    except Exception as e:        sys.exit(0)        print("\n\n👋 Interrupted. Bye!")    except KeyboardInterrupt:        main()    try:if __name__ == "__main__":        sys.exit(1)        print("❌ Lựa chọn không hợp lệ!")    else:        )            model_size=model            imgsz=imgsz,            batch=batch,            epochs=epochs,        train_ballot_detector(                imgsz = int(input("Image size [640]: ").strip() or '640')        batch = int(input("Batch size [16]: ").strip() or '16')        epochs = int(input("Epochs [100]: ").strip() or '100')        model = input("Model size (n/s/m/l/x) [n]: ").strip() or 'n'                print("\n⚙️  Custom configuration:")    elif choice == '4':        train_ballot_detector(epochs=200, batch=16, model_size='m')    elif choice == '3':        train_ballot_detector(epochs=100, batch=16, model_size='n')    elif choice == '2':        train_ballot_detector(epochs=50, batch=16, model_size='n')    if choice == '1':        choice = input("\nChọn (1/2/3/4): ").strip()        print("\n4. Custom")        print("   - Time: ~2-3 giờ (GPU)")    print("   - Epochs: 200")    print("   - Model: yolov8m (Medium)")    print("\n3. High Quality")        print("   - Time: ~30-60 phút (GPU)")    print("   - Epochs: 100")    print("   - Model: yolov8n (Nano)")    print("\n2. Standard (Khuyến nghị)")        print("   - Time: ~15-30 phút (GPU)")    print("   - Epochs: 50")    print("   - Model: yolov8n (Nano)")    print("\n1. Quick (Fast training)")    print("\n📋 Chọn cấu hình training:")    # Training options            sys.exit(1)        print("   README_STEP0_TRAINING.md")        print("\n📖 Xem hướng dẫn chuẩn bị dataset:")        print("\n❌ Dataset chưa sẵn sàng!")    if not check_dataset():    # Check dataset        print("="*70)    print("🎓 YOLOV8 TRAINING UTILITY")    print("\n" + "="*70)        """Main function"""def main():        return f"{hours:.1f} giờ (CPU)"        hours = minutes / 60        minutes = epochs * 4        # ~3-5 min per epoch on CPU    else:        return f"{minutes:.0f}-{minutes*2:.0f} phút (GPU)"        minutes = epochs * 0.5        # ~0.3-1 min per epoch on GPU    if device == 'cuda':    """Estimate training time"""def estimate_time(epochs, device):    return results        print("   4. Optimize: python step4_convert_model.py")    print("   3. Use app:  python step3_ui_app.py")    print("   2. Test:     python test_model.py")    print("   1. Validate: python validate_model.py")    print("\n💡 Next steps:")    # Next steps            print(f"   cp {best_model} models/best.pt")        print(f"⚠️  Manual copy needed:")    except Exception as e:        print("✅ Copied to: models/best.pt")        shutil.copy(best_model, 'models/best.pt')        os.makedirs('models', exist_ok=True)        import shutil    try:    print("\n📂 Deploying model...")    # Copy to models/            print(f"   Recall:    {metrics.get('metrics/recall(B)', 'N/A')}")        print(f"   Precision: {metrics.get('metrics/precision(B)', 'N/A')}")        print(f"   mAP50-95:  {metrics.get('metrics/mAP50-95(B)', 'N/A')}")        print(f"   mAP50:     {metrics.get('metrics/mAP50(B)', 'N/A')}")        metrics = results.results_dict    if hasattr(results, 'results_dict'):    print(f"\n📊 Final Metrics:")    # Metrics            print(f"   Size:  {size_mb:.2f} MB")        size_mb = os.path.getsize(best_model) / (1024 * 1024)    if os.path.exists(best_model):        print(f"   Last:  {last_model}")    print(f"   Best:  {best_model}")    print(f"\n📦 Models saved:")        last_model = "runs/train/ballot_cross/weights/last.pt"    best_model = "runs/train/ballot_cross/weights/best.pt"    # Best model path        print("="*70)    print("✅ TRAINING COMPLETE!")    print("\n" + "="*70)    # Training complete            return None        traceback.print_exc()        import traceback        print(f"\n❌ Training failed: {e}")    except Exception as e:        return None        print("\n\n⚠️  Training interrupted by user")    except KeyboardInterrupt:        results = model.train(**config)    try:        print("="*70)    print("📊 Xem progress: tensorboard --logdir runs/train")    print("="*70)    print("\n🚀 Starting training...")    # Start training            return None        print("❌ Đã hủy training")    if confirm != 'y':    confirm = input("\nTiếp tục? (y/n): ").strip().lower()        print("="*70)    print(f"   - Output: runs/train/ballot_cross/weights/best.pt")    print(f"   - Estimated time: {estimate_time(epochs, device)} ")    print(f"   - Epochs: {epochs}")    print("⚠️  Sắp bắt đầu training!")    print("\n" + "="*70)    # Confirm            print(f"   {key}: {value}")    for key, value in config.items():        }        'mosaic': 1.0,        'fliplr': 0.5,        'flipud': 0.0,        'scale': 0.5,        'translate': 0.1,        'degrees': 10.0,        'hsv_v': 0.4,        'hsv_s': 0.7,        'hsv_h': 0.015,        # Augmentation                'weight_decay': 0.0005,        'momentum': 0.937,        'lrf': 0.01,        'lr0': 0.01,        'optimizer': 'SGD',        'cache': False,        'save_period': 10,        'save': True,        'patience': 20,        # Optimization                'exist_ok': True,        'name': 'ballot_cross',        'project': 'runs/train',        'workers': 4,        'device': device,        'batch': batch,        'imgsz': imgsz,        'epochs': epochs,        'data': 'dataset/data.yaml',    config = {    print(f"\n⚙️  Training configuration:")    # Training configuration        print(f"   Size: {model_sizes.get(model_size, 'Unknown')}")    }        'x': 'XLarge (Best accuracy, ~130MB)'        'l': 'Large (High accuracy, ~90MB)',        'm': 'Medium (Better accuracy, ~50MB)',        's': 'Small (Balanced, ~22MB)',        'n': 'Nano (Fastest, ~6MB)',    model_sizes = {    # Model info            model = YOLO(model_name)        print("   Downloading pretrained weights...")        print(f"❌ Lỗi load model: {e}")    except Exception as e:        print(f"✅ Model loaded: {model_name}")        model = YOLO(model_name)    try:        print(f"\n📦 Loading pretrained model: {model_name}")    model_name = f'yolov8{model_size}.pt'    # Load pretrained model            print("   💡 Khuyến nghị: Dùng Google Colab (Free GPU)")        print("   ⚠️  No GPU detected. Training sẽ chậm hơn.")    else:        print(f"   Memory: {gpu_memory:.2f} GB")        print(f"   GPU: {gpu_name}")        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9        gpu_name = torch.cuda.get_device_name(0)    if device == 'cuda':        print(f"\n🔧 Device: {device}")    device = 'cuda' if torch.cuda.is_available() else 'cpu'    # Check GPU        print("="*70)    print("TRAINING YOLOV8 - BALLOT CROSS DETECTION")    print("\n" + "="*70)        """        model_size: Model size (n/s/m/l/x)        imgsz: Image size (640 khuyến nghị)        batch: Batch size (4-32, tùy GPU)        epochs: Số epochs (100-300)    Args:        Train YOLOv8 model for ballot cross detection    """):    model_size='n'  # n=nano, s=small, m=medium, l=large, x=xlarge    imgsz=640,    batch=16,    epochs=100,def train_ballot_detector(    return True    print("\n✅ Dataset OK!")            return False        print("   Xem: README_STEP0_TRAINING.md")        print("\n📖 Hướng dẫn chuẩn bị dataset:")        print(f"\n❌ Thiếu {len(missing)} thành phần!")    if missing:                    print(f"✅ {path}")            else:                print(f"✅ {path} ({count} files)")                count = len([f for f in os.listdir(path) if not f.startswith('.')])            if os.path.isdir(path):        else:            print(f"❌ Thiếu: {path}")            missing.append(path)        if not os.path.exists(path):    for path in required_files:    missing = []        ]        'dataset/labels/val',        'dataset/labels/train',        'dataset/images/val',        'dataset/images/train',        'dataset/data.yaml',    required_files = [        print("="*70)    print("KIỂM TRA DATASET")    print("="*70)        """Kiểm tra dataset có đủ không"""def check_dataset():import sysimport osimport torchfrom ultralytics import YOLO"""Kết quả: models/best.ptChạy script này để train model từ dataset có nhãn.BƯỚC 0: Training Script - Train YOLOv8 model for ballot cross detectionBƯỚC 0: Train YOLOv8 Model - Cross Mark Detection
Script training đầy đủ cho ballot cross detection
"""

from ultralytics import YOLO
import torch
import os
from pathlib import Path


def check_dataset():
    """Kiểm tra dataset structure"""
    
    print("="*70)
    print("CHECKING DATASET")
    print("="*70)
    
    required_paths = [
        'dataset/data.yaml',
        'dataset/images/train',
        'dataset/images/val',
        'dataset/labels/train',
        'dataset/labels/val',
    ]
    
    all_ok = True
    for path in required_paths:
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"{status} {path}")
        if not exists:
            all_ok = False
    
    if not all_ok:
        print("\n❌ Dataset không đầy đủ!")
        print("\n📖 Xem hướng dẫn: README_STEP0_TRAINING.md")
        print("   Section: PHẦN 1 - Chuẩn Bị Dataset")
        return False
    
    # Count images
    train_images = len(list(Path('dataset/images/train').glob('*.jpg'))) + \
                   len(list(Path('dataset/images/train').glob('*.png')))
    val_images = len(list(Path('dataset/images/val').glob('*.jpg'))) + \
                 len(list(Path('dataset/images/val').glob('*.png')))
    
    print(f"\n📊 Dataset statistics:")
    print(f"   Train images: {train_images}")
    print(f"   Val images: {val_images}")
    print(f"   Total: {train_images + val_images}")
    
    if train_images < 50:
        print(f"\n⚠️  Cảnh báo: Train images < 50")
        print("   Khuyến nghị: Thu thập thêm ảnh (goal: 100-500)")
    
    print("\n✅ Dataset OK!")
    return True


def train_ballot_detector(
    model_size='n',  # n=nano, s=small, m=medium, l=large
    epochs=100,
    batch_size=16,
    image_size=640,
    device=None
):
    """
    Train YOLOv8 model for ballot cross detection
    
    Args:
        model_size: n/s/m/l (nano/small/medium/large)
        epochs: Number of training epochs
        batch_size: Batch size (adjust based on GPU memory)
        image_size: Input image size
        device: 'cuda', 'cpu', or None (auto-detect)
    """
    
    print("\n" + "="*70)
    print("TRAINING YOLOV8 - BALLOT CROSS DETECTION")
    print("="*70)
    
    # Auto-detect device
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"\n🔧 Configuration:")
    print(f"   Device: {device}")
    
    if device == 'cuda':
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"   GPU: {gpu_name}")
        print(f"   Memory: {gpu_memory:.2f} GB")
    else:
        print("   ⚠️  No GPU detected. Training will be slower.")
        print("   💡 Consider using Google Colab for free GPU")
    
    print(f"   Model: YOLOv8{model_size}")
    print(f"   Epochs: {epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Image size: {image_size}")
    
    # Load pretrained model
    model_name = f'yolov8{model_size}.pt'
    print(f"\n📦 Loading pretrained model: {model_name}")
    
    try:
        model = YOLO(model_name)
        print("   ✅ Model loaded!")
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        print("   💡 Model will be downloaded automatically on first run")
        return None
    
    # Training configuration
    config = {
        'data': 'dataset/data.yaml',
        'epochs': epochs,
        'imgsz': image_size,
        'batch': batch_size,
        'device': device,
        'workers': 4,
        'project': 'runs/train',
        'name': f'ballot_cross_{model_size}',
        'exist_ok': True,
        
        # Performance
        'patience': 20,
        'save': True,
        'save_period': 10,
        'cache': False,
        
        # Optimizer
        'optimizer': 'SGD',
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        
        # Loss
        'box': 7.5,
        'cls': 0.5,
        'dfl': 1.5,
        
        # Augmentation
        'hsv_h': 0.015,
        'hsv_s': 0.7,
        'hsv_v': 0.4,
        'degrees': 10.0,
        'translate': 0.1,
        'scale': 0.5,
        'shear': 0.0,
        'perspective': 0.0,
        'flipud': 0.0,
        'fliplr': 0.5,
        'mosaic': 1.0,
        'mixup': 0.0,
    }
    
    # Confirm
    print(f"\n⚙️  Ready to train!")
    print(f"   Output folder: runs/train/ballot_cross_{model_size}/")
    
    confirm = input("\n▶️  Start training? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Training cancelled")
        return None
    
    # Start training
    print("\n🚀 Starting training...")
    print("="*70)
    print("💡 Tips:")
    print("   - Monitor: tensorboard --logdir runs/train")
    print("   - Stop: Ctrl+C (will save checkpoint)")
    print("   - Resume: Set resume=True in model.train()")
    print("="*70)
    
    try:
        results = model.train(**config)
        
        # Training complete
        print("\n" + "="*70)
        print("✅ TRAINING COMPLETE!")
        print("="*70)
        
        # Best model path
        best_model = f"runs/train/ballot_cross_{model_size}/weights/best.pt"
        print(f"\n📦 Best model: {best_model}")
        
        # Metrics
        metrics = results.results_dict
        print(f"\n📊 Final Metrics:")
        print(f"   mAP50: {metrics.get('metrics/mAP50(B)', 'N/A'):.4f}")
        print(f"   mAP50-95: {metrics.get('metrics/mAP50-95(B)', 'N/A'):.4f}")
        print(f"   Precision: {metrics.get('metrics/precision(B)', 'N/A'):.4f}")
        print(f"   Recall: {metrics.get('metrics/recall(B)', 'N/A'):.4f}")
        
        # Interpretation
        map50 = metrics.get('metrics/mAP50(B)', 0)
        print(f"\n💡 Model quality:")
        if map50 > 0.9:
            print("   ✅ EXCELLENT - Ready for production!")
        elif map50 > 0.8:
            print("   ✅ GOOD - Can use in production")
        elif map50 > 0.6:
            print("   ⚠️  OK - Consider improving")
        else:
            print("   ❌ POOR - Need more training/data")
        
        # Next steps
        print(f"\n📋 Next steps:")
        print(f"   1. Copy model:")
        print(f"      cp {best_model} models/best.pt")
        print(f"   2. Validate:")
        print(f"      python validate_model.py")
        print(f"   3. Test in app:")
        print(f"      python step3_ui_app.py")
        
        return results
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Training interrupted!")
        print("   Checkpoint saved. Resume with resume=True")
        return None
    
    except Exception as e:
        print(f"\n❌ Training error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main training pipeline"""
    
    print("\n" + "="*70)
    print("🎯 YOLOV8 TRAINING - BALLOT CROSS DETECTION")
    print("="*70)
    
    # Step 1: Check dataset
    if not check_dataset():
        return
    
    # Step 2: Choose configuration
    print("\n" + "="*70)
    print("CONFIGURATION")
    print("="*70)
    
    print("\nModel size:")
    print("  n - Nano    (Fastest, lowest accuracy)")
    print("  s - Small   (Balanced)")
    print("  m - Medium  (Better accuracy, slower)")
    print("  l - Large   (Best accuracy, slowest)")
    
    model_size = input("\nChọn model size (n/s/m/l) [n]: ").strip().lower() or 'n'
    
    if model_size not in ['n', 's', 'm', 'l']:
        print("❌ Invalid choice!")
        model_size = 'n'
    
    # Epochs
    epochs_input = input("Number of epochs [100]: ").strip()
    epochs = int(epochs_input) if epochs_input else 100
    
    # Batch size
    if torch.cuda.is_available():
        default_batch = 16
    else:
        default_batch = 8
        print("⚠️  CPU mode: Using smaller batch size")
    
    batch_input = input(f"Batch size [{default_batch}]: ").strip()
    batch_size = int(batch_input) if batch_input else default_batch
    
    # Step 3: Train
    results = train_ballot_detector(
        model_size=model_size,
        epochs=epochs,
        batch_size=batch_size
    )
    
    if results:
        print("\n🎉 Training successful!")
    else:
        print("\n⚠️  Training failed or cancelled")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Bye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
