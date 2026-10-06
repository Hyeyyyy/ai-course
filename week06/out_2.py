import re

def format_phone_number(phone_str):
    # 숫자만 남기기 (하이픈이나 공백 제거)
    digits = re.sub(r'\D', '', phone_str)
    
    # 1. 010으로 시작하는 경우
    if digits.startswith('010'):
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    # 2. 011, 016, 017, 018, 019로 시작하는 경우
    elif digits.startswith(('011', '016', '017', '018', '019')):
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 번호 길이입니다."
            
    else:
        return "지원하지 않는 번호 대역입니다."

# --- 테스트 코드 ---
test_cases = [
    "01012345678",   # 11자리 010
    "0101234567",    # 10자리 010 (오류 처리 대상)
    "0111234567",    # 10자리 011
    "01112345678",   # 11자리 011
    "0171234567",    # 10자리 017
    "01712345678",   # 11자리 017
    "01912345678",   # 11자리 019
    "021234567"      # 기타
]

for case in test_cases:
    print(f"{case} -> {format_phone_number(case)}")
