from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
주차 요금 계산기의 기능을 유지하면서 main.py의 디자인을 개선해줘.

- 창 크기는 620×800으로 한다.
- 밝은 회색 배경에 흰색 카드를 배치한다.
- 입력 영역, 주차 기록, 합계 영역을 구분한다.
- 제목과 합계는 크게, 안내 문구는 작게 표시한다.
- 입력창 두 개는 나란히 배치하고 크기를 통일한다.
- 계산 버튼은 넓은 파란색 버튼으로 만든다.
- 기록은 연한 회색 배경의 행으로 표시하고 삭제 버튼을 붙인다.
- 주차 기록 옆에 현재 기록 건수를 표시한다.
- 합계 영역은 연한 파란색 배경과 큰 금액으로 강조한다.
- 모서리를 둥글게 하고 요소 사이에 충분한 여백을 둔다.
- 기존 입력 검증, 계산, 삭제, 합계 기능은 유지한다.

Python Flet 1.0에서 동작하게 작성하고,
logic.py와 test_logic.py는 수정하지 않는다.
"""

response = client.chat.completions.create(
    model="gemma4",
    temperature=0.2,
    max_tokens=3000,
    messages=[
        {"role": "user", "content": prompt}
    ],
)

print(response.choices[0].message.content)