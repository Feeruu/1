import telebot
import sqlite3
bot = telebot.TeleBot('7082484484:AAGvOulj_lXSQO2fmklzUJMPM7_24tpWB70')
names = {}
admin = None
current_question = None
col_questions = None
sn = None
def check(username, password):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user
def check_admin(username, password):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("SELECT admin FROM users WHERE name=? AND pass=?", (username, password))
    admin = cur.fetchone()
    cur.close()
    conn.close()
    return admin
def check_survey(id):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("SELECT survey_name FROM survey WHERE survey_name=?", [id])
    ch = cur.fetchone()
    cur.close()
    conn.close()
    return ch

def check_prava(chat_id):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("SELECT admin FROM users WHERE chat_id=?", (chat_id,))
    status = cur.fetchone()
    cur.close()
    conn.close()
    return status


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL, chat_id INTEGER, name varchar(50), pass varchar(50), admin int, PRIMARY KEY(id AUTOINCREMENT))')
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    #item1 = telebot.types.InlineKeyboardButton('Войти', callback_data='button1')
    #item2 = telebot.types.InlineKeyboardButton('Зарегистрироваться', callback_data='button2')
    #item3 = telebot.types.InlineKeyboardButton('Список пользователей', callback_data='button3')
    item1 = telebot.types.KeyboardButton('Войти')
    item2 = telebot.types.KeyboardButton('Зарегистрироваться')
    item3 = telebot.types.KeyboardButton('Список пользователей')
    markup.add(item1, item2, item3)
    bot.reply_to(message, "Хотите войти или зарегистрироваться?", reply_markup=markup)
    # bot.send_message(message.chat.id, 'Для регистрации введите ваше имя')
    # bot.register_next_step_handler(message, user_name)

#@bot.callback_query_handler(func=lambda c: c.data == 'button1')
@bot.message_handler(func=lambda message: message.text == 'Войти')
def handle_login(message):
    markup2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('')
    markup2.add(item1)
    print(message.chat.id)
    bot.send_message(message.chat.id, 'Введите имя', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    name = message.text.strip()
    names[message.chat.id] = {'name': name}
    #password = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, proc)
def proc(message):
    password = message.text.strip()
    name = names[message.chat.id]['name']

    user = check(name, password)
    if user:
        admin = check_admin(name, password)
        if admin[0] == 0:
            markup = telebot.types.InlineKeyboardMarkup()
            item1 = telebot.types.InlineKeyboardButton('Продолжить', callback_data='con_user')
            markup.add(item1)
            bot.reply_to(message, "Вход выполнен успешно!", reply_markup=markup)
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            item1 = telebot.types.InlineKeyboardButton('Продолжить', callback_data='con_admin')
            markup.add(item1)
            bot.reply_to(message, "Вход выполнен успешно!", reply_markup=markup)
    else:
        bot.reply_to(message, "Неверное имя пользователя или пароль. Попробуйте снова")
        start(message)

@bot.message_handler(func=lambda message: message.text == 'Зарегистрироваться')
#@bot.callback_query_handler(func=lambda c: c.data == 'button2')
def handle_reg(message):
    bot.send_message(message.chat.id, 'Введите имя')
    bot.register_next_step_handler(message, user_pass_reg)

def user_pass_reg(message):
    name = message.text.strip()
    names[message.chat.id] = {'name': name}
    #password = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, proc_reg)
def proc_reg(message):
    password = message.text.strip()
    name = names[message.chat.id]['name']
    chat_id = message.chat.id
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (chat_id, name, pass, admin) VALUES ('%s', '%s', '%s', '%s')" % (chat_id, name, password, 1))
    conn.commit()
    cur.close()
    conn.close()

    #markup = telebot.types.InlineKeyboardMarkup()
    #markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='users'))
    #bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    #bot.register_next_step_handler(message, start)
    markup = telebot.types.InlineKeyboardMarkup()
    button_return = telebot.types.InlineKeyboardButton(text="Вернуться", callback_data="return")
    markup.add(button_return)
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы. Нажмите кнопку, чтобы вернуться на экран авторизации", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == 'return')
def return_to_menu(call):
    start(call.message)


@bot.callback_query_handler(func=lambda c: c.data == 'con_admin')
def con_admin(call):
    chat_id = call.message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        #item1 = telebot.types.InlineKeyboardButton('Создать опрос', callback_data='survey')
        item1 = telebot.types.KeyboardButton('Создать опрос')
        item2 = telebot.types.KeyboardButton('Список пользователей')
        markup.add(item1, item2)
        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=markup)
        conn = sqlite3.connect('users.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS survey (id INTEGER NOT NULL, survey_name varchar(100), PRIMARY KEY(id AUTOINCREMENT))')
        conn.commit()
        cur.close()
        conn.close()
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')


@bot.message_handler(func=lambda message: message.text == 'Список пользователей')
#@bot.callback_query_handler(func=lambda c: c.data == 'button3')
def list(message):
    chat_id = message.chat.id
    status = check_prava(chat_id)
    print(status)
    if status[0] == 1:
        conn = sqlite3.connect('users.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'Имя: {el[1]}, пароль: {el[2]}, уровень доступа: {el[3]}\n'

        cur.close()
        conn.close()

        bot.send_message(message.chat.id, info)
    else:
        bot.send_message(chat_id, 'У Вас недостаточно прав для этого действия')

@bot.message_handler(func=lambda message: message.text == 'Создать опрос' or 'Вернуться на создание опроса')
#@bot.callback_query_handler(func=lambda c: c.data == 'survey')
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
    #bot.register_next_step_handler(call.message, user_pass_reg)
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
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS survey_questions (id INTEGER NOT NULL, id_survey INTEGER NOT NULL, question_text varchar(100), FOREIGN KEY (id_survey) REFERENCES survey (id), PRIMARY KEY(id AUTOINCREMENT))")
    conn.commit()
    cur.close()
    conn.close()
    print(survey_name)
    conn = sqlite3.connect('users.sql')
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
    col_questions = int(message.text.strip())
    print(col_questions)
    current_question = 1
    bot.send_message(message.chat.id, f"{current_question} вопрос:")
    bot.register_next_step_handler(message, save_to_db)
def save_to_db(message):
    text = message.text
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM survey WHERE survey_name=?", [sn])
    id_survey = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO survey_questions (id_survey, question_text) VALUES ('%s', '%s')" % (id_survey[0], text))
    conn.commit()
    cur.close()
    conn.close()

    global current_question
    current_question += 1
    if current_question <= col_questions:
        bot.send_message(message.chat.id, f"{current_question} вопрос:")
        bot.register_next_step_handler(message, save_to_db)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        button_return = telebot.types.InlineKeyboardButton(text='Вернуться к командам', callback_data='con_admin')
        markup.add(button_return)
        bot.send_message(message.chat.id, "Опрос создан", reply_markup=markup)
        telebot.types.ReplyKeyboardRemove()

        #con_admin(call.message)

@bot.callback_query_handler(func=lambda c: c.data == 'con_user')
def con_user(call):
    bot.send_message(call.message.chat.id, "Вы юзер")

bot.polling(none_stop=True)