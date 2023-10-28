import sqlite3
from exam import Exam, ExamProgress


class db:
    # Создаем подключение к базе данных (файл my_database.db будет создан)

    def __init__(self):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                chat_id TEXT NOT NULL
                )
                ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Exams (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                questions_count INT NOT NULL,
                date DATETIME NOT NULL
                )
                ''')
        self.connection.commit()
        self.connection.close()


    def add_exam_(self, exam):
        a = 0

    def show_progress(self, id):
        b = []
        return b

    def delete_exam(self, exam_name):
        a = 0

    def update_progress(self, exam_progress):
        b = 0
# connection.close()
