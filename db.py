import sqlite3
from exam import Exam
from exam_progress import ExamProgress


class db:
    # Создаем подключение к базе данных (файл my_database.db будет создан)

    def __init__(self):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL
                )
                ''')
        self.connection.commit()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Exams (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                questions_count INTEGER,
                date DATETIME NOT NULL,
                progress INTEGER
                )
                ''')
        self.connection.commit()
        self.connection.close()

    def add_user(self, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (chat_id) VALUES (?);', (chat_id,))
        connection.commit()
        connection.close()

    def add_exam(self, exam, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchall()[0][0]

        cursor.execute('INSERT INTO Exams (user_id, name, questions_count, date) VALUES (?, ?, ?, ?)',
                       (user_id, exam.name, exam.questions_count, exam.date,))

        connection.commit()
        connection.close()

    def show_progress(self, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchall()[0][0]

        cursor.execute('SELECT name, progress * 100.0 / questions_count FROM Exams WHERE user_id = ?', (user_id,))
        progress = cursor.fetchall()

        connection.commit()
        connection.close()
        return progress

    def delete_exam(self, exam_name, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchall()[0][0]

        cursor.execute('DELETE FROM Exams WHERE user_id = ? and name = ?', (user_id, exam_name))
        connection.commit()
        connection.close()

    def update_progress(self, exam_progress, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchall()[0][0]

        cursor.execute("SELECT progress FROM Exams WHERE user_id = ? and name = ?", (user_id, exam_progress.name))
        current_progress = cursor.fetchall()[0][0]
        if current_progress is None:
            current_progress = 0
        exam_progress.progress += current_progress

        cursor.execute("UPDATE Exams SET progress = ? WHERE user_id = ? and name = ?", (exam_progress.progress, user_id, exam_progress.name))

        connection.commit()
        connection.close()

    def get_exams_names(self, chat_id):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchall()[0][0]

        cursor.execute('SELECT name FROM Exams WHERE user_id = ?', (user_id,))
        names = cursor.fetchall()

        return names

