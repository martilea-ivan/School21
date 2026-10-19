class Student:

    _id_counter = 0

    def __init__(self, name: str, gender: str):
        Student._id_counter += 1
        self.id = Student._id_counter
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.exam_time = None
        self.examiner_name = None
        self.correct_answers = 0

    def __repr__(self):
        return f"Student({self.id}: {self.name}, {self.status})"