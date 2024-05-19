import os

import telebot
import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
import io
import contextvars
user_states = {}
class UserState:
    def __init__(self, survey_id, current_question, col_questions, questions):
        self.survey_id = survey_id
        self.current_question = current_question
        self.col_questions = col_questions
        self.questions = questions

def get_user_state(chat_id):
    if chat_id not in user_states:
        user_states[chat_id] = UserState(None, 0, 0, [])
    return user_states[chat_id]
bot = telebot.TeleBot('7082484484:AAGvOulj_lXSQO2fmklzUJMPM7_24tpWB70')
names = {}
admin = None
#current_question = None
#col_questions = None
sn = None
ii = 0
iii = 0
col = 0
col1 = 0
sn_update = None
def check_admin(chat_id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT admin FROM users2 WHERE chat_id=?", (chat_id,))
    admin = cur.fetchone()
    cur.close()
    conn.close()
    return admin


def check_survey(id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT survey_name FROM survey WHERE survey_name=?", [id])
    ch = cur.fetchone()
    cur.close()
    conn.close()
    return ch


def check_prava(chat_id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT admin FROM users2 WHERE chat_id=?", (chat_id,))
    status = cur.fetchone()
    cur.close()
    conn.close()
    return status


def check_reg(chat_id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users2 WHERE chat_id=?", (chat_id,))
    status = cur.fetchone()
    cur.close()
    conn.close()
    return status


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users2 (id INTEGER NOT NULL, chat_id INTEGER, first_name varchar(50), last_name varchar(50), admin int, PRIMARY KEY(id AUTOINCREMENT))')
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.InlineKeyboardButton('Список пользователей', callback_data='button3')
    item2 = telebot.types.KeyboardButton('Зарегистрироваться')
    item3 = telebot.types.KeyboardButton('Продолжить')
    markup.add(item1, item2, item3)
    bot.reply_to(message, "Хотите зарегистрироваться или продолжить?", reply_markup=markup)
    # bot.send_message(message.chat.id, 'Для регистрации введите ваше имя')
    # bot.register_next_step_handler(message, user_name)


@bot.message_handler(func=lambda message: message.text == 'Зарегистрироваться')
def proc_reg(message):
    chat_id = message.chat.id
    status = check_reg(chat_id)
    print(status)
    if status == None:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()

        cur.execute("INSERT INTO users2 (chat_id, first_name, last_name, admin) VALUES ('%s', '%s', '%s', '%s')" % (
            chat_id, first_name, last_name, 1))
        conn.commit()
        cur.close()
        conn.close()
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text="Вернуться", callback_data="return")
        markup.add(button_return)
        bot.send_message(message.chat.id,
                         "Вы успешно зарегистрированы. Нажмите кнопку, чтобы вернуться на экран авторизации",
                         reply_markup=markup)
        return
    if status[0] == chat_id:
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text="Вернуться", callback_data="return")
        markup.add(button_return)
        bot.send_message(message.chat.id, "Вы уже зарегистрированы", reply_markup=markup)
        return
    else:
        pass
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users2 (chat_id, first_name, last_name, admin) VALUES ('%s', '%s', '%s', '%s')" % (
        chat_id, first_name, last_name, 1))
    conn.commit()
    cur.close()
    conn.close()

    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='users'))
    # bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    # bot.register_next_step_handler(message, start)
    markup = telebot.types.InlineKeyboardMarkup()
    button_return = telebot.types.InlineKeyboardButton(text="Вернуться", callback_data="return")
    markup.add(button_return)
    bot.send_message(message.chat.id,
                     "Вы успешно зарегистрированы. Нажмите кнопку, чтобы вернуться на экран авторизации",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data == 'return')
def return_to_menu(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    start(call.message)


@bot.message_handler(func=lambda message: message.text == 'Продолжить')
def handle_login(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    chat_id = message.chat.id
    telebot.types.ReplyKeyboardRemove()
    admin = check_admin(chat_id)
    if admin[0] == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        item1 = telebot.types.InlineKeyboardButton('Продолжить ', callback_data='con_user')
        markup.add(item1)
        bot.reply_to(message, "Вы продолжите как сотрудник", reply_markup=markup)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        item1 = telebot.types.InlineKeyboardButton('Продолжить ', callback_data='con_admin')
        markup.add(item1)
        bot.reply_to(message, "Вы продолжите как руководитель", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data == 'con_admin')
def con_admin(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    chat_id = call.message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        # item1 = telebot.types.InlineKeyboardButton('Создать опрос', callback_data='survey')
        item1 = telebot.types.KeyboardButton('Создать опрос')
        item2 = telebot.types.KeyboardButton('Удалить опрос')
        item4 = telebot.types.KeyboardButton('Список пользователей')
        item3 = telebot.types.KeyboardButton('Редактировать опрос')
        item5 = telebot.types.KeyboardButton('Получить отчет')
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(call.message.chat.id, "Что хотите сделать, руководитель?", reply_markup=markup)
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS survey (id INTEGER NOT NULL, survey_name varchar(100), PRIMARY KEY(id AUTOINCREMENT))')
        conn.commit()
        cur.close()
        conn.close()
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


@bot.message_handler(func=lambda message: message.text == 'Список пользователей')
# @bot.callback_query_handler(func=lambda c: c.data == 'button3')
def list1(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users2')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'Имя: {el[2]}, Фамилия: {el[3]}, уровень доступа: {el[4]}\n'

        cur.close()
        conn.close()

        bot.send_message(message.chat.id, info)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


@bot.message_handler(func=lambda message: message.text == 'Пройти опрос')
def opros(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 0:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS survey_answers (id INTEGER NOT NULL, id_survey INTEGER NOT NULL, chat_id INTEGER, question_text varchar(100), question_answer "
            f"varchar(100), FOREIGN KEY (id_survey) REFERENCES survey (id), FOREIGN KEY (question_text) REFERENCES survey_questions (question_text), FOREIGN KEY (chat_id) REFERENCES user2 (chat_id), PRIMARY KEY(id AUTOINCREMENT))")
        conn.commit()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        cur.execute('SELECT id, survey_name FROM survey')
        surveys = cur.fetchall()
        for survey in surveys:
            button = telebot.types.KeyboardButton(survey[1])
            markup.add(button)
        a = bot.send_message(message.chat.id, "Выберите опрос:", reply_markup=markup)
        cur.close()
        conn.close()
        bot.register_next_step_handler(a, test)
    # for a in surveys:
    # if a == surveys:
    # bot.register_next_step_handler(a, test)
    # print(a)
    else:
        bot.send_message(chat_id, 'Опрос проходите не Вы, а сотрудники')


def test(message):
    # global current_question
    # global col_questions
    # global sn
    # global survey_id
    chat_id = message.chat.id
    opr = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT id FROM survey WHERE survey_name=?', (opr,))
    survey_id = cur.fetchone()
    if not survey_id:
        bot.send_message(message.chat.id, "Введите заново название опроса:")
        bot.register_next_step_handler(message, test)  # Регистрация обработчика для нового ввода
        return
    survey_id = survey_id[0]

    cur.execute('SELECT id, question_text FROM survey_questions WHERE id_survey=?', (survey_id,))
    questions = cur.fetchall()
    cur.close()
    conn.close()

    if not questions:
        bot.send_message(message.chat.id, "У данного опроса нет вопросов.")
        return

    # current_question = 1
    # col_questions = len(questions)
    # sn = questions
    user_state = get_user_state(chat_id)
    user_state.survey_id = survey_id
    user_state.current_question = 0
    user_state.col_questions = len(questions)
    user_state.questions = questions
    bot.send_message(message.chat.id, "Начнем проходить опрос.", reply_markup=telebot.types.ReplyKeyboardRemove())
    #ask_question(message.chat.id, sn[current_question - 1])
    ask_question(chat_id, questions[0])
    # global current_question
    # global col_questions
    # global sn
    # global ii
    # markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # item1 = telebot.types.KeyboardButton('')
    # markup2.add(item1)
    #
    #
    # opr = message.text
    # conn = sqlite3.connect('users2.sql')
    # cur = conn.cursor()
    # cur.execute('SELECT id FROM survey WHERE survey_name=?', (opr,))
    # opr1 = cur.fetchone()
    # try:
    #     cur.execute('SELECT id_survey, question_text FROM survey_questions WHERE id_survey=?', opr1)
    # except:
    #
    #     bot.send_message(message.chat.id, "Введите заново название опроса:")
    #     bot.register_next_step_handler(message, test)  # Регистрация обработчика для нового ввода
    #     return  # Завершаем выполнение текущего вызова функции
    # opr2 = cur.fetchall()
    # cur.execute('SELECT question_text FROM survey_questions WHERE id_survey=?', opr1)
    # opr3 = cur.fetchall()
    # print(opr2)
    # print(opr3)
    # cur.close()
    # conn.close()
    # current_question = 1
    # col_questions = len(opr2)
    # print(col_questions)
    # sn = opr3
    # print(sn)
    # bot.send_message(message.chat.id, "Начнем проходить опрос. Отвечате 'Да' или 'Нет'",
    #                  reply_markup=telebot.types.ReplyKeyboardRemove())
    # bot.send_message(message.chat.id, f"{current_question} вопрос: {sn[0][0]}")
    # bot.register_next_step_handler(message, save_to_db_answer)
def ask_question(chat_id, question):
    user_state = get_user_state(chat_id)
    question_id, question_text = question
    current_question_number = user_state.current_question + 1
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT option_text FROM survey_options WHERE id_question=?', (question_id,))
    options = cur.fetchall()
    cur.close()
    conn.close()

    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for option in options:
        button = telebot.types.KeyboardButton(option[0])
        markup.add(button)

    #bot.send_message(chat_id, f"{current_question} вопрос: {question_text}", reply_markup=markup)
    bot.send_message(chat_id, f"{current_question_number} вопрос: {question[1]}", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(chat_id, save_to_db_answer)
def save_to_db_answer(message):
    text = message.text
    chat_id = message.chat.id
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    user_state = get_user_state(chat_id)
    # global current_question
    # global col_questions
    # global sn
    # global survey_id

    #cur.execute("INSERT INTO survey_answers (id_survey, question_text, chat_id, question_answer) VALUES (?, ?, ?, ?)",
                #(survey_id, sn[current_question - 1][1], chat_id, text))
    cur.execute("INSERT INTO survey_answers (id_survey, question_text, chat_id, question_answer) VALUES (?, ?, ?, ?)",
                (user_state.survey_id, user_state.questions[user_state.current_question][0], chat_id, text))
    conn.commit()
    cur.close()
    conn.close()
    user_state.current_question += 1
    if user_state.current_question < user_state.col_questions:
        ask_question(chat_id, user_state.questions[user_state.current_question])
    else:
        #bot.send_message(chat_id, "Опрос пройден", reply_markup=telebot.types.ReplyKeyboardRemove())
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам юзера', callback_data='con_user')
        markup.add(button_return)
        bot.send_message(chat_id, "Опрос пройден", reply_markup=markup)
        del user_states[chat_id]
    # current_question += 1
    # if current_question <= col_questions:
    #     ask_question(chat_id, sn[current_question - 1])
    # else:
    #     current_question = None
    #     col_questions = None
    #     sn = None
    #     survey_id = None
    #     markup = telebot.types.InlineKeyboardMarkup()
    #     button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам юзера', callback_data='con_user')
    #     markup.add(button_return)
    #     bot.send_message(chat_id, "Опрос пройден", reply_markup=markup)
    #     telebot.types.ReplyKeyboardRemove()
    #text = message.text
    #chat_id = message.chat.id
    #conn = sqlite3.connect('users2.sql')
    #cur = conn.cursor()
    #global ii
    #global iii
    #global sn
    #ii = 0
    #print(sn)
    #cur.execute("SELECT question_text FROM survey_questions WHERE question_text='%s'" % sn[ii][0])
    #que = cur.fetchall()
    #print(que)
    #cur.execute("SELECT id_survey FROM survey_questions WHERE question_text='%s'" % sn[ii][0])
    #ii += 1
    #iii = 0
    #id_survey = cur.fetchone()
    #conn.commit()
    #cur.close()
    #conn.close()
    #conn = sqlite3.connect('users2.sql')
    #cur = conn.cursor()
    #if id_survey is not None:
        #cur.execute("INSERT INTO survey_answers (id_survey, question_text, chat_id, question_answer) VALUES ('%s', '%s', '%s', '%s')" % (id_survey[0], que[0][0], chat_id, text))
        #conn.commit()
        #iii += 1
    #else:
        #bot.send_message(message.chat.id, "Вопросов у опроса нет")
        #return
    #cur.close()
    #conn.close()
    #global current_question
    #global col_questions
    #current_question += 1
    #if current_question <= col_questions and ii != col_questions:
        #bot.send_message(message.chat.id, f"{current_question} вопрос: {sn[current_question-1][0]}")
        #bot.register_next_step_handler(message, save_to_db_answer)
    #else:
        #current_question = None
        #col_questions = None
        #sn = None
        #ii = 0
        #iii = 0
        #markup = telebot.types.InlineKeyboardMarkup()
        #button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам юзера', callback_data='con_user')
        #markup.add(button_return)
        #bot.send_message(message.chat.id, "Опрос пройден", reply_markup=markup)
        #telebot.types.ReplyKeyboardRemove()

@bot.message_handler(func=lambda message: message.text == 'Создать опрос' and 'Вернуться на создание опроса')
# @bot.callback_query_handler(func=lambda c: c.data == 'survey')
def survey(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        bot.send_message(message.chat.id, 'Введите название опроса', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, nazv)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


def nazv(message):
    global sn
    # bot.register_next_step_handler(call.message, user_pass_reg)
    survey_name = message.text.strip()
    sn = survey_name
    chh = check_survey(survey_name)
    if chh:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_return = telebot.types.KeyboardButton(text='Вернуться на создание опроса')
        markup.add(button_return)
        bot.send_message(message.chat.id, 'Такое название уже есть', reply_markup=markup)
        return
    else:
        pass
    print(survey_name)
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS survey_questions (id INTEGER NOT NULL, id_survey INTEGER NOT NULL, question_text varchar(100), FOREIGN KEY (id_survey) REFERENCES survey (id), PRIMARY KEY(id AUTOINCREMENT))")
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS survey_options (id INTEGER PRIMARY KEY AUTOINCREMENT, id_survey INTEGER NOT NULL, id_question INTEGER NOT NULL, option_text varchar(100), FOREIGN KEY (id_survey) REFERENCES survey(id), FOREIGN KEY (id_question) REFERENCES survey_questions(id))")
    conn.commit()
    cur.close()
    conn.close()
    print(survey_name)
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO survey (survey_name) VALUES ('%s')" % (survey_name))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Введите количество вопросов')
    bot.register_next_step_handler(message, nazv1)


def nazv1(message):
    global current_question
    global col_questions
    try:
        col_questions = int(message.text.strip())
    except ValueError:
        markup1 = telebot.types.InlineKeyboardMarkup()
        item1 = telebot.types.InlineKeyboardButton('Вернуться на создание опроса', callback_data='con_admin')
        markup1.add(item1)
        bot.send_message(message.chat.id, 'Неверно указано количество', reply_markup=markup1)
        bot.register_next_step_handler(message, survey)
        return

    print(col_questions)
    current_question = 1
    bot.send_message(message.chat.id, f"{current_question} вопрос:")
    bot.register_next_step_handler(message, save_to_db)


def save_to_db(message):
    global sn, current_question, col_questions
    question_text = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", (sn,))
    id_survey = cur.fetchone()[0]
    cur.execute("INSERT INTO survey_questions (id_survey, question_text) VALUES (?, ?)", (id_survey, question_text))
    id_question = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Введите количество вариантов ответа для этого вопроса')
    bot.register_next_step_handler(message, get_number_of_options, id_survey, id_question)
    #global current_question
    #global col_questions
    #current_question += 1
    #if current_question <= col_questions:
    #    bot.send_message(message.chat.id, f"{current_question} вопрос:")
    #    bot.register_next_step_handler(message, save_to_db)
    #else:
     #   current_question = None
      #  col_questions = None
       # sn = None
        #markup = telebot.types.InlineKeyboardMarkup()
        #button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
        #markup.add(button_return)
        #bot.send_message(message.chat.id, "Опрос создан", reply_markup=markup)
        #telebot.types.ReplyKeyboardRemove()

        # con_admin(call.message)

def get_number_of_options(message, id_survey, id_question):
    try:
        num_options = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверно указано количество вариантов ответа. Попробуйте снова.')
        bot.register_next_step_handler(message, get_number_of_options, id_survey, id_question)
        return

    bot.send_message(message.chat.id, f'Введите 1 вариант ответа:')
    bot.register_next_step_handler(message, save_options_to_db, id_survey, id_question, num_options, 1)

def save_options_to_db(message, id_survey, id_question, num_options, current_option):
    option_text = message.text.strip()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO survey_options (id_survey, id_question, option_text) VALUES (?, ?, ?)", (id_survey, id_question, option_text))
    conn.commit()
    cur.close()
    conn.close()

    if current_option < num_options:
        bot.send_message(message.chat.id, f'Введите {current_option + 1} вариант ответа:')
        bot.register_next_step_handler(message, save_options_to_db, id_survey, id_question, num_options, current_option + 1)
    else:
        global current_question, col_questions
        current_question += 1
        if current_question <= col_questions:
            bot.send_message(message.chat.id, f"{current_question} вопрос:")
            bot.register_next_step_handler(message, save_to_db)
        else:
            current_question = None
            col_questions = None
            sn = None
            markup = telebot.types.InlineKeyboardMarkup()
            button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
            markup.add(button_return)
            bot.send_message(message.chat.id, "Опрос создан", reply_markup=markup)
            telebot.types.ReplyKeyboardRemove()
@bot.message_handler(func=lambda message: message.text == 'Удалить опрос')
def delete(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute('SELECT id, survey_name FROM survey')
        surveys = cur.fetchall()
        markup=telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for survey in surveys:
            button = telebot.types.KeyboardButton(survey[1])
            markup.add(button)
        a = bot.send_message(message.chat.id, "Выберите опрос:", reply_markup=markup)
        cur.close()
        conn.close()
        bot.register_next_step_handler(a, test1)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')
def test1(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    opr111 = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", (opr111,))
    opr11 = cur.fetchone()
    print(opr11)
    try:
        cur.execute("DELETE FROM survey WHERE id=?", opr11)
    except:
        bot.send_message(message.chat.id, "Ошибка. Введите заново название опроса:")
        bot.register_next_step_handler(message, test1)
        return
    bot.send_message(message.chat.id, "Начнем удаление опроса",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    conn.commit()
    cur.execute("DELETE FROM survey_questions WHERE id_survey=?", opr11)
    conn.commit()
    cur.execute('DELETE FROM survey_answers WHERE id_survey=?', opr11)
    conn.commit()
    cur.execute('DELETE FROM survey_options WHERE id_survey=?', opr11)
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
    markup.add(button_return)
    bot.send_message(message.chat.id, "Опрос удален", reply_markup=markup)
    telebot.types.ReplyKeyboardRemove()

@bot.message_handler(func=lambda message: message.text == 'Редактировать опрос')
def survey_update(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        bot.send_message(message.chat.id, 'Введите название опроса', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, nazv_update)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


def nazv_update(message):
    global sn_update
    # bot.register_next_step_handler(call.message, user_pass_reg)
    survey_name = message.text.strip()
    sn_update = survey_name
    print(survey_name)
    bot.send_message(message.chat.id, 'Введите название нового опроса')
    bot.register_next_step_handler(message, update)
def update(message):
    global sn_update
    survey_name = message.text.strip()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("UPDATE survey SET survey_name=? WHERE survey_name=?", (survey_name, sn_update))
    conn.commit()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", (survey_name,))
    abc = cur.fetchone()
    try:
        cur.execute("SELECT * FROM survey_questions WHERE id_survey=?", abc)
    except:
        bot.send_message(message.chat.id, "Введите заново название опроса:")
        bot.register_next_step_handler(message, update)
        return
    abc1 = cur.fetchall()
    abc11 = len(abc1)
    cur.close()
    conn.close()
    sn_update = survey_name
    global current_question
    global col_questions
    try:
        col_questions = abc11
    except ValueError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_return = telebot.types.KeyboardButton(text='Редактировать опрос')
        markup.add(button_return)
        bot.send_message(message.chat.id, 'Неверно указано количество', reply_markup=markup)
        return

    print(col_questions)
    current_question = 1
    bot.send_message(message.chat.id, f"{current_question} вопрос:")
    bot.register_next_step_handler(message, save_to_db_update)


def save_to_db_update(message):
    global sn_update
    global col
    global col1
    text = message.text
    print(sn_update, 'Это сн апдейт в сэйв дб')
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", [sn_update])
    id_survey = cur.fetchone()
    print(id_survey, 'это айди сурви в сэйв дб')
    conn.commit()
    cur.close()
    conn.close()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM survey_questions WHERE id_survey=?", id_survey)
    idd = cur.fetchone()
    print(idd)
    print(col1, 'это col1')
    if col1 == 0:
        col = idd[0]
        i = col
    else:
        col = col1
        i = col1
    print(i, 'это aa')
    cur.execute("UPDATE survey_questions SET question_text=? WHERE id=? AND id_survey=?",  (text, i, id_survey[0]))
    conn.commit()
    col += 1
    col1 = col
    cur.close()
    conn.close()

    global current_question
    global col_questions
    current_question += 1
    if current_question <= col_questions:
        bot.send_message(message.chat.id, f"{current_question} вопрос:")
        bot.register_next_step_handler(message, save_to_db_update)
    else:
        current_question = None
        col_questions = None
        sn_update = None
        col = 0
        col1 = 0
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
        markup.add(button_return)
        bot.send_message(message.chat.id, "Опрос отредактирован", reply_markup=markup)
        telebot.types.ReplyKeyboardRemove()

        # con_admin(call.message)

@bot.callback_query_handler(func=lambda c: c.data == 'con_user')
def con_user(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    chat_id = call.message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 0:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        # item1 = telebot.types.InlineKeyboardButton('Создать опрос', callback_data='survey')
        item1 = telebot.types.KeyboardButton('Пройти опрос')
        markup.add(item1)
        bot.send_message(call.message.chat.id, "Выберете действие", reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Опрос проходите не Вы, а клиенты')


@bot.message_handler(func=lambda message: message.text == 'Получить отчет')
def handle_get_report(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT id, survey_name FROM survey')
    surveys = cur.fetchall()
    cur.close()
    conn.close()
    if status[0] == 1:
        if surveys:
            markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for survey in surveys:
                item = telebot.types.KeyboardButton(survey[1])
                markup.add(item)
            bot.send_message(chat_id, "Отчет на какой опрос вы хотите получить?", reply_markup=markup)
            bot.register_next_step_handler(message, handle_selected_survey_report)
        else:
            bot.send_message(chat_id, "Нет доступных опросов для отчета.")
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


# Обработчик выбора опроса
def handle_selected_survey_report(message):
    chat_id = message.chat.id
    survey_name = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT id FROM survey WHERE survey_name = ?', (survey_name,))
    survey_id = cur.fetchone()[0]

    generate_report(survey_id)
    cur.execute('SELECT image FROM images WHERE survey_id = ?', (survey_id,))
    image_blob = cur.fetchone()
    cur.close()
    conn.close()
    if image_blob is not None:
        # Сохраняем изображение временно
        with open('temp_survey_report.png', 'wb') as f:
            f.write(image_blob[0])

        # Отправляем изображение пользователю
        with open('temp_survey_report.png', 'rb') as f:
            bot.send_photo(chat_id, f)

        # Удаляем временное изображение
        os.remove('temp_survey_report.png')
    markup = telebot.types.InlineKeyboardMarkup()
    item1 = telebot.types.InlineKeyboardButton('Продолжить ', callback_data='con_admin')
    markup.add(item1)
    bot.reply_to(message, f"Отчет для опроса '{survey_name}' сгенерирован и отображен.", reply_markup=markup)

def is_survey_name(text):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT survey_name FROM survey')
    survey_names = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return text in survey_names


# Функции для анализа и визуализации данных
def get_survey_data(survey_id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT question_text FROM survey_questions WHERE id_survey = ?', (survey_id,))
    questions = [row[0] for row in cur.fetchall()]

    cur.execute('SELECT question_text, question_answer FROM survey_answers WHERE id_survey = ?', (survey_id,))
    responses = cur.fetchall()
    cur.close()
    conn.close()
    return questions, responses


def process_responses(responses):
    data = defaultdict(list)
    print(data)
    for question, answer in responses:
        data[question].append(answer)
    return data


def analyze_responses(data, questions):
    analysis_results = {}
    for question in questions:
        answers = data[question]
        answer_summary = {option: answers.count(option) for option in set(answers)}
        analysis_results[question] = answer_summary
    return analysis_results


def plot_analysis(analysis_results, survey_id):
    num_questions = len(analysis_results)
    plt.figure(figsize=(10, 6 * num_questions))

    for idx, (question, summary) in enumerate(analysis_results.items(), start=1):
        plt.subplot(num_questions, 1, idx)
        plt.bar(summary.keys(), summary.values(), color='blue')
        plt.title(question)
        plt.xlabel('Ответы')
        plt.ylabel('Количество')
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.show()
    image_binary = buffer.getvalue()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            survey_id INTEGER,
            image BLOB,
            FOREIGN KEY(survey_id) REFERENCES survey(id)
        )
    ''')
    cur.execute("INSERT INTO images (survey_id, image) VALUES (?, ?)", (survey_id, sqlite3.Binary(image_binary)))
    conn.commit()
    cur.close()
    conn.close()
    buffer.close()
def generate_report(survey_id):
    questions, responses = get_survey_data(survey_id)
    data = process_responses(responses)
    analysis_results = analyze_responses(data, questions)
    plot_analysis(analysis_results, survey_id)

bot.polling(none_stop=True)
