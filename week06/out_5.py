def format_phone_number(phone_raw):
    # 1. 숫자만 남기기
    num = ''.join(filter(str.isdigit, phone_raw))
    length = len(num)
    
    # 2. 시작 번호 확인
    prefix = num[:3]
    
    # 010 조건
    if prefix == '010':
        if length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    # 011, 016, 017, 018, 019 조건
    elif prefix in ['011', '016', '017', '018', '019']:
        if length == 10:
            return f"{num[:3]}-{num[3:6]}-{num[6:]}"
        elif length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "잘못된 구형 번호 형식입니다."
            
    else:
        return "지원하지 않는 번호 체계입니다."

# 테스트
print(format_phone_number("01012345678"))  # 010-1234-5678
print(format_phone_number("0111234567"))   # 011-123-4567 (10자리)
print(format_phone_number("01112345678"))  # 011-1234-5678 (11자리)
print(format_phone_number("0171234567"))   # 017-123-4567
