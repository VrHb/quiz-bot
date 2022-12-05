import os


def get_questions_and_answers_from_file(path, file_name):
    quiz = {}
    with open(
        os.path.join(path, file_name),
        encoding="KOI8-R"
        ) as file:
        text = file.read()
        for text_peace in text.split("\n\n"):
            if text_peace.startswith("Вопрос"):
                question = text_peace 
            if text_peace.startswith("Ответ"):
                quiz[question] = text_peace 
    return quiz
