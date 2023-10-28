import random


def joke():
    try:
        file = open("анекдоты.txt", "r", encoding="utf8")
        jokes = file.readlines()
        random.shuffle(jokes)
        file.close()
        return jokes[0]
    except Exception:
        return "ОШИБКА!!! Попробуй снова 🙃"
