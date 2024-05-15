import telebot
import sqlite3

bot = telebot.TeleBot('7082484484:AAGvOulj_lXSQO2fmklzUJMPM7_24tpWB70')
names = {}
admin = None
current_question = None
col_questions = None
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
        markup.add(item1, item2, item3, item4)
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
def list(message):
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
    global current_question
    global col_questions
    global sn
    global ii
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    bot.send_message(message.chat.id, "Начнем проходить опрос. Отвечате 'Да' или 'Нет'", reply_markup=telebot.types.ReplyKeyboardRemove())
    opr = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute('SELECT id FROM survey WHERE survey_name=?', (opr,))
    opr1 = cur.fetchone()
    cur.execute('SELECT id_survey, question_text FROM survey_questions WHERE id_survey=?', opr1)
    opr2 = cur.fetchall()
    cur.execute('SELECT question_text FROM survey_questions WHERE id_survey=?', opr1)
    opr3 = cur.fetchall()
    print(opr2)
    print(opr3)
    cur.close()
    conn.close()
    current_question = 1
    col_questions = len(opr2)
    print(col_questions)
    sn = opr3
    print(sn)
    bot.send_message(message.chat.id, f"{current_question} вопрос: {sn[0][0]}")
    bot.register_next_step_handler(message, save_to_db_answer)
def save_to_db_answer(message):
    text = message.text
    chat_id = message.chat.id
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    global ii
    global iii
    global sn
    #ii = 0
    print(sn)
    cur.execute("SELECT question_text FROM survey_questions WHERE question_text='%s'" % sn[ii][0])
    que = cur.fetchall()
    print(que)
    cur.execute("SELECT id_survey FROM survey_questions WHERE question_text='%s'" % sn[ii][0])
    ii += 1
    #iii = 0
    id_survey = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    if id_survey is not None:
        cur.execute("INSERT INTO survey_answers (id_survey, question_text, chat_id, question_answer) VALUES ('%s', '%s', '%s', '%s')" % (id_survey[0], que[0][0], chat_id, text))
        conn.commit()
        iii += 1
    else:
        bot.send_message(message.chat.id, "Вопросов у опроса нет")
        return
    cur.close()
    conn.close()
    global current_question
    global col_questions
    current_question += 1
    if current_question <= col_questions and ii != col_questions:
        bot.send_message(message.chat.id, f"{current_question} вопрос: {sn[current_question-1][0]}")
        bot.register_next_step_handler(message, save_to_db_answer)
    else:
        current_question = None
        col_questions = None
        sn = None
        ii = 0
        iii = 0
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам юзера', callback_data='con_user')
        markup.add(button_return)
        bot.send_message(message.chat.id, "Опрос пройден", reply_markup=markup)
        telebot.types.ReplyKeyboardRemove()

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
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_return = telebot.types.KeyboardButton(text='Вернуться на создание опроса')
        markup.add(button_return)
        bot.send_message(message.chat.id, 'Неверно указано количество', reply_markup=markup)
        return

    print(col_questions)
    current_question = 1
    bot.send_message(message.chat.id, f"{current_question} вопрос:")
    bot.register_next_step_handler(message, save_to_db)


def save_to_db(message):
    global sn
    text = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", [sn])
    id_survey = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO survey_questions (id_survey, question_text) VALUES ('%s', '%s')" % (id_survey[0], text))
    conn.commit()
    cur.close()
    conn.close()

    global current_question
    global col_questions
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

        # con_admin(call.message)

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
    bot.send_message(message.chat.id, "Начнем удаление опроса",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    opr111 = message.text
    conn = sqlite3.connect('users2.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", (opr111,))
    opr11 = cur.fetchone()
    print(opr11)
    cur.execute("DELETE FROM survey WHERE id=?", opr11)
    conn.commit()
    cur.execute("DELETE FROM survey_questions WHERE id_survey=?", opr11)
    conn.commit()
    cur.execute('DELETE FROM survey_answers WHERE id_survey=?', opr11)
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
    cur.execute("SELECT * FROM survey_questions WHERE id_survey=?", abc)
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
        bot.send_message(call.message.chat.id, "Что хотите сделать, пользователь?", reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Опрос проходите не Вы, а сотрудники')


bot.polling(none_stop=True)
