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
