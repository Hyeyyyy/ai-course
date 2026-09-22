import json
import os

# 파일 경로 설정
TODO_FILE = 'todo.json'

def load_todos():
    """todo.json 파일에서 할 일 목록을 로드합니다."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def add_todo(todos):
    """새로운 할 일을 추가합니다."""
    task = input("추가할 할 일을 입력하세요: ").strip()
    if task:
        todos.append({"task": task, "completed": False})
        save_todos(todos)
        print(f"'{task}'(이)가 추가되었습니다.")
    else:
        print("할 일이 비어있을 수 없습니다.")

def view_todos(todos):
    """할 일 목록을 보여줍니다."""
    if not todos:
        print("\n현재 할 일이 없습니다.")
        return

    print("\n--- 할 일 목록 ---")
    for i, todo in enumerate(todos, 1):
        status = "[V]" if todo['completed'] else "[ ]"
        print(f"{i}. {status} {todo['task']}")
    print("------------------")

def complete_todo(todos):
    """할 일을 완료 상태로 변경합니다."""
    view_todos(todos)
    if not todos:
        return

    try:
        choice = int(input("완료 처리할 번호를 선택하세요: "))
        if 1 <= choice <= len(todos):
            todos[choice - 1]['completed'] = True
            save_todos(todos)
            print(f"{choice}번 할 일을 완료 처리했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def delete_todo(todos):
    """할 일을 삭제합니다."""
    view_todos(todos)
    if not todos:
        return

    try:
        choice = int(input("삭제할 번호를 선택하세요: "))
        if 1 <= choice <= len(todos):
            removed = todos.pop(choice - 1)
            save_todos(todos)
            print(f"'{removed['task']}'(이)가 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def main():
    """메인 메뉴 루프입니다."""
    while True:
        todos = load_todos()
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("원하는 작업의 번호를 입력하세요: ").strip()

        if choice == '1':
            add_todo(todos)
        elif choice == '2':
            view_todos(todos)
        elif choice == '3':
            complete_todo(todos)
        elif choice == '4':
            delete_todo(todos)
        elif choice == '5':
            print("프로그램을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("잘못된 입력입니다. 1~5 사이의 번호를 입력해주세요.")

if __name__ == "__main__":
    main()
