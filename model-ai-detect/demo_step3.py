"""
DEMO BƯỚC 3: UI Đơn giản hóa (Không cần model)
Demo giao diện UI để test layout và flow mà không cần model thật
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import random


class DemoBallotUI(ctk.CTk):
    """Demo UI đơn giản với dữ liệu giả"""
    
    def __init__(self):
        super().__init__()
        
        self.title("DEMO - Hệ thống Kiểm duyệt Phiếu bầu")
        self.geometry("1400x850")
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Biến demo
        self.ballot_count = 0
        self.valid_count = 0
        self.invalid_count = 0
        self.candidate_votes = {
            "Nguyễn Văn A": 0,
            "Trần Thị B": 0,
            "Lê Văn C": 0,
            "Phạm Thị D": 0,
            "Hoàng Văn E": 0
        }
        
        self.create_ui()
        
    def create_ui(self):
        """Tạo UI"""
        
        # Grid config
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Left panel
        self.create_left_panel()
        
        # Right panel
        self.create_right_panel()
        
        # Status bar
        self.create_status_bar()
        
    def create_left_panel(self):
        """Panel trái"""
        
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="📹 CAMERA PREVIEW (DEMO)",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=10)
        
        # Placeholder image
        self.preview_label = ctk.CTkLabel(
            frame,
            text="[Video Preview]\n\nClick 'Tạo Phiếu Demo' để mô phỏng",
            font=("Arial", 16),
            fg_color="gray20",
            corner_radius=10
        )
        self.preview_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=2, column=0, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🎥 Demo Camera",
            command=self.demo_camera,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="green"
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📸 Tạo Phiếu Demo",
            command=self.simulate_ballot,
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📊 Xem UI",
            command=self.show_ui_info,
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        ).grid(row=0, column=2, padx=5)
        
    def create_right_panel(self):
        """Panel phải"""
        
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        ctk.CTkLabel(
            frame,
            text="📊 PANEL ĐIỀU KHIỂN",
            font=("Arial", 20, "bold")
        ).pack(pady=15)
        
        # Stats
        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📈 THỐNG KÊ",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        self.lbl_total = ctk.CTkLabel(
            stats_frame,
            text="Tổng số phiếu: 0",
            font=("Arial", 14)
        )
        self.lbl_total.pack(pady=2)
        
        self.lbl_valid = ctk.CTkLabel(
            stats_frame,
            text="Phiếu hợp lệ: 0",
            font=("Arial", 14),
            text_color="green"
        )
        self.lbl_valid.pack(pady=2)
        
        self.lbl_invalid = ctk.CTkLabel(
            stats_frame,
            text="Phiếu không hợp lệ: 0",
            font=("Arial", 14),
            text_color="red"
        )
        self.lbl_invalid.pack(pady=2)
        
        # Separator
        ctk.CTkFrame(frame, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)
        
        # Candidates
        candidate_frame = ctk.CTkFrame(frame)
        candidate_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            candidate_frame,
            text="👥 KẾT QUẢ ỨNG VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        self.candidate_list = ctk.CTkScrollableFrame(
            candidate_frame,
            height=250
        )
        self.candidate_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.candidate_labels = {}
        for name in self.candidate_votes.keys():
            lbl = ctk.CTkLabel(
                self.candidate_list,
                text=f"○ {name}: 0 phiếu (0.0%)",
                font=("Arial", 13),
                anchor="w"
            )
            lbl.pack(fill="x", pady=2, padx=5)
            self.candidate_labels[name] = lbl
        
        # Separator
        ctk.CTkFrame(frame, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="💾 Xuất Excel",
            command=self.demo_export,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="blue"
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔄 Reset Demo",
            command=self.reset_demo,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="orange"
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="⚙️ Cài đặt",
            command=self.demo_settings,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
    def create_status_bar(self):
        """Status bar"""
        
        status_frame = ctk.CTkFrame(self, height=40)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="🟢 DEMO MODE - Không cần model thật",
            font=("Arial", 12)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            status_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Arial", 12)
        )
        self.time_label.pack(side="right", padx=10)
        
        self.update_time()
        
    def demo_camera(self):
        """Demo camera"""
        messagebox.showinfo(
            "Demo Camera",
            "Trong ứng dụng thật:\n\n"
            "1. Camera sẽ hiển thị real-time\n"
            "2. Có 5 vùng ROI được vẽ\n"
            "3. FPS ~15-20\n"
            "4. Click 'Chụp' để analyze"
        )
        self.status_label.configure(text="📹 Demo: Camera đang chạy...")
        
    def simulate_ballot(self):
        """Tạo phiếu demo"""
        
        self.ballot_count += 1
        
        # Random tạo phiếu hợp lệ hoặc không
        is_valid = random.choice([True, True, True, False])  # 75% hợp lệ
        
        if is_valid:
            self.valid_count += 1
            # Random chọn loại phiếu
            ballot_type = random.choice(["Bầu 1 người", "Bầu 2 người", "Bầu 3 người"])
            
            if ballot_type == "Bầu 1 người":
                num_voted = 1
            elif ballot_type == "Bầu 2 người":
                num_voted = 2
            else:
                num_voted = 3
            
            # Random chọn người được bầu
            all_candidates = list(self.candidate_votes.keys())
            voted_candidates = random.sample(all_candidates, num_voted)
            
            for name in voted_candidates:
                self.candidate_votes[name] += 1
            
            result_text = f"✅ Phiếu #{self.ballot_count}: {ballot_type}\n\n"
            result_text += "Người được bầu:\n" + "\n".join([f"✓ {name}" for name in voted_candidates])
            
        else:
            self.invalid_count += 1
            result_text = f"❌ Phiếu #{self.ballot_count}: KHÔNG HỢP LỆ\n\n"
            result_text += "Lý do: Số gạch không hợp lệ"
        
        # Update UI
        self.update_stats()
        
        # Show result
        messagebox.showinfo(f"Phiếu #{self.ballot_count}", result_text)
        
        self.status_label.configure(text=f"✅ Đã xử lý: Phiếu #{self.ballot_count}")
        
    def update_stats(self):
        """Cập nhật thống kê"""
        
        # Update totals
        self.lbl_total.configure(text=f"Tổng số phiếu: {self.ballot_count}")
        
        valid_pct = (self.valid_count / self.ballot_count * 100) if self.ballot_count > 0 else 0
        self.lbl_valid.configure(text=f"Phiếu hợp lệ: {self.valid_count} ({valid_pct:.1f}%)")
        
        self.lbl_invalid.configure(text=f"Phiếu không hợp lệ: {self.invalid_count}")
        
        # Update candidates
        for name, votes in self.candidate_votes.items():
            pct = (votes / self.valid_count * 100) if self.valid_count > 0 else 0
            icon = "✓" if votes > 0 else "○"
            self.candidate_labels[name].configure(
                text=f"{icon} {name}: {votes} phiếu ({pct:.1f}%)"
            )
        
    def demo_export(self):
        """Demo export"""
        
        if self.ballot_count == 0:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
            return
        
        messagebox.showinfo(
            "Demo Export",
            f"Trong ứng dụng thật, file Excel sẽ được tạo với:\n\n"
            f"📊 Sheet 1: Chi tiết {self.ballot_count} phiếu\n"
            f"📈 Sheet 2: Thống kê tổng hợp\n"
            f"👥 Sheet 3: Kết quả 5 ứng viên\n\n"
            f"File sẽ được lưu tại vị trí bạn chọn."
        )
        
        self.status_label.configure(text="💾 Demo: Đã xuất Excel")
        
    def reset_demo(self):
        """Reset demo"""
        
        result = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn reset tất cả dữ liệu demo?"
        )
        
        if result:
            self.ballot_count = 0
            self.valid_count = 0
            self.invalid_count = 0
            for name in self.candidate_votes:
                self.candidate_votes[name] = 0
            
            self.update_stats()
            self.status_label.configure(text="🔄 Đã reset demo")
            messagebox.showinfo("Thành công", "Đã reset dữ liệu demo!")
        
    def demo_settings(self):
        """Demo settings"""
        
        settings = ctk.CTkToplevel(self)
        settings.title("Cài đặt (Demo)")
        settings.geometry("500x400")
        
        ctk.CTkLabel(
            settings,
            text="⚙️ CÀI ĐẶT",
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            settings,
            text="ROI Layout:",
            font=("Arial", 14)
        ).pack(pady=5)
        
        layout = ctk.CTkOptionMenu(
            settings,
            values=["HORIZONTAL", "VERTICAL"],
            width=200
        )
        layout.set("HORIZONTAL")
        layout.pack(pady=5)
        
        ctk.CTkLabel(
            settings,
            text="Confidence Threshold:",
            font=("Arial", 14)
        ).pack(pady=5)
        
        slider = ctk.CTkSlider(
            settings,
            from_=0.1,
            to=0.9,
            width=300
        )
        slider.set(0.5)
        slider.pack(pady=5)
        
        ctk.CTkLabel(
            settings,
            text="0.50",
            font=("Arial", 12)
        ).pack()
        
        ctk.CTkButton(
            settings,
            text="Áp dụng",
            command=lambda: [messagebox.showinfo("Demo", "Đã áp dụng cài đặt!"), settings.destroy()],
            width=150,
            height=35
        ).pack(pady=20)
        
    def show_ui_info(self):
        """Hiển thị info về UI"""
        
        info = """
🎨 GIAO DIỆN UI - TÍNH NĂNG

Bên trái (Camera):
  📹 Camera Preview với ROI overlay
  🎥 Nút Bật/Tắt Camera
  📸 Nút Chụp & Phân tích
  📂 Nút Mở ảnh từ file

Bên phải (Control):
  📈 Thống kê realtime
  👥 Kết quả từng ứng viên
  💾 Xuất Excel
  🔄 Reset dữ liệu
  ⚙️ Cài đặt (ROI, Confidence)

Phía dưới:
  Status bar với thời gian realtime

Trong ứng dụng thật:
  ✓ Tích hợp BƯỚC 1 + BƯỚC 2
  ✓ AI detection thật
  ✓ Export Excel đầy đủ
  ✓ Thread-based processing
        """
        
        messagebox.showinfo("UI Info", info)
        
    def update_time(self):
        """Update time"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)


def main():
    """Run demo"""
    
    print("\n" + "="*70)
    print("DEMO UI - BƯỚC 3")
    print("="*70)
    print("\nĐây là demo giao diện không cần model thật.")
    print("Bạn có thể:")
    print("  1. Xem layout UI")
    print("  2. Test các chức năng")
    print("  3. Tạo phiếu demo để xem flow")
    print("\nĐể chạy ứng dụng thật với AI:")
    print("  python step3_ui_app.py")
    print("="*70 + "\n")
    
    app = DemoBallotUI()
    app.mainloop()


if __name__ == "__main__":
    main()
