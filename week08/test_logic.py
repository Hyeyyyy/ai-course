import unittest
from logic import calculate_parking_fee

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

    def test_max_fee(self):
        """최대 요금 20,000원 제한 확인"""
        # 매우 긴 시간 주차 (예: 10시간)
        self.assertEqual(calculate_parking_fee("09:00", "19:00"), 20000)

    # --- 예외 케이스 테스트 ---

    def test_invalid_time_format(self):
        """잘못된 시간 형식 입력 시 ValueError 발생 확인"""
        with self.assertRaises(ValueError) as cm:
            calculate_parking_fee("9:00", "09:30") # HH:MM 형식이 아님
        self.assertEqual(str(cm.exception), "시간 형식이 잘못되었습니다. HH:MM 형식이어야 합니다.")

        with self.assertRaises(ValueError):
            calculate_parking_fee("09:00", "25:00") # 유효하지 않은 시간

    def test_exit_before_entry(self):
        """출차 시간이 입차 시간보다 빠른 경우 ValueError 발생 확인"""
        with self.assertRaises(ValueError) as cm:
            calculate_parking_fee("10:00", "09:00")
        self.assertEqual(str(cm.exception), "출차 시간은 입차 시간보다 늦어야 합니다.")

if __name__ == "__main__":
    unittest.main()