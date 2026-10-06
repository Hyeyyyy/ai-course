import unittest
import os
import sqlite3
from app import app

class TodoAppTestCase(unittest.TestCase):
    def setUp(self):
        # 테스트용 설정
        self.app = app.test_client()
        self.app.testing = True
        self.test_db = 'test_todo.db'
        
        # app.py의 DATABASE를 테스트용으로 교체하기 위해 monkeypatching
        import app as app_module
        self.original_db = app_module.DATABASE
        app_module.DATABASE = self.test_db
        
        # 테스트용 DB 초기화
        conn = sqlite3.connect(self.test_db)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_completed BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def tearDown(self):
        # 테스트 종료 후 DB 삭제
        import app as app_module
        app_module.DATABASE = self.original_db
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except Exception:
                pass

    def test_get_index(self):
        """GET / 호출 시 페이지가 정상적으로 로드됨"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('나의 할 일 목록', response.get_data(as_text=True))

    def test_add_valid_todo(self):
        """POST /add (정상 제목) -> 성공 및 리다이렉트 확인"""
        response = self.app.post('/add', data={'title': 'Test Todo'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Todo', response.get_data(as_text=True))

    def test_add_empty_title(self):
        """POST /add (빈 제목) -> 데이터가 추가되지 않음"""
        conn = sqlite3.connect(self.test_db)
        count = conn.execute('SELECT COUNT(*) FROM todos').fetchone()[0]
        conn.close()
        
        self.app.post('/add', data={'title': ''}, follow_redirects=True)
        
        conn = sqlite3.connect(self.test_db)
        new_count = conn.execute('SELECT COUNT(*) FROM todos').fetchone()[0]
        conn.close()
        self.assertEqual(count, new_count)

    def test_add_whitespace_title(self):
        """POST /add (공백만 있는 제목) -> 데이터가 추가되지 않음"""
        conn = sqlite3.connect(self.test_db)
        count = conn.execute('SELECT COUNT(*) FROM todos').fetchone()[0]
        conn.close()
        
        self.app.post('/add', data={'title': '   '}, follow_redirects=True)
        
        conn = sqlite3.connect(self.test_db)
        new_count = conn.execute('SELECT COUNT(*) FROM todos').fetchone()[0]
        conn.close()
        self.assertEqual(count, new_count)

if __name__ == '__main__':
    unittest.main()
