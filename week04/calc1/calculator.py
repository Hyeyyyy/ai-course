import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("파이썬 계산기")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # 계산 결과가 표시될 입력창
        self.expression = ""
        self.display_var = tk.StringVar()

        # 상단 디스플레이 생성
        self.create_display()
        # 버튼 레이아웃 생성
        self.create_buttons()

    def create_display(self):
        """숫자와 연산자가 표시될 디스플레이 영역을 만듭니다."""
        display_frame = tk.Frame(self.root, width=300, height=50, bg="gray")
        display_frame.pack(side=tk.TOP, fill=tk.BOTH)

        display_label = tk.Entry(
            display_frame, 
            textvariable=self.display_var, 
            font=("Arial", 24), 
            bg="#eee", 
            fg="black", 
            justify="right", 
            bd=10, 
            relief=tk.FLAT
        )
        display_label.pack(fill=tk.BOTH, expand=True)

    def create_buttons(self):
        """계산기 버튼들을 생성합니다."""
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # 버튼 배열 (텍스트, 행, 열)
        buttons = [
            ('C', 0, 0), ('/', 0, 1), ('*', 0, 2), ('DEL', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('-', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('+', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('=', 3, 3),
            ('0', 4, 0, 2), ('.', 4, 2) # 0은 두 칸 차지하도록 설정 예정
        ]

        # 버튼을 그리드(Grid) 형태로 배치
        for btn_info in buttons:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            
            # 0 버튼의 경우 colspan을 조절하기 위해 처리
            colspan = btn_info[3] if len(btn_info) > 3 else 1
            
            # 버튼 스타일 설정
            button_color = "#f0f0f0"
            if text in ['/', '*', '-', '+', '=']:
                button_color = "#ff9500"  # 연산자 색상 (주황색)
            elif text == 'C' or text == 'DEL':
                button_color = "#ff3b30"  # 기능 버튼 색상 (빨간색)

            button = tk.Button(
                buttons_frame, 
                text=text, 
                width=5, 
                height=2, 
                font=("Arial", 14, "bold"),
                bg=button_color,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew")

        # 그리드 비율 설정 (버튼이 창 크기에 맞춰 늘어나도록)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        """버튼 클릭 시 동작을 제어합니다."""
        if char == 'C':
            self.expression = ""
        elif char == 'DEL':
            self.expression = self.expression[:-1]
        elif char == '=':
            try:
                # eval 함수를 사용하여 문자열 수식을 계산합니다.
                # 주의: 실제 서비스용 앱에서는 보안을 위해 eval 대신 직접 파서를 만들어야 합니다.
                self.expression = str(eval(self.expression))
            except ZeroDivisionError:
                messagebox.showerror("오류", "0으로 나눌 수 없습니다.")
                self.expression = ""
            except Exception:
                messagebox.showerror("오류", "잘못된 수식입니다.")
                self.expression = ""
        else:
            self.expression += str(char)

        self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
