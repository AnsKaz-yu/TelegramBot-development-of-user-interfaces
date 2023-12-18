import telebot
import sqlite3
from exam import Exam
from exam_progress import ExamProgress
from db import db
from telebot import types
from anecdote import joke
from memory import memory
from graphics import make_graph

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
    menu_markup.row(btn1, btn2)
    menu_markup.row(btn3, btn5, btn6)
    menu_markup.row(btn4, btn7)
    return menu_markup


def exams_markup(chat_id):
    exam_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    exams = Mydb.get_exams_names(chat_id)
    for exam in exams:
        btn = types.KeyboardButton(exam[0])
        exam_markup.row(btn)
    return exam_markup


#стартовое меню
@bot.message_handler(commands=['start'])
def start(message):
    global Mydb
    try:
        img = open('кот.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        Mydb.add_user(message.chat.id)
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Я помогу тебе не завалить сессию!".format(
                             message.from_user), reply_markup=menu_markup())
    except Exception:
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}. К сожалению, у меня не получилось корректно запомнить тебя и "
                              "при дальнейшем использовании я могу лагать.\n\nПожалуйста, попоробуй применить команду "
                              "/start снова или напиши моему создателю @ans_kaz!".format(
                             message.from_user))


# если мы хотим обрабатывать текст который написал нам пользователь
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Анекдот для поднятия настроения":
        bot.send_message(message.chat.id, text=joke())

    elif message.text == "❓ Рекомендации по запоминанию":
        bot.send_message(message.chat.id, text=memory())

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
        bot.send_message(message.chat.id,
                         "Какой экзамен хочешь удалить?".format(message.from_user),
                         reply_markup=exams_markup(message.chat.id))
        bot.register_next_step_handler(message, delete_exam)
    elif message.text == "📈 Мой прогесс":
        show_exam_progress(message.chat.id)
    elif message.text == "💪🏻 Я выучил новый вопрос!":
        MyProgress.clear()
        bot.send_message(message.chat.id,
                         "Круто! Расскажи, по какому предмету?".format(message.from_user),
                         reply_markup=exams_markup(message.chat.id))
        bot.register_next_step_handler(message, update_progress_exam_name)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..", reply_markup=menu_markup())


def delete_exam(message):
    global Mydb
    try:
        Mydb.delete_exam(message.text, message.chat.id)
        bot.send_message(message.from_user.id,
                         f"Экзамен {message.text} успешно удалён", reply_markup=menu_markup())
    except Exception:
        bot.send_message(message.from_user.id,
                         "Не удалось удалить экзамен. Возможно, экзамена с теким названием не существует.", reply_markup=menu_markup())


def show_exam_progress(chat_id):
    global Mydb
    progress_list = []
    try:
        progress_list = Mydb.show_progress(chat_id)
    except Exception:
        bot.send_message(chat_id,
                         "Ой-ой. Какая-то ошибка... Попробуй снова или напиши моему создателю @ans.kaz",
                         reply_markup=menu_markup())
    if not progress_list:
        bot.send_message(chat_id,
                         "У тебя еще нет добавленных экзаменов",
                         reply_markup=menu_markup())
    for i in progress_list:
        if i[1] == None:
            bot.send_message(chat_id, text=f"{i[0]}: 0.0%")
            make_graph(bot, chat_id, 0)
        else:
            bot.send_message(chat_id, text=f"{i[0]}: {'{:.2f}'.format(i[1])}%")
            make_graph(bot, chat_id, i[1])


def update_progress_exam_name(message):
    global MyProgress
    MyProgress.name = message.text
    bot.send_message(message.from_user.id, "Сколько новых вопросов ты выучил?")
    bot.register_next_step_handler(message, update_progress_questions_count)


def update_progress_questions_count(message):
    global MyProgress, Mydb
    try:
        MyProgress.progress = int(message.text)
        Mydb.update_progress(MyProgress, message.chat.id)
        bot.send_message(message.chat.id,
                         "Прогресс успешно обновлен".format(message.from_user),
                         reply_markup=menu_markup())
    except Exception:
        bot.send_message(message.chat.id,
                         "Не удалось обновить прогресс. Попробуй снова!".format(message.from_user),
                         reply_markup=menu_markup())


def get_name_of_exam(message):
    global MyExam, Mydb
    MyExam.set_name(message.text)
    if MyExam.i_know_all_necessary_information():
        try:
            Mydb.add_exam(MyExam, message.chat.id)
            MyExam.clear()
            bot.send_message(message.chat.id,
                             "Экзамен успешно добавлен".format(message.from_user),
                             reply_markup=menu_markup())

        except Exception:
            bot.send_message(message.chat.id,
                             "Не удалось добавить экзамен".format(message.from_user),
                             reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Когда будет проходить экзамен?")
        bot.register_next_step_handler(message, get_date_of_exam)


def get_date_of_exam(message):
    global MyExam, Mydb
    try:
        MyExam.set_date(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "Не удалось добавить дату( Попробуй ввести её снова!")
        bot.register_next_step_handler(message, get_date_of_exam)
        return

    if MyExam.i_know_all_necessary_information():
        try:
            Mydb.add_exam(MyExam, message.chat.id)
            MyExam.clear()
            bot.send_message(message.chat.id,
                             "Экзамен успешно добавлен".format(message.from_user),
                             reply_markup=menu_markup())
        except Exception:
            bot.send_message(message.chat.id,
                             "Не удалось добавить экзамен".format(message.from_user),
                             reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Сколько вопросов/билетов нужно выучить?")
        bot.register_next_step_handler(message, get_count_of_questions)


def get_count_of_questions(message):
    global MyExam, Mydb
    try:
        MyExam.set_questions_count(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "Не удалось добавить количество вопросов( Попробуй ещё раз!"
                                               "(Вводи цифры, пожалйста)")
        bot.register_next_step_handler(message, get_count_of_questions)
        return

    if MyExam.i_know_all_necessary_information():
        try:
            Mydb.add_exam(MyExam, message.chat.id)
            MyExam.clear()
            bot.send_message(message.chat.id,
                             "Экзамен успешно добавлен".format(message.from_user),
                             reply_markup=menu_markup())
        except sqlite3.Error as error:
            bot.send_message(message.chat.id,
                             "Не удалось добавить экзамен".format(message.from_user),
                             reply_markup=menu_markup())
    else:
        bot.send_message(message.from_user.id, "Какой экзамен сдаёшь?")
        bot.register_next_step_handler(message, get_name_of_exam)


bot.polling(none_stop=True)
