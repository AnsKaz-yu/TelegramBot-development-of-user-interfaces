import datetime

class Exam:
    name = ""
    date = datetime.date(1990, 1, 1)
    questions_count = 0

    def set_name(self, name):
        self.name = name

    def set_date(self, datestring):
        d = datestring.split('.')
        self.date = datetime.date(int(d[2]), int(d[1]), int(d[0]))

    def set_questions_count(self, count):
        self.questions_count = int(count)

    def i_know_all_necessary_information(self):
        if self.name == "" or self.questions_count == 0 or self.date == datetime.date(1990, 1, 1):
            return False
        return True

    def add_exam_to_database(self):
        # adding to database
        self.clear()

    def clear(self):
        self.name = ""
        self.date = datetime.date(1990, 1, 1)
        self.questions_count = 0

class ExamProgress:
    name = ""
    progress = 0
    def clear(self):
        name = ""
        progress = 0