import flet as ft


def main(page: ft.Page):
    page.title = "주차 요금 계산기"
    page.window.width = 520
    page.window.height = 600
    page.window.resizable = False

    entry_time = ft.TextField(label="입차 시각 (HH:MM)", value="", width=230)
    exit_time = ft.TextField(label="출차 시각 (HH:MM)", value="", width=230)
    notice = ft.Text(value="시각은 09:30처럼 입력하세요.", color=ft.Colors.BLUE)
    items = ft.ListView(expand=True, spacing=4)
    total = ft.Text(value="오늘 받은 요금 합계: 0원", size=20,
                    weight=ft.FontWeight.BOLD)

    def on_calculate(e):
        # 이번 단계에서는 창과 버튼의 동작만 확인한다.
        notice.value = "버튼 동작 확인 완료. 계산 기능은 다음 단계에서 연결합니다."
        page.update()

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
