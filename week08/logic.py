import math
import re
from datetime import datetime


def validate_time_format(time_str: str, label: str = "시각") -> None:
    """시간이 정확한 HH:MM 형식인지 검사한다."""
    if time_str is None or (isinstance(time_str, str) and not time_str.strip()):
        raise ValueError(f"{label}을 입력하세요.")
    if not isinstance(time_str, str) or not re.fullmatch(r"[0-9]{2}:[0-9]{2}", time_str):
        raise ValueError(f"{label}은 HH:MM 형식으로 입력하세요. (예: 09:30)")
    hour, minute = map(int, time_str.split(":"))
    if hour > 23 or minute > 59:
        raise ValueError(f"{label}은 00:00~23:59 범위로 입력하세요.")


def calculate_parking_minutes(entry_time_str: str, exit_time_str: str) -> int:
    """동일한 날의 유효한 입출차 시각에서 주차 시간(분)을 구한다."""
    time_format = "%H:%M"

    validate_time_format(entry_time_str, "입차 시각")
    validate_time_format(exit_time_str, "출차 시각")

    entry_time = datetime.strptime(entry_time_str, time_format)
    exit_time = datetime.strptime(exit_time_str, time_format)

    if exit_time == entry_time:
        raise ValueError("출차 시각은 입차 시각보다 늦어야 합니다.")
    if exit_time < entry_time:
        raise ValueError(
            "출차 시각은 입차 시각보다 늦어야 합니다. "
            "자정을 넘기는 주차는 지원하지 않습니다."
        )

    # 3. 총 주차 시간(분 단위) 계산
    duration_delta = exit_time - entry_time
    return int(duration_delta.total_seconds() / 60)


def calculate_parking_fee(entry_time_str: str, exit_time_str: str) -> int:
    """주차 요금을 계산하며 잘못된 입력은 ValueError로 알린다."""
    total_minutes = calculate_parking_minutes(entry_time_str, exit_time_str)

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


def calculate_total_fee(fees) -> int:
    """현재 목록에 남아 있는 요금의 합계를 구한다."""
    return sum(fees)
