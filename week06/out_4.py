def format_phone_number(phone_str):
    # 1. 숫자만 남기기
    num = ''.join(filter(str.isdigit, phone_str))
    length = len(num)
    
    if length < 10:
        return "Invalid Number"

    prefix = num[:3]
    
    # 2. 규칙 적용
    # 010으로 시작하는 경우
    if prefix == '010':
        if length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "Invalid 010 Number" # 010은 11자리만 인정한다는 규칙 적용

    # 011, 016, 017, 018, 019로 시작하는 경우
    elif prefix in ['011', '016', '017', '018', '019']:
        if length == 10:
            return f"{num[:3]}-{num[3:6]}-{num[6:]}"
        elif length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "Invalid Number Length"
            
    else:
        return "Unknown Prefix"

# 테스트
print(format_phone_number("01012345678"))  # 010-1234-5678 (X) -> 규칙상 11자리만 가능하므로 010-1234-5678 형태가 되려면 11자리여야 함
# 위 예시는 11자리 입력 시: 010-1234-5678
print(format_phone_number("0111234567"))   # 011-123-4567
print(format_phone_number("01612345678"))  # 016-1234-5678
