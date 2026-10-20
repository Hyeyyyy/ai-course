from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
test_logic.py를 스펙과 대조해 수정해줘.

- 09:00부터 15:00까지는 16,500원이므로 기대값을 수정한다.
- 20,000원 최대 요금 테스트는 09:00부터 19:00까지로 바꾼다.
- 31분, 41분, 50분, 120분 주차 테스트를 추가한다.
- 테스트 변수명 exit는 exit_time으로 바꾼다.
- logic.py의 계산 규칙은 변경하지 않는다.
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