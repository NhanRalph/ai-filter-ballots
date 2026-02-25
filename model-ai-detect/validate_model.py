"""
Validate trained model on validation dataset
"""

from ultralytics import YOLO
import torch
import os
import sys


def validate_model(model_path=None):
    """Validate model on validation set"""
    
    print("="*70)
    print("MODEL VALIDATION")
    print("="*70)
    
    # Default model path
    if model_path is None:
        model_path = "models/best.pt"
        
        # Try runs/train if not in models/
        if not os.path.exists(model_path):
            model_path = "runs/train/ballot_cross/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("\nĐường dẫn có thể:")
        print("   - models/best.pt")
        print("   - runs/train/ballot_cross/weights/best.pt")
        print("\nHoặc chạy training trước:")
        print("   python train_model.py")
        return None
    
    print(f"\n📦 Loading model: {model_path}")
    model = YOLO(model_path)
    print("✅ Model loaded successfully!")
    
    # Check dataset
    if not os.path.exists('dataset/data.yaml'):
        print("\n❌ Dataset not found: dataset/data.yaml")
        return None
    
    # Device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🔧 Device: {device}")
    
    # Validate
    print("\n🔍 Running validation on val dataset...")
    print("="*70)
    
    try:
        results = model.val(
            data='dataset/data.yaml',
            split='val',
            imgsz=640,
            batch=16,
            conf=0.25,
            iou=0.6,
            device=device,
            verbose=True
        )
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # Print metrics
    print("\n" + "="*70)
    print("📊 VALIDATION RESULTS")
    print("="*70)
    
    map50 = results.box.map50
    map50_95 = results.box.map
    precision = results.box.mp
    recall = results.box.mr
    
    print(f"\nmAP50:     {map50:.4f} (Mean Average Precision @ IoU=0.5)")
    print(f"mAP50-95:  {map50_95:.4f} (Mean Average Precision @ IoU=0.5:0.95)")
    print(f"Precision: {precision:.4f} (Accuracy of positive predictions)")
    print(f"Recall:    {recall:.4f} (Coverage of actual positives)")
    
    # Interpretation
    print("\n" + "="*70)
    print("💡 INTERPRETATION")
    print("="*70)
    
    print(f"\n📈 mAP50 = {map50:.4f}")
    if map50 > 0.9:
        print("   ✅ EXCELLENT - Model rất tốt!")
        print("   → Sẵn sàng production")
    elif map50 > 0.8:
        print("   ✅ GOOD - Model tốt")
        print("   → Có thể dùng production")
    elif map50 > 0.6:
        print("   ⚠️  OK - Model tạm được")
        print("   → Nên cải thiện thêm")
        print("\n   💡 Suggestions:")
        print("      - Thu thập thêm ảnh training")
        print("      - Kiểm tra label có chính xác không")
        print("      - Tăng epochs (200-300)")
    else:
        print("   ❌ POOR - Model chưa tốt")
        print("   → Cần train lại")
        print("\n   💡 Suggestions:")
        print("      - Thu thập nhiều ảnh hơn (500+)")
        print("      - Re-label dataset với công cụ tốt hơn")
        print("      - Dùng model lớn hơn (yolov8m)")
        print("      - Tăng epochs (200-300)")
        print("      - Augmentation mạnh hơn")
    
    print(f"\n🎯 Precision = {precision:.4f}")
    if precision > 0.9:
        print("   ✅ HIGH - Ít false positives")
    elif precision > 0.7:
        print("   ⚠️  OK - Có một số false positives")
    else:
        print("   ❌ LOW - Nhiều false positives")
        print("      → Model detect sai nhiều")
    
    print(f"\n🎯 Recall = {recall:.4f}")
    if recall > 0.9:
        print("   ✅ HIGH - Detect hầu hết crosses")
    elif recall > 0.7:
        print("   ⚠️  OK - Miss một số crosses")
    else:
        print("   ❌ LOW - Miss nhiều crosses")
        print("      → Model bỏ sót nhiều")
    
    # Recommendations
    print("\n" + "="*70)
    print("📋 NEXT STEPS")
    print("="*70)
    
    if map50 > 0.8:
        print("\n✅ Model đủ tốt! Tiếp tục:")
        print("   1. Test với ảnh mới: python test_model.py")
        print("   2. Dùng trong app:   python step3_ui_app.py")
        print("   3. Optimize model:   python step4_convert_model.py")
    else:
        print("\n⚠️  Model chưa tốt. Cần cải thiện:")
        print("   1. Thu thập thêm ảnh (goal: 500+)")
        print("   2. Re-label dataset")
        print("   3. Train lại với cấu hình tốt hơn")
        print("   4. Validate lại")
    
    return results


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("🔍 MODEL VALIDATION UTILITY")
    print("="*70)
    
    # Check model
    paths_to_try = [
        "models/best.pt",
        "runs/train/ballot_cross/weights/best.pt",
    ]
    
    model_path = None
    for path in paths_to_try:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        print("\n❌ Không tìm thấy model!")
        print("\nThử các đường dẫn:")
        for path in paths_to_try:
            print(f"   - {path}: {'✅ Found' if os.path.exists(path) else '❌ Not found'}")
        
        print("\n💡 Giải pháp:")
        print("   1. Chạy training: python train_model.py")
        print("   2. Hoặc chỉ định path:")
        
        manual_path = input("\nNhập path model (Enter = skip): ").strip()
        if manual_path and os.path.exists(manual_path):
            model_path = manual_path
        else:
            print("❌ Exiting...")
            sys.exit(1)
    
    # Validate
    results = validate_model(model_path)
    
    if results is None:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Bye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
