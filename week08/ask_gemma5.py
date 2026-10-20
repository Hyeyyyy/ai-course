from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
기존 계산기에 구체적인 입력 오류 안내와 빈 목록 안내를 추가해줘.
오류가 나도 입력값과 기존 기록을 유지하고, 정상 계산하면 오류 안내를 지운다.
결과는 입출차 시각, 주차 시간, 요금이 읽기 쉽게 표시되도록 다듬는다.
기존 구조와 요금 규칙을 유지하고 스펙과 테스트도 함께 보완해줘.
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