from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
주차 요금 계산 로직을 작성해줘.

규칙:
- 입력 시각은 HH:MM 형식이다. 예: 09:30
- 출차는 입차보다 늦어야 한다.
- 30분까지는 무료이며 요금은 0원이다.
- 30분을 초과한 시간만 계산한다.
- 초과 시간이 10분의 배수가 아니면 올림한다.
- 10분마다 500원이다.
- 최대 요금은 20,000원이다.
- 할인, 기본요금, 심야 할증은 추가하지 않는다.
- 잘못된 입력 처리도 작성한다.
- 화면 코드는 작성하지 않는다.
- Flet은 import하지 않는다.
- logic.py에 사용할 함수와 test_logic.py 테스트를 작성한다.
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