def format_phone_number(num):
    # 숫자 이외의 문자(하이픈 등) 제거
    num = ''.join(filter(str.isdigit, str(num)))
    length = len(num)
    
    # 1. 010으로 시작하는 경우
    if num.startswith('010'):
        if length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "유효하지 않은 010 번호"

    # 2. 011, 016, 017, 018, 019로 시작하는 경우
    elif num.startswith(('011', '016', '017', '018', '019')):
        if length == 10:
            return f"{num[:3]}-{num[3:6]}-{num[6:]}"
        elif length == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        else:
            return "유효하지 않은 번호"
            
    else:
        return "대상 번호 아님"

# 테스트 결과
print(format_phone_number("01012345678"))   # 010-1234-5678 (11자리 성공)
print(format_phone_number("0101234567"))    # 유효하지 않은 010 번호 (10자리 탈락)
print(format_phone_number("0111234567"))    # 011-123-4567 (10자리 성공)
print(format_phone_number("01112345678"))   # 011-1234-5678 (11자리 성공)
print(format_phone_number("01712345678"))   # 017-1234-5678 (11자리 성공)
