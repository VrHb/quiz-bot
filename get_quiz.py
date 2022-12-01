import os


for root, dirs, files in os.walk("./quiz-questions"):
    for file in files:
        pass


def get_questions_and_answers_from_file(file_name):
    quiz = {}
    with open(
        os.path.join("./quiz-questions", file_name),
        encoding="KOI8-R"
        ) as file:
        text = file.read()
        for text_peace in text.split("\n\n"):
            if text_peace.startswith("Вопрос"):
                question = text_peace 
            if text_peace.startswith("Ответ"):
                quiz[question] = text_peace 


if __name__ == "__main__":
    get_questions_and_answers_from_file("120br2.txt")
