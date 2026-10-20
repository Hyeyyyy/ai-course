import flet as ft
from logic import calculate_parking_fee, calculate_parking_minutes, calculate_total_fee


# 화면에서 반복해서 사용하는 색상
BACKGROUND = "#F4F6FA"
SURFACE = "#FFFFFF"
INK = "#172B4D"
MUTED = "#536580"
BORDER = "#DDE4EF"
BLUE = "#245CDD"
BLUE_LIGHT = "#EFF4FF"
RED = "#B42318"


def main(page: ft.Page):
    page.title = "주차 요금 계산기"
    page.window.width = 620
    page.window.height = 800
    page.window.resizable = False
    page.bgcolor = BACKGROUND
    page.padding = 24
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=BLUE,
        font_family="Malgun Gothic",
        use_material3=True,
    )

    def time_field(label, hint):
        return ft.TextField(
            label=label, hint_text=hint, value="", expand=True,
            text_size=20, color=INK,
            label_style=ft.TextStyle(size=13, color=MUTED),
            hint_style=ft.TextStyle(color="#8190A6"),
            filled=True, fill_color="#FAFBFD",
            border={
                ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                    border_radius=10, side=ft.BorderSide(width=1, color=BORDER),
                ),
                ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                    border_radius=10, side=ft.BorderSide(width=2, color=BLUE),
                ),
            },
            content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
        )

    entry_time = time_field("입차 시각", "09:00")
    exit_time = time_field("출차 시각", "10:30")
    notice = ft.Text(
        value="HH:MM 형식으로 입력하세요. 같은 날 주차만 계산합니다.",
        size=12, color=MUTED,
    )
    items = ft.ListView(expand=True, spacing=8, padding=0)
    record_count = ft.Text(value="0건", size=12, color=MUTED)
    total = ft.Text(value="0원", size=30, weight=ft.FontWeight.BOLD, color=BLUE)
    records = []

    def empty_state():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value="아직 계산한 기록이 없습니다.",
                            size=14, color=MUTED, weight=ft.FontWeight.W_500),
                    ft.Text(value="입출차 시각을 입력하면 여기에 기록됩니다.",
                            size=12, color=MUTED),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(vertical=30, horizontal=12),
            alignment=ft.Alignment.CENTER,
        )

    def refresh_list():
        items.controls.clear()
        if not records:
            items.controls.append(empty_state())
        for index, record in enumerate(records):
            items.controls.append(ft.Container(
                bgcolor="#F8FAFD", border_radius=10,
                padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    value=f"{record['entry']} → {record['exit']}",
                                    size=15, weight=ft.FontWeight.W_600, color=INK,
                                ),
                                ft.Text(
                                    value=(f"주차 시간: {record['minutes']}분 | "
                                           f"요금: {record['fee']:,}원"),
                                    size=12, color=MUTED,
                                ),
                            ],
                            spacing=5, expand=True,
                        ),
                        ft.Button(
                            content="삭제", data=index, on_click=on_delete,
                            tooltip="이 주차 기록 삭제", height=36, elevation=0,
                            bgcolor=SURFACE, color=MUTED,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                side=ft.BorderSide(width=1, color=BORDER),
                                padding=ft.Padding.symmetric(horizontal=14),
                            ),
                        ),
                    ],
                    spacing=12,
                ),
            ))
        amount = calculate_total_fee(record['fee'] for record in records)
        total.value = f"{amount:,}원"
        record_count.value = f"{len(records)}건"
        page.update()

    def on_delete(e):
        records.pop(e.control.data)
        notice.value = "기록을 삭제했습니다."
        notice.color = MUTED
        refresh_list()

    def on_calculate(e):
        try:
            fee = calculate_parking_fee(entry_time.value, exit_time.value)
            minutes = calculate_parking_minutes(entry_time.value, exit_time.value)
        except ValueError as error:
            notice.value = str(error)
            notice.color = RED
            page.update()
            return

        records.append({
            "entry": entry_time.value,
            "exit": exit_time.value,
            "minutes": minutes,
            "fee": fee,
        })
        notice.value = "계산 결과를 추가했습니다."
        notice.color = BLUE
        refresh_list()

    items.controls.append(empty_state())
    calculate = ft.Button(
        content="주차 요금 계산", on_click=on_calculate,
        height=48, bgcolor=BLUE, color=SURFACE, elevation=0,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
        ),
    )
    header = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(value="P", size=26, weight=ft.FontWeight.BOLD,
                                color=SURFACE),
                width=48, height=48, bgcolor=BLUE, border_radius=14,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Column(
                controls=[
                    ft.Text(value="주차 요금 계산기", size=25,
                            weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text(value="입차부터 정산까지, 한눈에.", size=12, color=MUTED),
                ],
                spacing=4, expand=True,
            ),
        ],
        spacing=14,
    )
    input_card = ft.Container(
        bgcolor=SURFACE, border=ft.Border.all(1, BORDER), border_radius=16,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(value="주차 시간 입력", size=15,
                                weight=ft.FontWeight.BOLD, color=INK, expand=True),
                        ft.Container(
                            content=ft.Text(value="30분 무료", size=11,
                                            color=BLUE, weight=ft.FontWeight.W_600),
                            bgcolor=BLUE_LIGHT, border_radius=6,
                            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                        ),
                    ],
                ),
                ft.Row(controls=[entry_time, exit_time], spacing=14),
                ft.Text(value="이후 10분마다 500원 · 하루 최대 20,000원",
                        size=12, color=MUTED),
                calculate,
                notice,
            ],
            spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )
    history_card = ft.Container(
        bgcolor=SURFACE, border=ft.Border.all(1, BORDER), border_radius=16,
        padding=20, expand=True,
        content=ft.Column(
            controls=[
                ft.Row(controls=[
                    ft.Text(value="주차 기록", size=15,
                            weight=ft.FontWeight.BOLD, color=INK, expand=True),
                    record_count,
                ]),
                items,
            ],
            spacing=14, expand=True,
        ),
    )
    summary = ft.Container(
        bgcolor=BLUE_LIGHT, border_radius=16,
        padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(value="오늘 받은 요금", size=14,
                                weight=ft.FontWeight.W_600, color=INK),
                        ft.Text(value="현재 목록 기준", size=11, color=MUTED),
                    ],
                    spacing=4, expand=True,
                ),
                total,
            ],
            spacing=12,
        ),
    )
    page.add(ft.Column(
        controls=[header, input_card, history_card, summary],
        spacing=18, expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    ))


if __name__ == "__main__":
    ft.run(main)
