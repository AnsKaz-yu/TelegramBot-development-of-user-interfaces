import telebot
import webbrowser
from exam import Exam, ExamProgress
from db import db
from telebot import types
from anecdote import joke

bot = telebot.TeleBot('6467477848:AAGiUpgDQX1ePytwoqVzvQ11RUr0O4cMJpc')  # это наш токен так скажем

MyProgress = ExamProgress()
MyExam = Exam()
Mydb = db()


def menu_markup():
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Анекдот для поднятия настроения")
    btn2 = types.KeyboardButton("❓ Рекомендации по запоминанию")
    btn3 = types.KeyboardButton("📌 Добавить экзамен")
    btn4 = types.KeyboardButton("📓 Расписание")
    btn5 = types.KeyboardButton("❌ Удалить экзамен")
    btn6 = types.KeyboardButton("📈 Мой прогесс")
    btn7 = types.KeyboardButton("💪🏻 Я выучил новый вопрос!")
    menu_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return menu_markup


# стартовое меню
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я помогу тебе не завалить сессию!".format(
                         message.from_user), reply_markup=menu_markup())


# если мы хотим обрабатывать текст который написал нам пользователь
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Анекдот для поднятия настроения":
        bot.send_message(message.chat.id, text=joke())

    elif message.text == "❓ Рекомендации по запоминанию":
        bot.send_message(message.chat.id, text="У меня память как у золотой рыбки")

    elif message.text == "📌 Добавить экзамен":
        MyExam.clear()
        bot.send_message(message.from_user.id,
                         "Отлично! Чтобы добавить экзамен, пожалйства, ответь на несколько вопросов:")
        bot.send_message(message.from_user.id, "Какой экзамен сдаёешь?")
        bot.register_next_step_handler(message, get_name_of_exam)

    elif message.text == "📓 Расписание":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Расписание", url='https://ruz.spbstu.ru/')
        markup.add(button1)
        bot.send_message(message.chat.id,
                         "Найди свою группу тут:".format(message.from_user),
                         reply_markup=markup)
    elif message.text == "❌ Удалить экзамен":
        bot.send_message(message.from_user.id,
                         "Какой экзамен хочешь удалить?")
        bot.register_next_step_handler(message, delete_exam)
    elif message.text == "📈 Мой прогесс":
        bot.send_message(message.from_user.id,
                         "Твой прогресс по экзаменам:")
        show_exam_progress(message.chat.id)
    elif message.text == "💪🏻 Я выучил новый вопрос!":
        MyProgress.clear()
        bot.send_message(message.from_user.id,
                         "Круто! Расскажи, по какому предмету?")
        bot.register_next_step_handler(message, update_progress_exam_name)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")


def delete_exam(message):
    try:
        Mydb.delete_exam(message.text)
        bot.send_message(message.from_user.id,
                         f"Экзамен {message.text} успешно удалён")
    except Exception:
        bot.send_message(message.from_user.id,
                         "Не удалось удалить экзамен. Возможно, экзамена с теким названием не существует.")


def show_exam_progress(id):
    progress_list = Mydb.show_progress(id)
    if not progress_list:
        bot.send_message(id,
                         "У тебя еще нет добавленных экзаменов",
                         reply_markup=menu_markup())
    for i in progress_list:
        bot.send_message(id, text=f"Экзамен {i[0]}: {i[1]}%")


def update_progress_exam_name(message):
    global MyProgress
    MyProgress.name = message.text
    bot.send_message(message.from_user.id, "Сколько новых вопросов ты выучил?")
    bot.register_next_step_handler(message, update_progress_questions_count)


def update_progress_questions_count(message):
    global MyProgress
    try:
        MyProgress.progress = int(message.text)
        Mydb.update_progress(MyProgress)
        bot.send_message(message.chat.id,
                         "Прогресс успешно обновлен".format(message.from_user),
                         reply_markup=menu_markup())
    except Exception:
        bot.send_message(message.chat.id,
                         "Не удалось обновить прогресс. Попробуй снова!".format(message.from_user),
                         reply_markup=menu_markup())


def get_name_of_exam(message):
    global MyExam
    MyExam.set_name(message.text)
    if MyExam.i_know_all_necessary_information():
        MyExam.add_exam_to_database()
        bot.send_message(message.chat.id,
                         "Экзамен успешно добавлен".format(message.from_user),
                         reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Когда будет проходить экзамен?")
        bot.register_next_step_handler(message, get_date_of_exam)


def get_date_of_exam(message):
    global MyExam
    try:
        MyExam.set_date(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "Не удалось добавить дату( Попробуй ввести её снова!")
        bot.register_next_step_handler(message, get_date_of_exam)
        return

    if MyExam.i_know_all_necessary_information():
        MyExam.add_exam_to_database()
        bot.send_message(message.chat.id,
                         "Экзамен успешно добавлен".format(message.from_user),
                         reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Сколько вопросов/билетов нужно выучить?")
        bot.register_next_step_handler(message, get_count_of_questions)


def get_count_of_questions(message):
    global MyExam
    try:
        MyExam.set_questions_count(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "Не удалось добавить количество вопросов( Попробуй ещё раз!"
                                               "(Вводи цифры, пожалйста)")
        bot.register_next_step_handler(message, get_count_of_questions)
        return

    if MyExam.i_know_all_necessary_information():
        MyExam.add_exam_to_database()
        bot.send_message(message.chat.id,
                         "Экзамен успешно добавлен".format(message.from_user),
                         reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Какой экзамен сдаёшь?")
        bot.register_next_step_handler(message, get_name_of_exam)


bot.polling(none_stop=True)
