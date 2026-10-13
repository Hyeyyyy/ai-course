import re

def parse_amount(value: str) -> int:
    """
    금액 문자열을 정수로 변환한다.
    - 앞뒤 공백 제거
    - 올바른 천 단위 쉼표 허용 (예: 1,000)
    - 잘못된 쉼표 형식 거부 (예: 1,,000, ,1000, 1000,)
    - 내부 공백 거부
    - 0보다 큰 양의 정수만 허용
    """
    if not isinstance(value, str):
        raise ValueError("Amount must be a string")
    
    s = value.strip()
    
    if not s:
        raise ValueError("Empty amount")

    # 내부 공백 체크 (strip 이후이므로 중간 공백이 있는지 확인)
    if ' ' in s:
        raise ValueError("Internal spaces are not allowed")

    # 쉼표 형식 검증 및 처리
    if ',' in s:
        # 정규식: 숫자로 시작하고, (,숫자3자리)가 반복되는 패턴
        if not re.match(r"^\d{1,3}(,\d{3})*$", s):
            raise ValueError("Invalid comma format")
        clean_s = s.replace(',', '')
    else:
        # 쉼표가 없는 경우 숫자만 있는지 확인
        if not s.isdigit():
            raise ValueError("Invalid numeric format")
        clean_s = s

    amount = int(clean_s)

    if amount <= 0:
        raise ValueError("Amount must be a positive integer")

    return amount

def validate_content(content: str) -> bool:
    """내용이 문자열이고 앞뒤 공백 제거 후 비어 있지 않으면 True"""
    if not isinstance(content, str):
        return False
    return len(content.strip()) > 0

def validate_type(transaction_type: str) -> bool:
    """'income' 또는 'expense'이면 True"""
    return transaction_type in ("income", "expense")

def calculate_totals(items: list[dict]) -> dict:
    """
    각 항목의 type과 amount를 이용해 수입 합계, 지출 합계, 잔액을 계산한다.
    """
    income_total = 0
    expense_total = 0
    
    for item in items:
        if item["type"] == "income":
            income_total += item["amount"]
        elif item["type"] == "expense":
            expense_total += item["amount"]
            
    return {
        "income": income_total,
        "expense": expense_total,
        "balance": income_total - expense_total
    }

def create_transaction(content: str, amount_text: str, transaction_type: str) -> dict:
    """
    내용과 금액과 구분을 검증하여 dict를 반환한다.
    """
    if not validate_content(content):
        raise ValueError("Invalid content")
    
    amount = parse_amount(amount_text)
    
    if not validate_type(transaction_type):
        raise ValueError("Invalid transaction type")
        
    return {
        "content": content.strip(),
        "amount": amount,
        "type": transaction_type
    }
