import random


def memory():
    try:
        file = open("рекомендации по запоминанию.txt", "r", encoding="utf8")
        memory = file.readlines()
        random.shuffle(memory)
        file.close()
        return memory[0]
    except Exception:
        return "ОШИБКА!!! Попробуй снова 🙃"
