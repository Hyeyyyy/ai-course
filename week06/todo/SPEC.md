```markdown
# 1. 개요
사용자가 할 일을 등록하고, 목록을 확인하며, 완료 상태를 변경하거나 삭제할 수 있는 단순한 할 일 관리(Todo) 웹 애플리케이션입니다.

# 2. 기술
- **Language:** Python
- **Framework:** Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS (Pure CSS)

# 3. 파일 구성
- `app.py`: Flask 서버 로직, 라우팅, DB 연동 및 CRUD 처리
- `database.db`: 할 일 데이터를 저장하는 SQLite 데이터베이스 파일
- `static/css/style.css`: 애플리케이션 디자인을 위한 커스텀 스타일시트
- `templates/index.html`: 할 일 목록 및 입력 폼이 포함된 메인 페이지

# 4. 동작 규칙

| 라우트 | 메서드 | 입력 | 결과 |
| :--- | :--- | :--- | :--- |
| `/` | GET | 없음 | 전체 할 일 목록 및 입력 양식 화면 출력 |
| `/add` | POST | `title` (String) | 새로운 할 일 생성 후 `/`로 리다이렉트 |
| `/toggle/<int:todo_id>` | POST | `todo_id` (Integer) | 해당 할 일의 완료 여부 반전 후 `/`로 리다이렉트 |
| `/delete/<int:todo_id>` | POST | `todo_id` (Integer) | 해당 할 일 삭제 후 `/`로 리다이렉트 |

# 5. 화면
- **메인 화면**:
    - 상단: 새로운 할 일을 입력할 수 있는 텍스트 필드와 '추가' 버튼
    - 중앙: 할 일 목록 (제목, 완료 여부, 생성 시각 표시)
        - 완료된 항목은 취소선 또는 시각적 스타일로 구분
        - 각 항목 옆에 '완료/미완료 전환' 버튼과 '삭제' 버튼 배치

# 6. 테스트

| 요청 | 기대하는 결과 |
| :--- | :--- |
| GET `/` | `index.html` 페이지가 정상적으로 로드됨 |
| POST `/add` (title="공부하기") | DB에 "공부하기"가 저장되고 `/`로 이동함 |
| POST `/add` (title="") | 빈 제목 입력 시 오류 없이 처리되거나 혹은 저장이 되지 않음 |
| POST `/add` (title=" " [공백만]) | 공백만 있는 제목이 허용되지 않도록 처리됨 |
| POST `/add` (매우 긴 문자열) | 데이터베이스 저장 제한 내에서 정상 작동함 |
| POST `/toggle/1` | ID가 1인 항목의 `is_completed` 값이 반전됨 |
| POST `/delete/1` | ID가 1인 항목이 DB에서 완전히 삭제됨 |
| GET `/toggle/999` (존재하지 않는 ID) | 404 에러를 반환하거나 오류 없이 메인으로 리다이렉트함 |
| GET `/delete/999` (존재하지 않는 ID) | 404 에러를 반환하거나 오류 없이 메인으로 리다이렉트함 |
| GET `/add` (잘못된 메서드 호출) | 405 Method Not Allowed 반환 |
| POST `/toggle/abc` (숫자가 아닌 ID) | 404 에러 또는 타입 불일치 에러 처리 |

# 7. 완료 전 점검
- [ ] 모든 CRUD 기능(조회, 추가, 완료 토글, 삭제)이 정상 작동하는가?
- [ ] SQLite 데이터베이스에 데이터가 올바르게 저장되고 삭제되는가?
- [ ] 외부 CSS 프레임워크 없이 순수 CSS만으로 레이아웃이 구성되었는가?
- [ ] HTML 템플릿이 Flask의 `render_template`을 통해 동적으로 렌더링되는가?

# 8. 하지 않는 것
- 사용자 인증 및 로그인 기능
- 기존 할 일의 내용을 수정하는 기능 (Update)
- Bootstrap, Tailwind CSS 등 외부 CSS 프레임워크 사용
- React, Vue.js 등 자바스크립트 프레임워크 사용
```