"""
BƯỚC 3: Giao diện UI với CustomTkinter
Chức năng:
- Camera preview real-time
- Nút điều khiển Start/Stop/Capture
- Hiển thị thống kê trực quan
- Xuất Excel từ UI
- Tích hợp đầy đủ BƯỚC 1 + BƯỚC 2
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
from datetime import datetime
from typing import Optional
import os

# Import logic từ BƯỚC 1 & 2
from step1_roi_detection import BallotROIDetector
from step2_ballot_classifier import BallotClassifier, BallotDataCollector, ExcelExporter
import config


class BallotUIApp(ctk.CTk):
    """Ứng dụng UI chính cho hệ thống kiểm duyệt phiếu bầu"""
    
    def __init__(self):
        super().__init__()
        
        # Cấu hình window
        self.title("Hệ thống Kiểm duyệt Phiếu bầu - AI Detection")
        self.geometry("1400x850")
        
        # Biến trạng thái
        self.camera_running = False
        self.camera_thread = None
        self.cap = None
        self.current_frame = None
        self.selected_camera_id = 0  # Camera device ID
        
        # Khởi tạo components
        self.detector = None
        self.classifier = BallotClassifier()
        self.collector = BallotDataCollector()
        self.exporter = ExcelExporter()
        
        # Setup UI theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Tạo UI
        self.create_ui()
        
        # Try load model
        self.load_ai_model()
        
    def create_ui(self):
        """Tạo giao diện chính"""
        
        # Main container
        self.grid_columnconfigure(0, weight=3)  # Left - Camera
        self.grid_columnconfigure(1, weight=2)  # Right - Control Panel
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # ==================== LEFT SIDE: CAMERA PREVIEW ====================
        self.create_camera_panel()
        
        # ==================== RIGHT SIDE: CONTROL PANEL ====================
        self.create_control_panel()
        
        # ==================== BOTTOM: STATUS BAR ====================
        self.create_status_bar()
        
    def create_camera_panel(self):
        """Tạo panel hiển thị camera"""
        
        # Frame chính
        camera_frame = ctk.CTkFrame(self, corner_radius=10)
        camera_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        camera_frame.grid_rowconfigure(1, weight=1)
        camera_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            camera_frame, 
            text="📹 CAMERA PREVIEW",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=10)
        
        # Video display
        self.video_label = ctk.CTkLabel(camera_frame, text="")
        self.video_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Camera controls
        controls = ctk.CTkFrame(camera_frame)
        controls.grid(row=2, column=0, pady=10)
        
        # Row 0: Camera selector
        ctk.CTkLabel(
            controls,
            text="Camera:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.camera_selector = ctk.CTkOptionMenu(
            controls,
            values=["Camera 0 (Default)", "Camera 1", "Camera 2", "Camera 3"],
            command=self.on_camera_change,
            width=150
        )
        self.camera_selector.grid(row=0, column=1, padx=5, pady=5)
        self.camera_selector.set("Camera 0 (Default)")
        
        # Row 1: Main buttons
        self.btn_start_camera = ctk.CTkButton(
            controls,
            text="🎥 Bật Camera",
            command=self.toggle_camera,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_start_camera.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_capture = ctk.CTkButton(
            controls,
            text="📸 Chụp & Phân tích",
            command=self.capture_and_analyze,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            state="disabled"
        )
        self.btn_capture.grid(row=1, column=1, padx=5, pady=5)
        
        # Row 2: File buttons
        self.btn_load_image = ctk.CTkButton(
            controls,
            text="📂 Mở 1 ảnh",
            command=self.load_image_file,
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.btn_load_image.grid(row=2, column=0, padx=5, pady=5)
        
        self.btn_batch_import = ctk.CTkButton(
            controls,
            text="📁 Import Folder",
            command=self.batch_import_folder,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="orange",
            hover_color="darkorange"
        )
        self.btn_batch_import.grid(row=2, column=1, padx=5, pady=5)
        
    def create_control_panel(self):
        """Tạo panel điều khiển bên phải"""
        
        # Main frame
        control_frame = ctk.CTkFrame(self, corner_radius=10)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(
            control_frame,
            text="📊 PANEL ĐIỀU KHIỂN",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)
        
        # ========== THỐNG KÊ ==========
        stats_frame = ctk.CTkFrame(control_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📈 THỐNG KÊ",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        # Tổng số phiếu
        self.lbl_total = ctk.CTkLabel(
            stats_frame,
            text="Tổng số phiếu: 0",
            font=("Arial", 14)
        )
        self.lbl_total.pack(pady=2)
        
        # Phiếu hợp lệ
        self.lbl_valid = ctk.CTkLabel(
            stats_frame,
            text="Phiếu hợp lệ: 0",
            font=("Arial", 14),
            text_color="green"
        )
        self.lbl_valid.pack(pady=2)
        
        # Phiếu không hợp lệ
        self.lbl_invalid = ctk.CTkLabel(
            stats_frame,
            text="Phiếu không hợp lệ: 0",
            font=("Arial", 14),
            text_color="red"
        )
        self.lbl_invalid.pack(pady=2)
        
        # Separator
        ctk.CTkFrame(control_frame, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)
        
        # ========== KẾT QUẢ ỨNG VIÊN ==========
        candidate_frame = ctk.CTkFrame(control_frame)
        candidate_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            candidate_frame,
            text="👥 KẾT QUẢ ỨNG VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        # Scrollable frame cho danh sách ứng viên
        self.candidate_list = ctk.CTkScrollableFrame(
            candidate_frame,
            height=250
        )
        self.candidate_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Khởi tạo labels cho ứng viên
        self.candidate_labels = {}
        for name in config.CANDIDATE_NAMES:
            lbl = ctk.CTkLabel(
                self.candidate_list,
                text=f"{name}: 0 phiếu",
                font=("Arial", 13),
                anchor="w"
            )
            lbl.pack(fill="x", pady=2, padx=5)
            self.candidate_labels[name] = lbl
        
        # Separator
        ctk.CTkFrame(control_frame, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)
        
        # ========== CÁC NÚT CHỨC NĂNG ==========
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.btn_export = ctk.CTkButton(
            button_frame,
            text="💾 Xuất Excel",
            command=self.export_to_excel,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="blue",
            hover_color="darkblue"
        )
        self.btn_export.pack(pady=5)
        
        self.btn_reset = ctk.CTkButton(
            button_frame,
            text="🔄 Reset Dữ liệu",
            command=self.reset_data,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="orange",
            hover_color="darkorange"
        )
        self.btn_reset.pack(pady=5)
        
        self.btn_settings = ctk.CTkButton(
            button_frame,
            text="⚙️ Cài đặt",
            command=self.open_settings,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.btn_settings.pack(pady=5)
        
    def create_status_bar(self):
        """Tạo thanh trạng thái"""
        
        status_frame = ctk.CTkFrame(self, height=40)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="🟢 Sẵn sàng - Chờ tải model...",
            font=("Arial", 12)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            status_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Arial", 12)
        )
        self.time_label.pack(side="right", padx=10)
        
        # Update time
        self.update_time()
        
    # ==================== AI MODEL FUNCTIONS ====================
    
    def load_ai_model(self):
        """Load AI model"""
        
        self.update_status("⏳ Đang tải AI model...")
        
        try:
            self.detector = BallotROIDetector()
            if self.detector.load_model():
                self.update_status("✅ Model đã sẵn sàng!")
                messagebox.showinfo("Thành công", "AI Model đã được tải!")
            else:
                self.update_status("❌ Lỗi: Không thể tải model!")
                messagebox.showerror("Lỗi", f"Không thể tải model từ: {config.MODEL_PATH}")
        except Exception as e:
            self.update_status(f"❌ Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi khi tải model:\n{str(e)}")
    
    # ==================== CAMERA FUNCTIONS ====================
    
    def toggle_camera(self):
        """Bật/Tắt camera"""
        
        if not self.camera_running:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Bật camera"""
        
        if self.detector is None:
            messagebox.showerror("Lỗi", "Model chưa được tải!")
            return
        
        # Thử mở camera với device ID đã chọn
        self.update_status(f"⏳ Đang mở camera {self.selected_camera_id}...")
        self.cap = cv2.VideoCapture(self.selected_camera_id)
        
        if not self.cap.isOpened():
            # Thử auto-detect camera khác
            error_msg = f"Không thể mở Camera {self.selected_camera_id}!\n\n"
            error_msg += "Đang thử tìm camera khác...\n"
            
            found = False
            for cam_id in range(5):  # Thử camera 0-4
                if cam_id == self.selected_camera_id:
                    continue
                    
                self.update_status(f"⏳ Thử camera {cam_id}...")
                test_cap = cv2.VideoCapture(cam_id)
                
                if test_cap.isOpened():
                    # Tìm thấy camera
                    ret, _ = test_cap.read()
                    if ret:
                        error_msg += f"✅ Tìm thấy Camera {cam_id}!\n\n"
                        error_msg += f"Bạn có muốn dùng Camera {cam_id} không?"
                        
                        if messagebox.askyesno("Camera khả dụng", error_msg):
                            self.cap = test_cap
                            self.selected_camera_id = cam_id
                            self.camera_selector.set(f"Camera {cam_id}")
                            found = True
                            break
                        else:
                            test_cap.release()
                else:
                    test_cap.release()
            
            if not found:
                messagebox.showerror(
                    "Lỗi Camera",
                    "Không tìm thấy camera nào!\n\n"
                    "Giải pháp:\n"
                    "1. Kiểm tra webcam đã cắm USB\n"
                    "2. Kiểm tra webcam đang dùng bởi app khác\n"
                    "3. Thử khởi động lại máy tính\n"
                    "4. Kiểm tra quyền truy cập camera\n\n"
                    "Hoặc dùng chức năng 'Mở ảnh' để import ảnh có sẵn."
                )
                self.update_status("❌ Không tìm thấy camera")
                return
        
        self.camera_running = True
        self.btn_start_camera.configure(
            text="⏸️ Tắt Camera",
            fg_color="red",
            hover_color="darkred"
        )
        self.btn_capture.configure(state="normal")
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.update_camera_feed, daemon=True)
        self.camera_thread.start()
        
        self.update_status("🎥 Camera đang hoạt động")
    
    def stop_camera(self):
        """Tắt camera"""
        
        self.camera_running = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.btn_start_camera.configure(
            text="🎥 Bật Camera",
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_capture.configure(state="disabled")
        
        # Clear video display
        self.video_label.configure(image=None, text="Camera đã tắt")
        
        self.update_status("⏸️ Camera đã dừng")
    
    def update_camera_feed(self):
        """Update camera feed (chạy trong thread)"""
        
        while self.camera_running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.current_frame = frame.copy()
                    
                    # Vẽ ROI zones lên frame
                    h, w = frame.shape[:2]
                    roi_zones = self.detector.calculate_roi_zones(h, w)
                    
                    for idx, (x1, y1, x2, y2) in enumerate(roi_zones):
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"{idx+1}"
                        cv2.putText(frame, label, (x1 + 10, y1 + 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Convert to PhotoImage
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    
                    # Resize to fit
                    display_width = 800
                    aspect_ratio = img.height / img.width
                    display_height = int(display_width * aspect_ratio)
                    img = img.resize((display_width, display_height), Image.Resampling.LANCZOS)
                    
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(display_width, display_height))
                    
                    # Update UI (thread-safe)
                    self.video_label.configure(image=photo, text="")
                    self.video_label.image = photo
    
    def capture_and_analyze(self):
        """Chụp ảnh từ camera và phân tích"""
        
        if self.current_frame is None:
            messagebox.showwarning("Cảnh báo", "Không có frame nào từ camera!")
            return
        
        self.update_status("⏳ Đang phân tích phiếu...")
        
        # Process trong thread để không block UI
        threading.Thread(target=self._process_frame, args=(self.current_frame,), daemon=True).start()
    
    def _process_frame(self, frame):
        """Xử lý frame (chạy trong thread)"""
        
        try:
            # BƯỚC 1: Detect
            crossed_status, annotated = self.detector.process_ballot(frame, visualize=True)
            
            # BƯỚC 2: Classify
            classification = self.classifier.classify_ballot(crossed_status)
            
            # Thêm vào collector
            ballot_count = len(self.collector.ballots) + 1
            ballot_id = f"PHIEU_{ballot_count:04d}"
            
            self.collector.add_ballot(
                crossed_status,
                ballot_id=ballot_id,
                metadata={
                    'source': 'camera',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
            # Update UI
            self.after(0, lambda: self._show_result(classification, annotated))
            self.after(0, self.update_statistics)
            
            status_msg = f"✅ Phiếu #{ballot_count}: {classification['status_message']}"
            self.after(0, lambda: self.update_status(status_msg))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi xử lý:\n{str(e)}"))
            self.after(0, lambda: self.update_status(f"❌ Lỗi: {str(e)}"))
    
    def _show_result(self, classification, annotated_frame):
        """Hiển thị kết quả phân tích"""
        
        # Tạo window mới để hiển thị
        result_window = ctk.CTkToplevel(self)
        result_window.title("Kết quả Phân tích")
        result_window.geometry("900x700")
        
        # Hiển thị ảnh
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = img.resize((800, 500), Image.Resampling.LANCZOS)
        photo = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 500))
        
        img_label = ctk.CTkLabel(result_window, image=photo, text="")
        img_label.pack(pady=10)
        img_label.image = photo
        
        # Hiển thị thông tin
        info_frame = ctk.CTkFrame(result_window)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        status_color = "green" if classification['is_valid'] else "red"
        
        ctk.CTkLabel(
            info_frame,
            text=classification['status_message'],
            font=("Arial", 18, "bold"),
            text_color=status_color
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Số người được bầu: {classification['num_voted']}/5",
            font=("Arial", 14)
        ).pack(pady=2)
        
        if classification['voted_for']:
            voted_text = "Người được bầu:\n" + "\n".join([f"✓ {name}" for name in classification['voted_for']])
            ctk.CTkLabel(
                info_frame,
                text=voted_text,
                font=("Arial", 13),
                text_color="green"
            ).pack(pady=5)
        
        # Nút đóng
        ctk.CTkButton(
            result_window,
            text="Đóng",
            command=result_window.destroy,
            width=150,
            height=35
        ).pack(pady=10)
    
    # ==================== FILE FUNCTIONS ====================
    
    def on_camera_change(self, choice: str):
        """Callback khi đổi camera"""
        # Extract camera ID from choice string
        cam_id = int(choice.split()[1])  # "Camera 0" -> 0
        self.selected_camera_id = cam_id
        self.update_status(f"📹 Đã chọn Camera {cam_id}")
        
        # Nếu camera đang chạy, restart với camera mới
        if self.camera_running:
            messagebox.showinfo(
                "Thông báo",
                f"Vui lòng tắt camera hiện tại và bật lại để dùng Camera {cam_id}"
            )
    
    def batch_import_folder(self):
        """Import nhiều ảnh từ folder"""
        
        if self.detector is None:
            messagebox.showerror("Lỗi", "Model chưa được tải!")
            return
        
        # Chọn folder
        folder_path = filedialog.askdirectory(title="Chọn folder chứa ảnh phiếu bầu")
        
        if not folder_path:
            return
        
        # Tìm tất cả file ảnh
        import glob
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.JPG', '*.JPEG', '*.PNG', '*.BMP']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(folder_path, ext)))
            image_files.extend(glob.glob(os.path.join(folder_path, '**', ext), recursive=True))
        
        # Remove duplicates
        image_files = list(set(image_files))
        
        if not image_files:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy file ảnh nào trong folder!")
            return
        
        # Confirm
        msg = f"Tìm thấy {len(image_files)} ảnh trong folder.\n\n"
        msg += f"Bạn có muốn xử lý tất cả {len(image_files)} ảnh không?\n\n"
        msg += "(Có thể mất vài phút)"
        
        if not messagebox.askyesno("Xác nhận Batch Import", msg):
            return
        
        # Create progress window
        self._batch_process_images(image_files)
    
    def _batch_process_images(self, image_files):
        """Xử lý batch images với progress window"""
        
        # Progress window
        progress_window = ctk.CTkToplevel(self)
        progress_window.title("Đang xử lý...")
        progress_window.geometry("500x200")
        progress_window.transient(self)
        progress_window.grab_set()
        
        ctk.CTkLabel(
            progress_window,
            text="Đang xử lý ảnh...",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        progress_label = ctk.CTkLabel(
            progress_window,
            text="0/0",
            font=("Arial", 14)
        )
        progress_label.pack(pady=10)
        
        progress_bar = ctk.CTkProgressBar(progress_window, width=400)
        progress_bar.pack(pady=10)
        progress_bar.set(0)
        
        status_label = ctk.CTkLabel(
            progress_window,
            text="",
            font=("Arial", 12)
        )
        status_label.pack(pady=10)
        
        # Process in thread
        def process():
            total = len(image_files)
            success_count = 0
            error_count = 0
            
            for idx, img_path in enumerate(image_files):
                try:
                    # Read image
                    frame = cv2.imread(img_path)
                    if frame is None:
                        error_count += 1
                        continue
                    
                    # Process
                    crossed_status, _ = self.detector.process_ballot(frame, visualize=False)
                    classification = self.classifier.classify_ballot(crossed_status)
                    
                    # Add to collector
                    ballot_count = len(self.collector.ballots) + 1
                    ballot_id = f"PHIEU_{ballot_count:04d}"
                    
                    self.collector.add_ballot(
                        crossed_status,
                        ballot_id=ballot_id,
                        metadata={
                            'source': 'batch_import',
                            'file': os.path.basename(img_path),
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    print(f"Error processing {img_path}: {e}")
                
                # Update progress
                progress = (idx + 1) / total
                progress_bar.set(progress)
                progress_label.configure(text=f"{idx+1}/{total} ảnh")
                status_label.configure(text=f"✅ {success_count} thành công | ❌ {error_count} lỗi")
            
            # Done
            progress_window.after(500, progress_window.destroy)
            
            # Show result
            result_msg = f"Hoàn tất xử lý {total} ảnh!\n\n"
            result_msg += f"✅ Thành công: {success_count}\n"
            result_msg += f"❌ Lỗi: {error_count}\n\n"
            result_msg += "Thống kê đã được cập nhật."
            
            self.after(0, lambda: messagebox.showinfo("Hoàn tất", result_msg))
            self.after(0, self.update_statistics)
            self.after(0, lambda: self.update_status(f"✅ Batch import: {success_count}/{total} ảnh"))
        
        threading.Thread(target=process, daemon=True).start()
    
    def load_image_file(self):
        """Mở file ảnh và phân tích"""
        
        if self.detector is None:
            messagebox.showerror("Lỗi", "Model chưa được tải!")
            return
        
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh phiếu bầu",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        self.update_status(f"⏳ Đang xử lý: {os.path.basename(file_path)}")
        
        # Load và process
        frame = cv2.imread(file_path)
        if frame is None:
            messagebox.showerror("Lỗi", "Không thể đọc file ảnh!")
            return
        
        # Process
        threading.Thread(target=self._process_frame, args=(frame,), daemon=True).start()
    
    # ==================== DATA FUNCTIONS ====================
    
    def update_statistics(self):
        """Cập nhật thống kê lên UI"""
        
        stats = self.collector.get_statistics()
        
        # Update labels
        self.lbl_total.configure(text=f"Tổng số phiếu: {stats['total']}")
        self.lbl_valid.configure(text=f"Phiếu hợp lệ: {stats['valid']} ({stats['valid_percentage']:.1f}%)")
        self.lbl_invalid.configure(text=f"Phiếu không hợp lệ: {stats['invalid']}")
        
        # Update candidate scores
        for name, votes in stats['candidate_votes'].items():
            if name in self.candidate_labels:
                percentage = (votes / stats['valid'] * 100) if stats['valid'] > 0 else 0
                self.candidate_labels[name].configure(
                    text=f"{'✓' if votes > 0 else '○'} {name}: {votes} phiếu ({percentage:.1f}%)"
                )
    
    def export_to_excel(self):
        """Xuất dữ liệu ra Excel"""
        
        if len(self.collector.ballots) == 0:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
            return
        
        # Chọn nơi lưu
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"ballot_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if not file_path:
            return
        
        self.update_status("⏳ Đang xuất Excel...")
        
        try:
            output_file = self.exporter.export_to_excel(
                self.collector.get_ballots(),
                output_path=file_path,
                include_statistics=True
            )
            
            self.update_status(f"✅ Đã xuất: {os.path.basename(output_file)}")
            messagebox.showinfo("Thành công", f"Đã xuất file:\n{output_file}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất Excel:\n{str(e)}")
            self.update_status(f"❌ Lỗi xuất Excel")
    
    def reset_data(self):
        """Reset tất cả dữ liệu"""
        
        result = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa tất cả dữ liệu?\nHành động này không thể hoàn tác!"
        )
        
        if result:
            self.collector.clear()
            self.update_statistics()
            self.update_status("🔄 Đã reset dữ liệu")
            messagebox.showinfo("Thành công", "Đã xóa tất cả dữ liệu!")
    
    def open_settings(self):
        """Mở cửa sổ cài đặt"""
        
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Cài đặt")
        settings_window.geometry("500x400")
        
        ctk.CTkLabel(
            settings_window,
            text="⚙️ CÀI ĐẶT",
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        # ROI Layout
        ctk.CTkLabel(
            settings_window,
            text="ROI Layout:",
            font=("Arial", 14)
        ).pack(pady=5)
        
        layout_var = ctk.StringVar(value=config.ROI_LAYOUT)
        ctk.CTkOptionMenu(
            settings_window,
            values=["HORIZONTAL", "VERTICAL"],
            variable=layout_var,
            width=200
        ).pack(pady=5)
        
        # Confidence threshold
        ctk.CTkLabel(
            settings_window,
            text="Confidence Threshold:",
            font=("Arial", 14)
        ).pack(pady=5)
        
        conf_var = ctk.DoubleVar(value=config.CONFIDENCE_THRESHOLD)
        ctk.CTkSlider(
            settings_window,
            from_=0.1,
            to=0.9,
            variable=conf_var,
            width=300
        ).pack(pady=5)
        
        conf_label = ctk.CTkLabel(
            settings_window,
            text=f"{config.CONFIDENCE_THRESHOLD:.2f}",
            font=("Arial", 12)
        )
        conf_label.pack()
        
        def update_conf_label(value):
            conf_label.configure(text=f"{float(value):.2f}")
        
        conf_var.trace_add("write", lambda *args: update_conf_label(conf_var.get()))
        
        # Nút Apply
        def apply_settings():
            config.ROI_LAYOUT = layout_var.get()
            config.CONFIDENCE_THRESHOLD = conf_var.get()
            if self.detector:
                self.detector.roi_layout = config.ROI_LAYOUT
                self.detector.confidence = config.CONFIDENCE_THRESHOLD
            messagebox.showinfo("Thành công", "Đã áp dụng cài đặt!")
            settings_window.destroy()
        
        ctk.CTkButton(
            settings_window,
            text="Áp dụng",
            command=apply_settings,
            width=150,
            height=35
        ).pack(pady=20)
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def update_status(self, message: str):
        """Cập nhật status bar"""
        self.status_label.configure(text=message)
    
    def update_time(self):
        """Cập nhật thời gian"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)
    
    def on_closing(self):
        """Xử lý khi đóng app"""
        
        if len(self.collector.ballots) > 0:
            result = messagebox.askyesnocancel(
                "Xác nhận",
                "Có dữ liệu chưa được lưu. Bạn có muốn xuất Excel trước khi thoát?"
            )
            
            if result is None:  # Cancel
                return
            elif result:  # Yes - Export
                self.export_to_excel()
        
        # Stop camera
        if self.camera_running:
            self.stop_camera()
        
        # Destroy
        self.destroy()


def main():
    """Chạy ứng dụng"""
    
    app = BallotUIApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
