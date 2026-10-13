from logic import (
    calculate_totals,
    create_transaction,
    parse_amount,
    reset_transactions,
    validate_content,
)


passed = 0
failed = 0


def check(name, action, expected=None, expected_error=None):
    global passed, failed
    print(f"Running: {name}...", end=" ")
    try:
        result = action()
        if expected_error is not None:
            print("FAIL (expected an error)")
            failed += 1
        elif result != expected:
            print(f"FAIL (expected {expected!r}, got {result!r})")
            failed += 1
        else:
            print("PASS")
            passed += 1
    except Exception as error:
        if expected_error is not None and isinstance(error, expected_error):
            print(f"PASS (Caught expected {expected_error.__name__})")
            passed += 1
        else:
            print(f"FAIL ({type(error).__name__}: {error})")
            failed += 1


check("parse_amount('1,000')", lambda: parse_amount("1,000"), 1000)
check("parse_amount('00100')", lambda: parse_amount("00100"), 100)
check("parse_amount('abc')", lambda: parse_amount("abc"), expected_error=ValueError)
check("parse_amount('10.5')", lambda: parse_amount("10.5"), expected_error=ValueError)
check("parse_amount('0')", lambda: parse_amount("0"), expected_error=ValueError)
check("parse_amount('-100')", lambda: parse_amount("-100"), expected_error=ValueError)
check("parse_amount(' ')", lambda: parse_amount(" "), expected_error=ValueError)
check("parse_amount('1 000')", lambda: parse_amount("1 000"), expected_error=ValueError)
check("parse_amount('1,,000')", lambda: parse_amount("1,,000"), expected_error=ValueError)
check("validate_content('간식')", lambda: validate_content("간식"), True)
check("validate_content(' ')", lambda: validate_content(" "), False)
check(
    "calculate_totals([])",
    lambda: calculate_totals([]),
    {"income": 0, "expense": 0, "balance": 0},
)
check(
    "calculate_totals(income 1000, expense 300)",
    lambda: calculate_totals(
        [
            {"content": "A", "amount": 1000, "type": "income"},
            {"content": "B", "amount": 300, "type": "expense"},
        ]
    ),
    {"income": 1000, "expense": 300, "balance": 700},
)
check(
    "calculate_totals(expense 500, 200)",
    lambda: calculate_totals(
        [
            {"content": "A", "amount": 500, "type": "expense"},
            {"content": "B", "amount": 200, "type": "expense"},
        ]
    ),
    {"income": 0, "expense": 700, "balance": -700},
)
check(
    "create_transaction('간식', '1,000', 'expense')",
    lambda: create_transaction("간식", "1,000", "expense"),
    {"content": "간식", "amount": 1000, "type": "expense"},
)
transactions = [{"content": "점심", "amount": 8000, "type": "expense"}]
check("reset_transactions", lambda: (reset_transactions(transactions), transactions), (None, []))

print("-" * 64)
print(f"TEST SUMMARY: Passed: {passed}, Failed: {failed}")
if failed == 0:
    print("ALL TESTS PASSED!")
