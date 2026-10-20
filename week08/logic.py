import math
import re
from datetime import datetime


def validate_time_format(time_str: str) -> None:
    """시간이 정확한 HH:MM 형식인지 검사한다."""
    if not isinstance(time_str, str) or not time_str:
        raise ValueError("시간은 비어 있을 수 없습니다.")
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", time_str):
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식이어야 합니다.")

def calculate_parking_fee(entry_time_str: str, exit_time_str: str) -> int:
    """
    입차 및 출차 시간을 받아 주차 요금을 계산합니다.
    
    :param entry_time_str: 입차 시간 (HH:MM)
    :param exit_time_str: 출차 시간 (HH:MM)
    :return: 계산된 주차 요금 (int)
    :raises ValueError: 시간 형식이 잘못되었거나 출차 시간이 입차 시간보다 빠를 경우
    """
    time_format = "%H:%M"

    validate_time_format(entry_time_str)
    validate_time_format(exit_time_str)

    entry_time = datetime.strptime(entry_time_str, time_format)
    exit_time = datetime.strptime(exit_time_str, time_format)

    # 2. 출차 시간이 입차 시간보다 늦어야 함 검증
    if exit_time <= entry_time:
        raise ValueError("출차 시간은 입차 시간보다 늦어야 합니다.")

    # 3. 총 주차 시간(분 단위) 계산
    duration_delta = exit_time - entry_time
    total_minutes = int(duration_delta.total_seconds() / 60)

    # 4. 요금 계산 로직
    # 30분까지는 무료
    if total_minutes <= 30:
        return 0

    # 30분을 초과한 시간 계산
    excess_minutes = total_minutes - 30

    # 10분의 배수가 아니면 올림 (예: 31분 -> 40분으로 계산)
    # math.ceil(excess_minutes / 10) * 10 방식을 사용하여 10분 단위로 올림 처리
    billable_units = math.ceil(excess_minutes / 10)
    
    # 10분당 500원
    fee = billable_units * 500

    # 5. 최대 요금 제한 (20,000원)
    max_fee = 20000
    return min(fee, max_fee)
