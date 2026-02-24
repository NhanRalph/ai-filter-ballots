"""
BƯỚC 2: Logic Phân loại Phiếu & Export Excel
Chức năng:
- Nhận mảng kết quả từ BƯỚC 1 ([1,0,0,1,1])
- Đối chiếu với Quy tắc đếm (Bầu 1, 2, 3 người)
- Phân loại phiếu hợp lệ/không hợp lệ
- Lưu dữ liệu vào pandas DataFrame
- Xuất ra file Excel (.xlsx)
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
import config
from pathlib import Path


class BallotClassifier:
    """Class phân loại phiếu bầu dựa trên quy tắc"""
    
    def __init__(self):
        """Khởi tạo classifier với quy tắc từ config"""
        self.valid_rules = config.VALID_BALLOT_RULES
        self.candidate_names = config.CANDIDATE_NAMES
        
    def classify_ballot(self, crossed_status: List[int]) -> Dict:
        """
        Phân loại 1 phiếu bầu
        
        Args:
            crossed_status: List[int] - [1,0,0,1,1] (1=bị gạch, 0=không gạch)
            
        Returns:
            Dict chứa thông tin phân loại:
            {
                'is_valid': bool,
                'ballot_type': str,
                'num_crossed': int,
                'num_voted': int,
                'voted_for': List[str],  # Tên người được bầu
                'crossed_for': List[str],  # Tên người bị gạch
                'status_message': str
            }
        """
        # Đếm số người bị gạch
        num_crossed = sum(crossed_status)
        num_voted = 5 - num_crossed
        
        # Kiểm tra hợp lệ
        is_valid = num_crossed in self.valid_rules
        ballot_type = self.valid_rules.get(num_crossed, "Không xác định")
        
        # Xác định người được bầu và bị gạch
        voted_for = []
        crossed_for = []
        
        for idx, status in enumerate(crossed_status):
            name = self.candidate_names[idx]
            if status == 0:  # Không bị gạch = Được bầu
                voted_for.append(name)
            else:  # Bị gạch
                crossed_for.append(name)
        
        # Tạo status message
        if is_valid:
            status_message = f"✅ Hợp lệ - {ballot_type}"
        else:
            status_message = f"❌ Không hợp lệ - Số gạch: {num_crossed}"
        
        return {
            'is_valid': is_valid,
            'ballot_type': ballot_type,
            'num_crossed': num_crossed,
            'num_voted': num_voted,
            'voted_for': voted_for,
            'crossed_for': crossed_for,
            'status_message': status_message,
            'crossed_status': crossed_status  # Lưu lại mảng gốc
        }
    
    def get_vote_array(self, crossed_status: List[int]) -> List[int]:
        """
        Chuyển đổi crossed_status thành vote_array
        
        Args:
            crossed_status: [1,0,0,1,1] (1=gạch, 0=không gạch)
            
        Returns:
            vote_array: [0,1,1,0,0] (1=được bầu, 0=không được bầu)
        """
        return [0 if x == 1 else 1 for x in crossed_status]
    
    def print_result(self, classification: Dict, ballot_number: int = None):
        """
        In kết quả phân loại ra console
        
        Args:
            classification: Dict kết quả từ classify_ballot()
            ballot_number: Số thứ tự phiếu (tùy chọn)
        """
        print("\n" + "="*60)
        if ballot_number:
            print(f"PHIẾU SỐ {ballot_number}")
            print("="*60)
        
        print(f"Trạng thái: {classification['status_message']}")
        print(f"Số người bị gạch: {classification['num_crossed']}/5")
        print(f"Số người được bầu: {classification['num_voted']}/5")
        
        print(f"\nNgười ĐƯỢC BẦU:")
        if classification['voted_for']:
            for name in classification['voted_for']:
                print(f"  ✓ {name}")
        else:
            print("  (Không có)")
        
        print(f"\nNgười BỊ GẠCH:")
        if classification['crossed_for']:
            for name in classification['crossed_for']:
                print(f"  ✗ {name}")
        else:
            print("  (Không có)")


class BallotDataCollector:
    """Class thu thập và quản lý dữ liệu nhiều phiếu bầu"""
    
    def __init__(self):
        """Khởi tạo collector"""
        self.ballots = []  # Danh sách các phiếu đã thu thập
        self.classifier = BallotClassifier()
        
    def add_ballot(self, crossed_status: List[int], 
                   ballot_id: str = None,
                   metadata: Dict = None):
        """
        Thêm 1 phiếu bầu vào bộ sưu tập
        
        Args:
            crossed_status: List[int] - Kết quả từ BƯỚC 1
            ballot_id: ID/Tên phiếu (tùy chọn)
            metadata: Dict thông tin bổ sung (timestamp, image_path, etc.)
        """
        # Phân loại phiếu
        classification = self.classifier.classify_ballot(crossed_status)
        
        # Tạo ID tự động nếu không có
        if ballot_id is None:
            ballot_id = f"Phiếu_{len(self.ballots) + 1:04d}"
        
        # Thêm metadata
        ballot_data = {
            'ballot_id': ballot_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **classification
        }
        
        # Thêm metadata bổ sung nếu có
        if metadata:
            ballot_data['metadata'] = metadata
        
        self.ballots.append(ballot_data)
        
        return len(self.ballots)  # Trả về số thứ tự phiếu
    
    def get_ballots(self) -> List[Dict]:
        """Lấy danh sách tất cả phiếu"""
        return self.ballots
    
    def get_statistics(self) -> Dict:
        """
        Tính toán thống kê tổng hợp
        
        Returns:
            Dict chứa thống kê
        """
        if not self.ballots:
            return {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'vote_1': 0,
                'vote_2': 0,
                'vote_3': 0,
                'candidate_votes': {}
            }
        
        total = len(self.ballots)
        valid = sum(1 for b in self.ballots if b['is_valid'])
        invalid = total - valid
        
        # Đếm theo loại phiếu
        vote_1 = sum(1 for b in self.ballots if b['ballot_type'] == "Bầu 1 người")
        vote_2 = sum(1 for b in self.ballots if b['ballot_type'] == "Bầu 2 người")
        vote_3 = sum(1 for b in self.ballots if b['ballot_type'] == "Bầu 3 người")
        
        # Đếm số phiếu cho từng ứng viên
        candidate_votes = {name: 0 for name in config.CANDIDATE_NAMES}
        for ballot in self.ballots:
            if ballot['is_valid']:  # Chỉ đếm phiếu hợp lệ
                for name in ballot['voted_for']:
                    candidate_votes[name] += 1
        
        return {
            'total': total,
            'valid': valid,
            'invalid': invalid,
            'valid_percentage': (valid / total * 100) if total > 0 else 0,
            'vote_1': vote_1,
            'vote_2': vote_2,
            'vote_3': vote_3,
            'candidate_votes': candidate_votes
        }
    
    def print_statistics(self):
        """In thống kê ra console"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("THỐNG KÊ TỔNG HỢP")
        print("="*60)
        print(f"Tổng số phiếu: {stats['total']}")
        print(f"Phiếu hợp lệ: {stats['valid']} ({stats['valid_percentage']:.1f}%)")
        print(f"Phiếu không hợp lệ: {stats['invalid']}")
        
        print(f"\nPhân loại phiếu hợp lệ:")
        print(f"  - Bầu 1 người: {stats['vote_1']} phiếu")
        print(f"  - Bầu 2 người: {stats['vote_2']} phiếu")
        print(f"  - Bầu 3 người: {stats['vote_3']} phiếu")
        
        print(f"\nKết quả bầu cử (chỉ tính phiếu hợp lệ):")
        # Sắp xếp theo số phiếu giảm dần
        sorted_candidates = sorted(
            stats['candidate_votes'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for idx, (name, votes) in enumerate(sorted_candidates, 1):
            print(f"  {idx}. {name}: {votes} phiếu")
        
        print("="*60)
    
    def clear(self):
        """Xóa tất cả dữ liệu"""
        self.ballots.clear()


class ExcelExporter:
    """Class xuất dữ liệu ra file Excel"""
    
    def __init__(self):
        """Khởi tạo exporter"""
        self.candidate_names = config.CANDIDATE_NAMES
        
    def export_to_excel(self, ballots: List[Dict], 
                       output_path: str = None,
                       include_statistics: bool = True) -> str:
        """
        Xuất danh sách phiếu bầu ra Excel
        
        Args:
            ballots: List các phiếu từ BallotDataCollector
            output_path: Đường dẫn file output (tùy chọn)
            include_statistics: True nếu muốn thêm sheet thống kê
            
        Returns:
            Đường dẫn file đã xuất
        """
        if not ballots:
            print("Không có dữ liệu để xuất!")
            return None
        
        # Tạo tên file tự động nếu không có
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/ballot_results_{timestamp}.xlsx"
        
        # Tạo thư mục output nếu chưa có
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Tạo DataFrame chính
        df_main = self._create_main_dataframe(ballots)
        
        # Xuất ra Excel với multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Dữ liệu chi tiết từng phiếu
            df_main.to_excel(writer, sheet_name='Chi tiết phiếu', index=False)
            
            # Sheet 2: Thống kê (nếu yêu cầu)
            if include_statistics:
                df_stats = self._create_statistics_dataframe(ballots)
                df_stats.to_excel(writer, sheet_name='Thống kê', index=False)
            
            # Sheet 3: Tổng hợp theo ứng viên
            df_candidates = self._create_candidates_dataframe(ballots)
            df_candidates.to_excel(writer, sheet_name='Kết quả ứng viên', index=False)
        
        print(f"\n✅ Đã xuất file Excel: {output_path}")
        return output_path
    
    def _create_main_dataframe(self, ballots: List[Dict]) -> pd.DataFrame:
        """
        Tạo DataFrame chính với chi tiết từng phiếu
        
        Format:
        | STT | ID Phiếu | Thời gian | Tên 1 | Tên 2 | Tên 3 | Tên 4 | Tên 5 | Trạng thái | Loại phiếu |
        """
        rows = []
        
        for idx, ballot in enumerate(ballots, 1):
            row = {
                'STT': idx,
                'ID Phiếu': ballot['ballot_id'],
                'Thời gian': ballot['timestamp']
            }
            
            # Thêm cột cho từng ứng viên (X = được bầu, rỗng = bị gạch)
            crossed_status = ballot['crossed_status']
            for i, name in enumerate(self.candidate_names):
                if crossed_status[i] == 0:  # Không bị gạch = Được bầu
                    row[name] = 'X'
                else:  # Bị gạch
                    row[name] = ''
            
            # Thêm trạng thái
            row['Trạng thái'] = 'Hợp lệ' if ballot['is_valid'] else 'Không hợp lệ'
            row['Loại phiếu'] = ballot['ballot_type']
            row['Số gạch'] = ballot['num_crossed']
            row['Số bầu'] = ballot['num_voted']
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def _create_statistics_dataframe(self, ballots: List[Dict]) -> pd.DataFrame:
        """Tạo DataFrame thống kê tổng hợp"""
        collector = BallotDataCollector()
        collector.ballots = ballots
        stats = collector.get_statistics()
        
        rows = [
            {'Chỉ số': 'Tổng số phiếu', 'Giá trị': stats['total']},
            {'Chỉ số': 'Phiếu hợp lệ', 'Giá trị': stats['valid']},
            {'Chỉ số': 'Phiếu không hợp lệ', 'Giá trị': stats['invalid']},
            {'Chỉ số': 'Tỷ lệ hợp lệ (%)', 'Giá trị': f"{stats['valid_percentage']:.2f}"},
            {'Chỉ số': '', 'Giá trị': ''},
            {'Chỉ số': 'Bầu 1 người', 'Giá trị': stats['vote_1']},
            {'Chỉ số': 'Bầu 2 người', 'Giá trị': stats['vote_2']},
            {'Chỉ số': 'Bầu 3 người', 'Giá trị': stats['vote_3']},
        ]
        
        return pd.DataFrame(rows)
    
    def _create_candidates_dataframe(self, ballots: List[Dict]) -> pd.DataFrame:
        """Tạo DataFrame kết quả theo ứng viên"""
        collector = BallotDataCollector()
        collector.ballots = ballots
        stats = collector.get_statistics()
        
        rows = []
        for idx, (name, votes) in enumerate(stats['candidate_votes'].items(), 1):
            rows.append({
                'Thứ hạng': idx,
                'Tên ứng viên': name,
                'Số phiếu bầu': votes,
                'Tỷ lệ (%)': f"{(votes / stats['valid'] * 100) if stats['valid'] > 0 else 0:.2f}"
            })
        
        # Sắp xếp theo số phiếu giảm dần
        df = pd.DataFrame(rows)
        df = df.sort_values('Số phiếu bầu', ascending=False).reset_index(drop=True)
        df['Thứ hạng'] = range(1, len(df) + 1)
        
        return df


# ==================== INTEGRATION WITH STEP 1 ====================

def process_and_classify_ballot(detector, frame, ballot_id=None):
    """
    Tích hợp BƯỚC 1 & BƯỚC 2:
    Xử lý ảnh -> Phân loại -> Trả về đầy đủ thông tin
    
    Args:
        detector: Instance của BallotROIDetector (từ step1)
        frame: Ảnh phiếu bầu
        ballot_id: ID phiếu (tùy chọn)
        
    Returns:
        Tuple (crossed_status, classification, annotated_frame)
    """
    # BƯỚC 1: Detect ROI
    crossed_status, annotated_frame = detector.process_ballot(frame, visualize=True)
    
    # BƯỚC 2: Phân loại
    classifier = BallotClassifier()
    classification = classifier.classify_ballot(crossed_status)
    
    return crossed_status, classification, annotated_frame


# ==================== TEST FUNCTIONS ====================

def test_classifier():
    """Test chức năng phân loại"""
    print("\n" + "="*70)
    print("TEST: BALLOT CLASSIFIER")
    print("="*70)
    
    classifier = BallotClassifier()
    
    # Test cases
    test_cases = [
        {
            'name': 'Phiếu hợp lệ - Bầu 1 người',
            'crossed': [1, 1, 0, 1, 1],  # 4 gạch -> 1 người được chọn
            'expected': True
        },
        {
            'name': 'Phiếu hợp lệ - Bầu 2 người',
            'crossed': [1, 0, 0, 1, 1],  # 3 gạch -> 2 người được chọn
            'expected': True
        },
        {
            'name': 'Phiếu hợp lệ - Bầu 3 người',
            'crossed': [0, 0, 1, 1, 0],  # 2 gạch -> 3 người được chọn
            'expected': True
        },
        {
            'name': 'Phiếu KHÔNG hợp lệ - Không gạch ai',
            'crossed': [0, 0, 0, 0, 0],  # 0 gạch -> không hợp lệ
            'expected': False
        },
        {
            'name': 'Phiếu KHÔNG hợp lệ - Gạch 1 người',
            'crossed': [1, 0, 0, 0, 0],  # 1 gạch -> không hợp lệ
            'expected': False
        },
        {
            'name': 'Phiếu KHÔNG hợp lệ - Gạch tất cả',
            'crossed': [1, 1, 1, 1, 1],  # 5 gạch -> không hợp lệ
            'expected': False
        },
    ]
    
    passed = 0
    failed = 0
    
    for idx, test in enumerate(test_cases, 1):
        result = classifier.classify_ballot(test['crossed'])
        is_pass = result['is_valid'] == test['expected']
        
        status = "✅ PASS" if is_pass else "❌ FAIL"
        if is_pass:
            passed += 1
        else:
            failed += 1
        
        print(f"\nTest {idx}: {test['name']}")
        print(f"  Input: {test['crossed']}")
        print(f"  Result: {result['status_message']}")
        print(f"  {status}")
    
    print("\n" + "="*70)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("="*70)


def test_data_collection():
    """Test thu thập và xuất dữ liệu"""
    print("\n" + "="*70)
    print("TEST: DATA COLLECTION & EXCEL EXPORT")
    print("="*70)
    
    # Tạo collector
    collector = BallotDataCollector()
    
    # Thêm một số phiếu mẫu
    sample_ballots = [
        [1, 1, 0, 1, 1],  # Bầu 1 người
        [1, 0, 0, 1, 1],  # Bầu 2 người
        [0, 0, 1, 1, 0],  # Bầu 3 người
        [1, 0, 1, 0, 1],  # Bầu 2 người
        [0, 1, 1, 0, 1],  # Bầu 2 người
        [0, 0, 0, 0, 0],  # Không hợp lệ
        [1, 1, 1, 1, 1],  # Không hợp lệ
        [1, 1, 1, 0, 0],  # Bầu 2 người
    ]
    
    print("\nThêm phiếu vào collector...")
    for ballot in sample_ballots:
        collector.add_ballot(ballot)
    
    print(f"Đã thêm {len(sample_ballots)} phiếu")
    
    # In thống kê
    collector.print_statistics()
    
    # Xuất Excel
    print("\nXuất dữ liệu ra Excel...")
    exporter = ExcelExporter()
    output_file = exporter.export_to_excel(
        collector.get_ballots(),
        output_path="output/test_results.xlsx",
        include_statistics=True
    )
    
    if output_file:
        print(f"\n✅ Test hoàn tất! File đã được lưu tại: {output_file}")
        return output_file
    else:
        print("\n❌ Có lỗi khi xuất file")
        return None


if __name__ == "__main__":
    """
    Test script cho BƯỚC 2
    """
    import sys
    
    print("\n" + "="*70)
    print("BƯỚC 2: BALLOT CLASSIFIER & EXCEL EXPORT TEST")
    print("="*70)
    print("\nChọn chế độ test:")
    print("1. Test Classifier (phân loại phiếu)")
    print("2. Test Data Collection & Export Excel")
    print("3. Chạy tất cả tests")
    
    choice = input("\nNhập lựa chọn (1/2/3): ").strip()
    
    if choice == "1":
        test_classifier()
    elif choice == "2":
        test_data_collection()
    elif choice == "3":
        test_classifier()
        print("\n" + "="*70)
        test_data_collection()
    else:
        print("Lựa chọn không hợp lệ!")
