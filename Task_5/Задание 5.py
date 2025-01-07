from random import choice
import telebot

# Укажите ваш токен
token = '' 

bot = telebot.TeleBot(token)

RANDOM_TASKS = [
    'Написать Гвидо письмо', 
    'Выучить Python', 
    'Записаться на курс в Нетологию', 
    'Посмотреть 4 сезон Рик и Морти'
]

todos = dict()

HELP = '''
Список доступных команд:
* /print  - напечатать все задачи на заданную дату
* /add - добавить задачу
* /random - добавить на сегодня случайную задачу
* /help - Напечатать help
'''

def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['random'])
def random_command(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на сегодня')

@bot.message_handler(commands=['add'])
def add_command(message):
    try:
        _, date, tail = message.text.split(maxsplit=2)
        task = tail  # Упрощение: task уже содержит всю строку после date
        if len(task) < 3:
            bot.send_message(message.chat.id, 'Задачи должны быть больше 3х символов')
        else:
            add_todo(date, task)
            bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}')
    except ValueError:
        bot.send_message(message.chat.id, 'Используйте формат: /add ДАТА ЗАДАЧА')

@bot.message_handler(commands=['print'])
def print_command(message):
    try:
        date = message.text.split(maxsplit=1)[1].lower()  # Изменено для получения только одной даты
        tasks = todos.get(date)
        response = f'{date}: \n' if tasks else f'Нет задач на {date}\n'
        if tasks:
            for task in tasks:
                response += f'[ ] {task}\n'
        bot.send_message(message.chat.id, response)
    except IndexError:
        bot.send_message(message.chat.id, 'Укажите дату для печати задач: /print ДАТА')

# Запуск бота
bot.polling(none_stop=True)
