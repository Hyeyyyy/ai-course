from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    amount = ""
    people = ""

    if request.method == 'POST':
        try:
            amount_str = request.form.get('amount', '')
            people_str = request.form.get('people', '')

            if not amount_str or not people_str:
                error = "금액과 인원수를 모두 입력해주세요."
            else:
                amount = float(amount_str)
                people = int(people_str)

                if people <= 0:
                    error = "인원수는 1명 이상이어야 합니다."
                else:
                    result = amount / people
        except ValueError:
            error = "올바른 숫자를 입력해주세요."

    return render_template('index.html', result=result, error=error, amount=amount, people=people)

if __name__ == '__main__':
    app.run(debug=True)
