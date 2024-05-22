import os
import telebot
import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
import io

user_states = {}
user_states_update = {}


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


class UserStateUpdate:
    def __init__(self, survey_name, survey_id, current_question, col_questions, questions, current_option, col_options,
                 options):
        self.survey_name = survey_name
        self.survey_id = survey_id
        self.current_question = current_question
        self.col_questions = col_questions
        self.questions = questions
        self.current_option = current_option
        self.col_options = col_options
        self.options = options


def get_user_state_update(chat_id):
    if chat_id not in user_states_update:
        user_states_update[chat_id] = UserStateUpdate(None, None, 0, 0, [], 0, 0, [])
    return user_states_update[chat_id]


bot = telebot.TeleBot('7082484484:AAGvOulj_lXSQO2fmklzUJMPM7_24tpWB70')
names = {}

sn = None

sn_update = None


def check_survey(id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT survey_name FROM survey WHERE survey_name=?", [id])
    ch = cur.fetchone()
    cur.close()
    conn.close()
    return ch


def check_survey_id(id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT survey_name FROM survey WHERE id=?", [id])
    ch = cur.fetchone()
    cur.close()
    conn.close()
    return ch[0] if ch else None


def check_prava(chat_id):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT admin FROM users2 WHERE chat_id=?", (chat_id,))
    status = cur.fetchone()
    cur.close()
    conn.close()
    return status


def get_all_users():
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users2 WHERE admin=0")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [user[0] for user in users]


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
    item2 = telebot.types.KeyboardButton('Зарегистрироваться')
    item3 = telebot.types.KeyboardButton('Продолжить')
    markup.add(item2, item3)
    bot.reply_to(message, "Хотите зарегистрироваться или продолжить?", reply_markup=markup)


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
            chat_id, first_name, last_name, 0))
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
    status = check_prava(chat_id)
    if status[0] == 0:
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
    if status[0] == 2 or 1:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item1 = telebot.types.KeyboardButton('Создать опрос')
        item2 = telebot.types.KeyboardButton('Удалить опрос')
        item4 = telebot.types.KeyboardButton('Список пользователей')
        item3 = telebot.types.KeyboardButton('Редактировать опрос')
        item5 = telebot.types.KeyboardButton('Получить отчет')
        item6 = telebot.types.KeyboardButton('Изменить права доступа')
        item7 = telebot.types.KeyboardButton('Получить список отзывов')
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        if status[0] == 2:
            bot.send_message(call.message.chat.id, "Что хотите сделать, главный администратор?", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "Что хотите сделать, администратор?", reply_markup=markup)
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
def list_of_users(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 2 or 1:
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
    else:
        bot.send_message(chat_id, 'Опрос проходите не Вы, а сотрудники')


def test(message):
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

    user_state = get_user_state(chat_id)
    user_state.survey_id = survey_id
    user_state.current_question = 0
    user_state.col_questions = len(questions)
    user_state.questions = questions
    bot.send_message(message.chat.id, "Начнем проходить опрос.", reply_markup=telebot.types.ReplyKeyboardRemove())
    ask_question(chat_id, questions[0])


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

    bot.send_message(chat_id, f"{current_question_number} вопрос: {question[1]}", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(chat_id, save_to_db_answer)


def save_to_db_answer(message):
    text = message.text
    chat_id = message.chat.id
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    user_state = get_user_state(chat_id)

    cur.execute("SELECT question_text FROM survey_questions WHERE id=?",
                (user_state.questions[user_state.current_question][0],))
    question_text = cur.fetchone()[0]
    cur.execute("INSERT INTO survey_answers (id_survey, question_text, chat_id, question_answer) VALUES (?, ?, ?, ?)",
                (user_state.survey_id, question_text, chat_id, text))
    conn.commit()
    cur.close()
    conn.close()
    user_state.current_question += 1
    if user_state.current_question < user_state.col_questions:
        ask_question(chat_id, user_state.questions[user_state.current_question])
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам юзера', callback_data='con_user')
        markup.add(button_return)
        bot.send_message(chat_id, "Опрос пройден", reply_markup=markup)
        del user_states[chat_id]


@bot.message_handler(func=lambda message: message.text in ['Создать опрос', 'Вернуться на создание опроса'])
def survey(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1 or 2:
        bot.send_message(message.chat.id, 'Введите название опроса', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, nazv)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


def nazv(message):
    global sn
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
        bot.send_message(message.chat.id, f'Название опроса "{survey_name}" принято.')
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS survey_questions (id INTEGER NOT NULL, id_survey INTEGER NOT NULL, question_text varchar(100), FOREIGN KEY (id_survey) REFERENCES survey (id), PRIMARY KEY(id AUTOINCREMENT))")
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS survey_options (id INTEGER PRIMARY KEY AUTOINCREMENT, id_survey INTEGER NOT NULL, id_question INTEGER NOT NULL, option_text varchar(100), FOREIGN KEY (id_survey) REFERENCES survey(id), FOREIGN KEY (id_question) REFERENCES survey_questions(id))")
        conn.commit()
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
    cur.execute("INSERT INTO survey_options (id_survey, id_question, option_text) VALUES (?, ?, ?)",
                (id_survey, id_question, option_text))
    conn.commit()
    cur.close()
    conn.close()

    if current_option < num_options:
        bot.send_message(message.chat.id, f'Введите {current_option + 1} вариант ответа:')
        bot.register_next_step_handler(message, save_options_to_db, id_survey, id_question, num_options,
                                       current_option + 1)
    else:
        global current_question, col_questions
        current_question += 1
        if current_question <= col_questions:
            bot.send_message(message.chat.id, f"{current_question} вопрос:")
            bot.register_next_step_handler(message, save_to_db)
        else:
            current_question = None
            col_questions = None

            markup = telebot.types.InlineKeyboardMarkup()
            button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
            markup.add(button_return)
            users = get_all_users()
            for user in users:
                bot.send_message(user, f'Новый опрос "{check_survey_id(id_survey)}" создан. Пожалуйста, пройдите его.')
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
    if status[0] == 1 or 2:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute('SELECT id, survey_name FROM survey')
        surveys = cur.fetchall()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
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
    chat_id = message.chat.id
    status = check_prava(chat_id)
    if status[0] == 1 or 2:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute('SELECT id, survey_name FROM survey')
        surveys = cur.fetchall()
        cur.close()
        conn.close()

        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for survey in surveys:
            markup.add(telebot.types.KeyboardButton(survey[1]))
        bot.send_message(message.chat.id, 'Выберите название опроса', reply_markup=markup)
        bot.register_next_step_handler(message, nazv_update)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


def nazv_update(message):
    chat_id = message.chat.id
    survey_name = message.text.strip()
    user_state = get_user_state_update(chat_id)
    user_state.survey_name = survey_name

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", (survey_name,))
    survey_id = cur.fetchone()

    if not survey_id:
        bot.send_message(chat_id, "Такого опроса не существует. Попробуйте снова.")
        bot.register_next_step_handler(message, nazv_update)
        return

    user_state.survey_id = survey_id[0]
    cur.execute("SELECT id, question_text FROM survey_questions WHERE id_survey=?", (survey_id[0],))
    questions = cur.fetchall()
    user_state.questions = questions
    user_state.col_questions = len(questions)

    cur.close()
    conn.close()

    bot.send_message(chat_id, 'Введите новое название опроса')
    bot.register_next_step_handler(message, update_survey_name)


def update_survey_name(message):
    chat_id = message.chat.id
    new_survey_name = message.text.strip()
    user_state = get_user_state_update(chat_id)

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("UPDATE survey SET survey_name=? WHERE id=?", (new_survey_name, user_state.survey_id))
    conn.commit()
    cur.close()
    conn.close()

    user_state.survey_name = new_survey_name
    bot.send_message(chat_id, 'Введите новое количество вопросов')
    bot.register_next_step_handler(message, update_question_count)


def update_question_count(message):
    chat_id = message.chat.id
    user_state = get_user_state_update(chat_id)

    try:
        new_question_count = int(message.text.strip())
        if new_question_count < 0:
            raise ValueError("Количество вопросов должно быть положительным числом.")
    except ValueError:
        bot.send_message(chat_id, 'Неверное количество. Попробуйте снова.')
        bot.register_next_step_handler(message, update_question_count)
        return

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()

    if new_question_count > user_state.col_questions:
        for _ in range(new_question_count - user_state.col_questions):
            cur.execute("INSERT INTO survey_questions (id_survey, question_text) VALUES (?, ?)",
                        (user_state.survey_id, ''))
    elif new_question_count < user_state.col_questions:
        cur.execute("DELETE FROM survey_questions WHERE id_survey=? ORDER BY id DESC LIMIT ?",
                    (user_state.survey_id, user_state.col_questions - new_question_count))

    conn.commit()
    cur.execute("SELECT id, question_text FROM survey_questions WHERE id_survey=?", (user_state.survey_id,))
    user_state.questions = cur.fetchall()
    user_state.col_questions = new_question_count

    cur.close()
    conn.close()

    user_state.current_question = 0
    ask_update_question(chat_id)


def ask_update_question(chat_id):
    user_state = get_user_state_update(chat_id)
    if user_state.current_question < user_state.col_questions:
        question_text = user_state.questions[user_state.current_question][1]
        bot.send_message(chat_id,
                         f"{user_state.current_question + 1} вопрос: {question_text}\nВведите новый текст вопроса:")
        bot.register_next_step_handler_by_chat_id(chat_id, update_question_text)
    else:
        user_state.current_question = 0
        user_state.current_option = 0
        ask_update_options(chat_id)


def update_question_text(message):
    chat_id = message.chat.id
    new_question_text = message.text.strip()
    user_state = get_user_state_update(chat_id)

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    question_id = user_state.questions[user_state.current_question][0]
    cur.execute("UPDATE survey_questions SET question_text=? WHERE id=?", (new_question_text, question_id))
    conn.commit()
    cur.close()
    conn.close()

    user_state.questions[user_state.current_question] = (question_id, new_question_text)
    user_state.current_question += 1

    ask_update_question(chat_id)


def ask_update_options(chat_id):
    user_state = get_user_state_update(chat_id)
    if user_state.current_question < user_state.col_questions:
        question_text = user_state.questions[user_state.current_question][1]
        question_id = user_state.questions[user_state.current_question][0]
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute('SELECT option_text FROM survey_options WHERE id_question = ? AND id_survey = ?',
                    (question_id, user_state.survey_id))
        options = cur.fetchall()
        user_state.options = options
        user_state.col_options = len(options)
        cur.close()
        conn.close()

        if user_state.col_options > 0:
            bot.send_message(chat_id, f"Введите количество новых вариантов ответа для вопроса '{question_text}'")
            bot.register_next_step_handler_by_chat_id(chat_id, get_new_options_count)
        else:
            bot.send_message(chat_id, f"Введите количество вариантов ответа для вопроса '{question_text}'")
            bot.register_next_step_handler_by_chat_id(chat_id, get_new_options_count)
    else:
        finalize_update(chat_id)


def get_new_options_count(message):
    chat_id = message.chat.id
    user_state = get_user_state_update(chat_id)
    try:
        user_state.col_options = int(message.text.strip())
    except ValueError:
        bot.send_message(chat_id, 'Неверное количество. Попробуйте снова.')
        bot.register_next_step_handler(message, get_new_options_count)
        return

    user_state.current_option = 0
    ask_new_option_text(chat_id)


def ask_new_option_text(chat_id):
    user_state = get_user_state_update(chat_id)
    question_text = user_state.questions[user_state.current_question][1]
    bot.send_message(chat_id,
                     f"Введите новый текст {user_state.current_option + 1}-го варианта ответа для вопроса '{question_text}':")
    bot.register_next_step_handler_by_chat_id(chat_id, save_new_option)


def save_new_option(message):
    chat_id = message.chat.id
    new_option_text = message.text.strip()
    user_state = get_user_state_update(chat_id)

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    question_id = user_state.questions[user_state.current_question][0]
    cur.execute("INSERT INTO survey_options (id_survey, id_question, option_text) VALUES (?, ?, ?)",
                (user_state.survey_id, question_id, new_option_text))
    conn.commit()
    cur.close()
    conn.close()

    user_state.current_option += 1

    if user_state.current_option < user_state.col_options:
        ask_new_option_text(chat_id)
    else:
        user_state.current_question += 1
        ask_update_options(chat_id)


def update_option_text(message):
    chat_id = message.chat.id
    new_option_text = message.text.strip()
    user_state = get_user_state_update(chat_id)

    if user_state.current_option < len(user_state.options):
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        question_id = user_state.questions[user_state.current_question][0]
        option_text = user_state.options[user_state.current_option][0]
        cur.execute("UPDATE survey_options SET option_text=? WHERE id_survey=? AND id_question=? AND option_text=?",
                    (new_option_text, user_state.survey_id, question_id, option_text))
        conn.commit()
        cur.close()
        conn.close()

    user_state.current_option += 1

    if user_state.current_option < user_state.col_options:
        bot.send_message(chat_id,
                         f"Введите новый текст {user_state.current_option + 1}-го варианта ответа для вопроса '{user_state.questions[user_state.current_question][1]}':")
        bot.register_next_step_handler_by_chat_id(chat_id, update_option_text)
    else:
        user_state.current_question += 1
        user_state.current_option = 0
        ask_update_options(chat_id)


def finalize_update(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
    markup.add(button_return)
    bot.send_message(chat_id, "Опрос отредактирован", reply_markup=markup)
    del user_states_update[chat_id]


@bot.callback_query_handler(func=lambda c: c.data == 'con_user')
def con_user(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    chat_id = call.message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 0:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item1 = telebot.types.KeyboardButton('Пройти опрос')
        item2 = telebot.types.KeyboardButton('Отправить отзыв')
        markup.add(item1, item2)
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


def handle_selected_survey_report(message):
    chat_id = message.chat.id
    survey_name = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT id FROM survey WHERE survey_name = ?', (survey_name,))
    survey_id = cur.fetchone()[0]

    generate_report(survey_id)
    cur.execute('SELECT image FROM images WHERE survey_id = ? ORDER BY created_at DESC LIMIT 1', (survey_id,))
    image_blob = cur.fetchone()
    cur.close()
    conn.close()
    if image_blob is not None:
        with open('temp_survey_report.png', 'wb') as f:
            f.write(image_blob[0])

        with open('temp_survey_report.png', 'rb') as f:
            bot.send_photo(chat_id, f)

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
    image_binary = buffer.getvalue()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            survey_id INTEGER,
            image BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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


@bot.message_handler(func=lambda message: message.text == 'Изменить права доступа')
def change_user_access(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    if status[0] == 2:
        conn = sqlite3.connect('users2.sql')
        cur = conn.cursor()
        cur.execute("SELECT id, chat_id, first_name, last_name, admin FROM users2 WHERE admin IN (0, 1)")
        users = cur.fetchall()
        cur.close()
        conn.close()

        if users:
            markup = telebot.types.InlineKeyboardMarkup()
            for user in users:
                user_id, user_chat_id, first_name, last_name, user_status = user
                button_text = f"{first_name} {last_name} (ID: {user_chat_id}) | Статус: {user_status}"
                callback_data = f"change_status:{user_id}:{user_status}"
                button = telebot.types.InlineKeyboardButton(button_text, callback_data=callback_data)
                markup.add(button)
            button_return = telebot.types.InlineKeyboardButton('Вернуться к командам', callback_data='con_admin')
            markup.add(button_return)
            bot.send_message(chat_id, "Выберите пользователя для изменения прав доступа:", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Нет доступных пользователей для изменения прав доступа.")
    else:
        bot.send_message(chat_id, "У вас недостаточно прав для этого действия.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_status:'))
def handle_change_status(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    user_id = int(data[1])
    current_status = int(data[2])
    new_status = 1 if current_status == 0 else 0

    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users2 SET admin=? WHERE id=?", (new_status, user_id))
    conn.commit()
    cur.close()
    conn.close()

    bot.answer_callback_query(call.id, "Права доступа обновлены.")
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Права доступа обновлены.")
    change_user_access(call.message)


def add_feedback(feedback_text):
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS feedback (id INTEGER NOT NULL, text varchar(100), PRIMARY KEY(id AUTOINCREMENT))")
    cur.execute("INSERT INTO feedback (text) VALUES (?)", (feedback_text,))
    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'Отправить отзыв')
def send_feedback(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваш отзыв:")
    bot.register_next_step_handler(message, receive_feedback)


def receive_feedback(message):
    feedback_text = message.text
    add_feedback(feedback_text)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")


@bot.message_handler(func=lambda message: message.text == 'Получить список отзывов')
def view_feedback(message):
    user_status = check_prava(message.chat.id)
    if user_status and user_status[0] == 1:
        feedbacks = get_all_feedbacks()
        if feedbacks:
            feedback_messages = "\n\n".join([f"{i + 1}. {fb[0]}" for i, fb in enumerate(feedbacks)])
            bot.send_message(message.chat.id, f"Отзывы:\n\n{feedback_messages}")
        else:
            bot.send_message(message.chat.id, "Нет отзывов.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для просмотра отзывов.")


def get_all_feedbacks():
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT text FROM feedback")
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()
    return feedbacks


bot.polling(none_stop=True)
