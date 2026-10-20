from openai import OpenAI

client = OpenAI(
    base_url="https://krchoi.com/gemma4/v1",
    api_key="none",
)

prompt = """
아래 주차 요금 계산기의 디자인을 깔끔하고 완성도 높은 데스크톱 앱처럼 개선해줘.

Python Flet 1.0을 사용한다. main.py의 화면 디자인만 수정하고,
기존 계산·추가·삭제·합계·오류 안내 기능은 유지한다.
logic.py와 test_logic.py는 수정하지 않는다.

디자인 방향:
- 밝은 회색 배경, 흰색 입력 영역, 짙은 남색 글자,
  파란색 강조 버튼으로 차분하고 일관된 화면을 만든다.
- 과한 장식, 이모지, 그라데이션은 사용하지 않는다.
- 제목, 설명, 입력 영역, 결과 목록, 합계 사이에 충분한 여백을 둔다.
- 제목은 크게, 보조 설명은 작고 차분하게 표시한다.

화면 구성:
- 상단: '주차 요금 계산기' 제목과 간결한 요금 안내
- 입력 영역: 입차·출차 입력창을 나란히 배치하고 크기를 통일
- 계산 버튼: 입력 영역 아래에 넓고 눈에 잘 띄게 배치
- 결과 목록: 입출차 시각, 주차 시간, 요금이 구분되도록 정돈
- 삭제 버튼: 계산 버튼보다 작고 덜 강조된 형태로 표시
- 하단 합계: '오늘 받은 요금'과 큰 금액으로 가장 중요한 결과를 강조

세부 조건:
- 창 크기는 약 600×720으로 조정하고 목록은 스크롤되게 한다.
- 긴 오류 문구가 잘리거나 다른 요소와 겹치지 않게 한다.
- 빈 목록 안내는 차분하게 표시한다.
- 금액의 천 단위 쉼표를 유지한다.
- 색상, 글자 크기, 간격은 소수의 일관된 값으로 사용한다.
- 기존 프로젝트의 Flet 문법을 참고하고 Flet 1.0에서 지원하는 API만 사용한다.
- 외부 패키지나 이미지 없이 구현한다.

설명은 짧게 하고, 바로 저장해 실행할 수 있는 main.py 전체 코드를 출력해줘.

import flet as ft
from logic import calculate_parking_fee, calculate_parking_minutes, calculate_total_fee


def main(page: ft.Page):
    page.title = "주차 요금 계산기"
    page.window.width = 520
    page.window.height = 600
    page.window.resizable = False

    entry_time = ft.TextField(label="입차 시각 (HH:MM)", value="", width=230)
    exit_time = ft.TextField(label="출차 시각 (HH:MM)", value="", width=230)
    notice = ft.Text(value="시각은 09:30처럼 입력하세요. 같은 날 주차만 계산합니다.",
                     color=ft.Colors.BLUE)
    items = ft.ListView(expand=True, spacing=4)
    items.controls.append(ft.Text(value="아직 계산한 기록이 없습니다."))
    total = ft.Text(value="오늘 받은 요금 합계: 0원", size=20,
                    weight=ft.FontWeight.BOLD)
    records = []

    def refresh_list():
        items.controls.clear()
        if not records:
            items.controls.append(ft.Text(value="아직 계산한 기록이 없습니다."))
        for index, record in enumerate(records):
            items.controls.append(ft.Row(controls=[
                ft.Text(
                    value=(f"{record['entry']} → {record['exit']}\n"
                           f"주차 시간: {record['minutes']}분 | 요금: {record['fee']:,}원"),
                    expand=True,
                ),
                ft.Button(content="삭제", data=index, on_click=on_delete),
            ]))
        amount = calculate_total_fee(record['fee'] for record in records)
        total.value = f"오늘 받은 요금 합계: {amount:,}원"
        page.update()

    def on_delete(e):
        records.pop(e.control.data)
        notice.value = "기록을 삭제했습니다."
        notice.color = ft.Colors.BLUE
        refresh_list()

    def on_calculate(e):
        try:
            fee = calculate_parking_fee(entry_time.value, exit_time.value)
            minutes = calculate_parking_minutes(entry_time.value, exit_time.value)
        except ValueError as error:
            notice.value = str(error)
            notice.color = ft.Colors.RED
            page.update()
            return

        records.append({
            "entry": entry_time.value,
            "exit": exit_time.value,
            "minutes": minutes,
            "fee": fee,
        })
        notice.value = "계산 결과를 추가했습니다."
        notice.color = ft.Colors.BLUE
        refresh_list()

    page.add(
        ft.Text(value="주차 요금 계산기", size=24, weight=ft.FontWeight.BOLD),
        ft.Text(value="30분까지 무료 · 이후 10분마다 500원 · 최대 20,000원"),
        ft.Row(controls=[entry_time, exit_time]),
        ft.Button(content="계산", on_click=on_calculate, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        notice,
        ft.Text(value="계산 결과 목록"),
        items,
        total,
    )


if __name__ == "__main__":
    ft.run(main)

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