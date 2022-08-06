import telebot
from telebot import types
import requests
import random
from bs4 import BeautifulSoup as b

bot = telebot.TeleBot('5433415893:AAHK6GBetdPstASvZyEh1aSvpT7vqFvcnr0')
url = 'https://www.anekdot.ru/release/anekdot/day/'
url2 = 'https://habr.com/ru/news/'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anecdotes = soup.find_all('div', class_='text')
    return [c.text for c in anecdotes]

list_of_jokes = parser(url)
random.shuffle(list_of_jokes)

def parser2(url2):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    news = soup.find_all('span', class_='text')
    return [c.text for c in news]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    yes = types.KeyboardButton('Да')
    markup.add(yes)
    bot.send_message(message.chat.id, 'Привет, бот-вафля на связи! Чем я могу тебе помочь? Я пока не понимаю '
                                      'язык людей, так что тебе придётся использовать кнопки и команды. Are you '
                                      'ready? Тогда быстрее жми на кнопку! ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choosing_action(message):
    if message.text == 'Да':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        joke = types.KeyboardButton('Анекдот')
        spamming = types.KeyboardButton('Спам')
        news = types.KeyboardButton('Новости')
        markup.add(joke, spamming, news)
        bot.send_message(message.chat.id, 'Отлично! Выбирай, чем я тебе могу помочь!',
                         reply_markup=markup)
        bot.register_next_step_handler(message, two_actions)

    else:
        bot.send_message(message.chat.id, 'Ну я же говорил, что я пока что глупенький и не понимаю человеческий язык! '
                                          'Нажми конпку "Да" внизу, чтобы начать!')


@bot.message_handler(content_types=['text'])
def two_actions(message):
    if message.text == 'Анекдот':
        jokes_proc(message)
    elif message.text == 'Спам':
        spam_buttons(message)
        bot.register_next_step_handler(message, spam)
    elif message.text == 'Новости':
        news(message)


@bot.message_handler(content_types=['text'])
def jokes_proc(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    joke = types.KeyboardButton('Загружай!')
    back = types.KeyboardButton('Назад')
    markup.add(joke, back)
    bot.send_message(message.chat.id, 'Хочешь развлечься анекдотами?', reply_markup=markup)
    bot.register_next_step_handler(message, pip)


@bot.message_handler(content_types=['text'])
def pip(message):
    if message.text == 'Загружай!':
        jokes(message)
    elif message.text == 'Назад':
        message.text = 'Да'
        choosing_action(message)


@bot.message_handler(content_types=['text'])
def jokes(message):
    bot.send_message(message.chat.id, list_of_jokes[0])
    del list_of_jokes[0]
    jokes_proc(message)


@bot.message_handler(content_types=['text'])
def spam_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    matvey = types.KeyboardButton('Матвей')
    vova = types.KeyboardButton('Вова')
    prokhor = types.KeyboardButton('Прохор')
    vasya = types.KeyboardButton('Вася')
    dima = types.KeyboardButton('Дима')
    back = types.KeyboardButton('Назад')
    markup.add(matvey, vova, prokhor, vasya, dima, back)

    bot.send_message(message.chat.id, 'Кто-то не отвечает тебе? Давай разберёмся! Кто посмел тебя игнорировать? '
                                      'Выбирай скорее!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def spam(message):
    markup = types.ReplyKeyboardMarkup()
    if message.text == 'Назад':
        message.text = 'Да'
        choosing_action(message)

    else:
        for i in range(0, 10):
            if message.text == 'Матвей':
                bot.send_message(message.chat.id, '@DrFobosser, выйди на связь!', reply_markup=markup)
            elif message.text == 'Дима':
                bot.send_message(message.chat.id, '@RuFuZZZ, выйди на связь!', reply_markup=markup)
            elif message.text == 'Вова':
                bot.send_message(message.chat.id, '@JustSenseSeeker, выйди на связь!', reply_markup=markup)
            elif message.text == 'Вася':
                bot.send_message(message.chat.id, '@codemdvd, выйди на связь!', reply_markup=markup)
            elif message.text == 'Прохор':
                bot.send_message(message.chat.id, '@prokhorkotov, выйди на связь!', reply_markup=markup)
    bot.register_next_step_handler(message,back)


@bot.message_handler(content_types=['text'])
def back(message):
    markup = types.ReplyKeyboardMarkup()
    if message.text == 'Назад':
        message.text = 'Да'
        choosing_action(message)


@bot.message_handler(content_types=['text'])
def news(message):




bot.polling(none_stop=True)
