import unittest
from logic import calculate_parking_fee, calculate_parking_minutes, calculate_total_fee

class TestParkingFeeLogic(unittest.TestCase):

    # --- 정상 케이스 테스트 ---
    
    def test_free_period(self):
        """30분 이내 주차 시 0원 확인"""
        self.assertEqual(calculate_parking_fee("09:00", "09:30"), 0)
        self.assertEqual(calculate_parking_fee("09:00", "09:15"), 0)

    def test_exact_10min_intervals(self):
        """10분 단위로 딱 떨어지는 경우 확인"""
        # 30분(무료) + 10분(500원) = 40분 주차
        self.assertEqual(calculate_parking_fee("09:00", "09:40"), 500)
        # 30분(무료) + 20분(1000원) = 50분 주차
        self.assertEqual(calculate_parking_fee("09:00", "09:50"), 1000)

    def test_rounding_up(self):
        """10분 단위가 아닐 때 올림 처리 확인"""
        # 30분(무료) + 1분(초과) = 31분 주차 -> 10분 단위로 올림하여 500원
        self.assertEqual(calculate_parking_fee("09:00", "09:31"), 500)
        # 30분(무료) + 11분(초과) = 41분 주차 -> 20분 단위로 올림하여 1000원
        self.assertEqual(calculate_parking_fee("09:00", "09:41"), 1000)

    def test_additional_fee_cases(self):
        """초과 시간 계산의 대표 사례를 확인한다."""
        self.assertEqual(calculate_parking_fee("09:00", "09:50"), 1000)
        self.assertEqual(calculate_parking_fee("09:00", "10:00"), 1500)
        self.assertEqual(calculate_parking_fee("09:00", "11:00"), 4500)

    def test_max_fee(self):
        """최대 요금 20,000원 제한 확인"""
        # 매우 긴 시간 주차 (예: 10시간)
        self.assertEqual(calculate_parking_fee("09:00", "19:00"), 20000)

    def test_cap_boundary(self):
        """최대 요금 직전과 도달 및 초과 시점을 확인한다."""
        self.assertEqual(calculate_parking_fee("09:00", "16:00"), 19500)
        self.assertEqual(calculate_parking_fee("09:00", "16:01"), 20000)
        self.assertEqual(calculate_parking_fee("09:00", "16:10"), 20000)
        self.assertEqual(calculate_parking_fee("09:00", "16:11"), 20000)

    def test_parking_minutes(self):
        self.assertEqual(calculate_parking_minutes("09:00", "09:31"), 31)
        self.assertEqual(calculate_parking_minutes("00:00", "23:59"), 1439)
        with self.assertRaises(ValueError):
            calculate_parking_minutes("23:30", "00:30")

    def test_total_fee(self):
        self.assertEqual(calculate_total_fee([]), 0)
        self.assertEqual(calculate_total_fee([500, 1000, 1500]), 3000)
        self.assertEqual(calculate_total_fee([500, 1500]), 2000)

    # --- 예외 케이스 테스트 ---

    def test_invalid_time_format(self):
        """잘못된 시간 형식 입력 시 ValueError 발생 확인"""
        with self.assertRaises(ValueError) as cm:
            calculate_parking_fee("9:00", "09:30") # HH:MM 형식이 아님
        self.assertEqual(str(cm.exception), "입차 시각은 HH:MM 형식으로 입력하세요. (예: 09:30)")

        with self.assertRaises(ValueError):
            calculate_parking_fee("09:00", "25:00") # 유효하지 않은 시간

        with self.assertRaises(ValueError):
            calculate_parking_fee("09:00", "09:60") # 유효하지 않은 분

    def test_strict_time_format(self):
        """한 자리 시각과 빈 입력을 거부하는지 확인한다."""
        for entry, exit_time in [
            ("9:00", "09:30"),
            ("0900", "09:30"),
            ("09:0", "09:30"),
            ("09:000", "10:00"),
            ("24:00", "10:00"),
            ("09:00", "9:30"),
            ("09:00\n", "10:00"),
            ("", "09:30"),
            (None, "09:30"),
        ]:
            with self.assertRaises(ValueError):
                calculate_parking_fee(entry, exit_time)

    def test_exit_before_entry(self):
        """출차 시간이 입차 시간보다 빠른 경우 ValueError 발생 확인"""
        with self.assertRaises(ValueError) as cm:
            calculate_parking_fee("09:00", "08:59")
        self.assertEqual(
            str(cm.exception),
            "출차 시각은 입차 시각보다 늦어야 합니다. 자정을 넘기는 주차는 지원하지 않습니다.",
        )

    def test_exit_equal_entry(self):
        """입차와 출차가 같은 경우를 거부하는지 확인한다."""
        with self.assertRaises(ValueError):
            calculate_parking_fee("10:00", "10:00")

    def test_empty_exit_time(self):
        """출차 시각이 비어 있으면 거부하는지 확인한다."""
        with self.assertRaises(ValueError):
            calculate_parking_fee("10:00", "")
        with self.assertRaises(ValueError):
            calculate_parking_fee("10:00", None)

    def test_error_messages(self):
        """수정할 입력과 원인을 구체적으로 안내하는지 확인한다."""
        cases = [
            ("", "10:00", "입차 시각을 입력하세요."),
            (None, "10:00", "입차 시각을 입력하세요."),
            ("   ", "10:00", "입차 시각을 입력하세요."),
            ("09:00", "", "출차 시각을 입력하세요."),
            ("09:00", None, "출차 시각을 입력하세요."),
            ("09:00", "   ", "출차 시각을 입력하세요."),
            ("9:00", "10:00", "입차 시각은 HH:MM 형식으로 입력하세요. (예: 09:30)"),
            ("09:00", "9:30", "출차 시각은 HH:MM 형식으로 입력하세요. (예: 09:30)"),
            ("24:00", "24:10", "입차 시각은 00:00~23:59 범위로 입력하세요."),
            ("09:60", "10:00", "입차 시각은 00:00~23:59 범위로 입력하세요."),
            ("09:00", "25:00", "출차 시각은 00:00~23:59 범위로 입력하세요."),
            ("09:00", "09:00", "출차 시각은 입차 시각보다 늦어야 합니다."),
        ]
        for entry, exit_time, message in cases:
            with self.subTest(entry=entry, exit_time=exit_time):
                with self.assertRaises(ValueError) as cm:
                    calculate_parking_fee(entry, exit_time)
                self.assertEqual(str(cm.exception), message)

    def test_midnight_message(self):
        with self.assertRaises(ValueError) as cm:
            calculate_parking_fee("23:00", "01:00")
        self.assertIn("자정을 넘기는 주차는 지원하지 않습니다.", str(cm.exception))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParkingFeeLogic)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"최종 결과: 통과 {result.testsRun - len(result.failures) - len(result.errors)}개, 실패 {len(result.failures) + len(result.errors)}개")
    raise SystemExit(0 if result.wasSuccessful() else 1)
