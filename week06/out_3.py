def format_phone_number(phone):
    # 숫자만 남기기 (하이픈이나 공백 제거)
    phone = ''.join(filter(str.isdigit, phone))
    length = len(phone)
    
    # 1. 010으로 시작하는 경우
    if phone.startswith('010'):
        if length == 11:
            return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    # 2. 기타 통신사 번호로 시작하는 경우
    elif phone.startswith(('011', '016', '017', '018', '019')):
        if length == 10:
            return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        elif length == 11:
            return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
        else:
            return "잘못된 번호 형식입니다."
            
    else:
        return "휴대폰 번호가 아닙니다."

# --- 테스트 ---
print(format_phone_number("01012345678"))  # 결과: 010-1234-5678 (11자리)
print(format_phone_number("0111234567"))  # 결과: 011-123-4567 (10자리)
print(format_phone_number("01712345678"))  # 결과: 017-1234-5678 (11자리)
print(format_phone_number("0101234567"))   # 결과: 잘못된 010 번호 형식입니다.
