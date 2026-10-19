import random


class Question:

    PHI = (1 + 5 ** 0.5) / 2  # Золотое сечение

    def __init__(self, text: str):
        self.text = text
        self.words = text.split()
        self.correct_count = 0

    def get_probabilities(self, gender: str) -> list:

        n = len(self.words)
        if n == 0:
            return []
        if n == 1:
            return [1.0]

        probs = []
        remaining = 1.0
        for i in range(n - 1):
            p = remaining / self.PHI
            probs.append(p)
            remaining -= p
        probs.append(remaining)

        if gender == 'Ж':
            probs.reverse()

        return probs

    def student_answer(self, gender: str) -> str:
        probs = self.get_probabilities(gender)
        return random.choices(self.words, weights=probs, k=1)[0]

    def examiner_answers(self) -> list:

        n = len(self.words)
        if n == 0:
            return []

        shuffled = self.words[:]
        random.shuffle(shuffled)

        result = [shuffled[0]]

        for i in range(1, n):
            if random.random() < 1 / 3:
                result.append(shuffled[i])
            else:
                break

        return result

    def __repr__(self):
        return f"Question('{self.text[:20]}...')"