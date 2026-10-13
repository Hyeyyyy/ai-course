import flet as ft

from logic import calculate_totals, create_transaction, reset_transactions


FONT = "Arial Rounded MT Bold"
PINK = "#ec6f9e"
LIGHT_PINK = "#f8c9dc"
TEXT_COLOR = "#4a3040"


def main(page: ft.Page):
    page.title = "용돈 기입장"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    transactions = []

    title = ft.Text(
        value="용돈 기입장 ♡",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=TEXT_COLOR,
        font_family=FONT,
    )
    content_field = ft.TextField(label="내용", value="", width=125)
    amount_field = ft.TextField(label="금액", value="", width=85)
    type_dropdown = ft.Dropdown(
        label="구분",
        value="지출",
        width=95,
        options=[ft.dropdown.Option("수입"), ft.dropdown.Option("지출")],
    )
    notice = ft.Text(value="", color=PINK, font_family=FONT)
    list_view = ft.ListView(expand=True, spacing=4)
    income_text = ft.Text(value="수입 0원", color=TEXT_COLOR, font_family=FONT)
    expense_text = ft.Text(value="지출 0원", color=TEXT_COLOR, font_family=FONT)
    balance_text = ft.Text(
        value="잔액 0원",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=TEXT_COLOR,
        font_family=FONT,
    )

    def refresh_summary():
        totals = calculate_totals(transactions)
        income_text.value = f"수입 {totals['income']:,}원"
        expense_text.value = f"지출 {totals['expense']:,}원"
        balance_text.value = f"잔액 {totals['balance']:,}원"

    def delete_transaction(e):
        transactions.pop(e.control.data)
        refresh_list()
        refresh_summary()
        page.update()

    def refresh_list():
        list_view.controls.clear()
        for index, transaction in enumerate(transactions):
            transaction_type = "수입" if transaction["type"] == "income" else "지출"
            list_view.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            value=transaction["content"],
                            width=95,
                            color=TEXT_COLOR,
                            font_family=FONT,
                        ),
                        ft.Text(
                            value=transaction_type,
                            width=45,
                            color=TEXT_COLOR,
                            font_family=FONT,
                        ),
                        ft.Text(
                            value=f"{transaction['amount']:,}원",
                            expand=True,
                            color=TEXT_COLOR,
                            font_family=FONT,
                        ),
                        ft.Button(
                            content="삭제",
                            data=index,
                            on_click=delete_transaction,
                            bgcolor=LIGHT_PINK,
                            color=TEXT_COLOR,
                        ),
                    ]
                )
            )

    def add_transaction(e):
        type_map = {"수입": "income", "지출": "expense"}
        try:
            transaction = create_transaction(
                content_field.value,
                amount_field.value,
                type_map[type_dropdown.value],
            )
        except (KeyError, ValueError):
            if not content_field.value or not content_field.value.strip():
                notice.value = "내용을 입력해주세요."
            else:
                notice.value = "금액은 0보다 큰 정수로 입력해주세요."
            page.update()
            return

        transactions.insert(0, transaction)
        content_field.value = ""
        amount_field.value = ""
        notice.value = ""
        refresh_list()
        refresh_summary()
        page.update()

    def clear_all(e):
        reset_transactions(transactions)
        content_field.value = ""
        amount_field.value = ""
        type_dropdown.value = "지출"
        notice.value = "모든 거래를 초기화했습니다."
        refresh_list()
        refresh_summary()
        page.update()

    add_button = ft.Button(
        content=ft.Text(value="추가", color="white", font_family=FONT),
        on_click=add_transaction,
        expand=True,
        height=42,
        bgcolor=PINK,
        color="white",
    )
    clear_button = ft.Button(
        content=ft.Text(value="전체 초기화", color=TEXT_COLOR, font_family=FONT),
        on_click=clear_all,
        expand=True,
        height=42,
        bgcolor=LIGHT_PINK,
        color=TEXT_COLOR,
    )

    page.add(
        title,
        ft.Row(controls=[content_field, amount_field, type_dropdown]),
        ft.Row(controls=[add_button, clear_button]),
        notice,
        list_view,
        ft.Row(controls=[income_text, expense_text]),
        balance_text,
    )


ft.run(main)
