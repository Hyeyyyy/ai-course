from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
현재 logic.py와 test_logic.py를 검토하고 다음 문제만 수정해줘.

1. 시간은 반드시 정확히 HH:MM 형식만 허용한다.
   - "09:00"은 허용한다.
   - "9:00", "0900", "09:0", "09:000"은 거부한다.
   - 시는 00~23, 분은 00~59만 허용한다.

2. 입차와 출차가 같은 경우도 오류로 처리한다.
   - 출차 시간 <= 입차 시간이면 ValueError를 발생시킨다.

3. 빈 문자열과 None도 오류로 처리한다.

4. 주차 요금 계산 규칙은 변경하지 않는다.
   - 30분까지 무료
   - 초과 시간은 10분 단위 올림
   - 10분당 500원
   - 최대 20,000원

5. test_logic.py에 위 세 가지 오류 케이스를 추가한다.
6. 테스트 실행 결과에 통과 개수와 실패 개수가 명확히 출력되게 한다.
7. 화면 코드는 작성하지 않는다.
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