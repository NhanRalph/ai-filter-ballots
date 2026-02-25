"""
Test trained model on new images
Visualize detection results
"""

from ultralytics import YOLO
import cv2
import os
import sys
from pathlib import Path


def test_model_on_images(model_path, image_folder, output_folder='test_results', conf=0.5):
    """
    Test model on folder of images
    
    Args:
        model_path: Path to trained model
        image_folder: Folder containing test images
        output_folder: Where to save results
        conf: Confidence threshold (0-1)
    """
    
    print("="*70)
    print("MODEL TESTING")
    print("="*70)
    
    # Check model
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        return False
    
    print(f"\n📦 Loading model: {model_path}")
    model = YOLO(model_path)
    print("✅ Model loaded!")
    
    # Check images
    if not os.path.exists(image_folder):
        print(f"\n❌ Image folder not found: {image_folder}")
        return False
    
    # Get all images
    image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP']
    image_files = []
    for ext in image_exts:
        image_files.extend(Path(image_folder).glob(f'*{ext}'))
    
    if not image_files:
        print(f"\n❌ No images found in {image_folder}")
        return False
    
    print(f"\n📁 Found {len(image_files)} images")
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    print(f"💾 Results will be saved to: {output_folder}/")
    
    # Process images
    print("\n🔍 Processing images...")
    print("="*70)
    
    results_summary = {
        'total': len(image_files),
        'with_detections': 0,
        'without_detections': 0,
        'total_crosses': 0
    }
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] {image_path.name}")
        
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"   ⚠️  Cannot read image")
            continue
        
        # Run detection
        results = model(img, conf=conf, verbose=False)
        
        # Count detections
        num_detections = len(results[0].boxes)
        results_summary['total_crosses'] += num_detections
        
        if num_detections > 0:
            results_summary['with_detections'] += 1
            print(f"   ✅ Detected {num_detections} cross(es)")
        else:
            results_summary['without_detections'] += 1
            print(f"   ⚪ No detections")
        
        # Draw results
        annotated = results[0].plot()
        
        # Save
        output_path = os.path.join(output_folder, f"result_{image_path.name}")
        cv2.imwrite(output_path, annotated)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    print(f"\nProcessed:         {results_summary['total']} images")
    print(f"With detections:   {results_summary['with_detections']} images")
    print(f"Without:           {results_summary['without_detections']} images")
    print(f"Total crosses:     {results_summary['total_crosses']}")
    print(f"Average per image: {results_summary['total_crosses']/results_summary['total']:.2f}")
    
    print(f"\n💾 Results saved to: {output_folder}/")
    
    return True


def test_single_image(model_path, image_path, conf=0.5):
    """Test model on single image with preview"""
    
    print("="*70)
    print("SINGLE IMAGE TEST")
    print("="*70)
    
    # Load model
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        return False
    
    print(f"\n📦 Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Read image
    if not os.path.exists(image_path):
        print(f"\n❌ Image not found: {image_path}")
        return False
    
    print(f"📷 Testing: {image_path}")
    
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Cannot read image")
        return False
    
    # Run detection
    print(f"\n🔍 Running detection (conf={conf})...")
    results = model(img, conf=conf, verbose=False)
    
    # Results
    num_detections = len(results[0].boxes)
    print(f"\n✅ Detected {num_detections} cross(es)")
    
    if num_detections > 0:
        print("\n📋 Detections:")
        for i, box in enumerate(results[0].boxes, 1):
            conf = box.conf[0]
            xyxy = box.xyxy[0]
            print(f"   {i}. Confidence: {conf:.3f}, Box: [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")
    
    # Draw results
    annotated = results[0].plot()
    
    # Show
    print("\n👁️  Showing result... (Press any key to close)")
    cv2.imshow('Detection Result', annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save option
    save = input("\n💾 Save result? (y/n): ").strip().lower()
    if save == 'y':
        output_name = f"test_result_{Path(image_path).name}"
        cv2.imwrite(output_name, annotated)
        print(f"✅ Saved: {output_name}")
    
    return True


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("🧪 MODEL TESTING UTILITY")
    print("="*70)
    
    # Find model
    model_paths = [
        "models/best.pt",
        "runs/train/ballot_cross/weights/best.pt",
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        print("\n❌ Model not found!")
        print("\nTried:")
        for path in model_paths:
            print(f"   - {path}")
        
        manual = input("\nEnter model path (or Enter to exit): ").strip()
        if manual and os.path.exists(manual):
            model_path = manual
        else:
            print("Exiting...")
            sys.exit(1)
    
    print(f"\n📦 Using model: {model_path}")
    
    # Test mode
    print("\n" + "="*70)
    print("TEST MODE")
    print("="*70)
    
    print("\n1. Test single image (with preview)")
    print("2. Test folder of images (batch)")
    print("3. Test on dataset/test/ folder")
    
    choice = input("\nChọn mode (1/2/3): ").strip()
    
    # Confidence threshold
    conf_input = input("Confidence threshold (0-1) [0.5]: ").strip()
    conf = float(conf_input) if conf_input else 0.5
    
    if choice == '1':
        # Single image
        image_path = input("\nĐường dẫn ảnh: ").strip()
        if not image_path:
            print("❌ No image provided")
            sys.exit(1)
        
        test_single_image(model_path, image_path, conf)
    
    elif choice == '2':
        # Folder
        folder_path = input("\nĐường dẫn folder: ").strip()
        if not folder_path:
            print("❌ No folder provided")
            sys.exit(1)
        
        output_folder = input("Output folder [test_results]: ").strip() or 'test_results'
        
        test_model_on_images(model_path, folder_path, output_folder, conf)
    
    elif choice == '3':
        # Test dataset
        if os.path.exists('dataset/images/test'):
            test_model_on_images(model_path, 'dataset/images/test', 'test_results', conf)
        else:
            print("\n❌ dataset/images/test not found!")
    
    else:
        print("❌ Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Bye!")
        cv2.destroyAllWindows()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        cv2.destroyAllWindows()
        sys.exit(1)
