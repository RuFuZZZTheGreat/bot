import telebot
from telebot import types
import requests
import random
from bs4 import BeautifulSoup as b

bot = telebot.TeleBot('5433415893:AAHK6GBetdPstASvZyEh1aSvpT7vqFvcnr0')
url = 'https://www.anekdot.ru/release/anekdot/day/'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anecdotes = soup.find_all('div', class_='text')
    return [c.text for c in anecdotes]


list_of_jokes = parser(url)
random.shuffle(list_of_jokes)


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
        markup.add(joke, spamming)
        bot.send_message(message.chat.id, 'Отлично! Настало время выбрать, чем я тебе могу помочь!',
                         reply_markup=markup)
        bot.register_next_step_handler(message, two_actions)

    else:
        bot.send_message(message.chat.id, 'Ну я же говорил, что я пока что глупенький и не понимаю человеческий язык! '
                                          'Нажми конпку "Да" внизу, чтобы начать!')


@bot.message_handler(content_types=['text'])
def two_actions(message):
    if message.text == 'Анекдот':
        bot.send_message(message.chat.id, 'Хочешь развлечься анекдотами? Напиши любую цифру от 1 до 9')
        bot.register_next_step_handler(message, jokes)
    elif message.text == 'Спам':
        spam_buttons(message)
        bot.register_next_step_handler(message, spam)


@bot.message_handler(content_types=['text'])
def jokes(message):
    markup = types.ReplyKeyboardMarkup()
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        ready = types.KeyboardButton('Да')
        markup.add(ready)
        bot.send_message(message.chat.id, 'Хороший выбор! Злодейству не бывать! Хочешь ещё вместе развлечься? Жми '
                                          'скорее "ДА"!', reply_markup=markup)
    else:
        if message.text.lower() in '123456789':
            bot.send_message(message.chat.id, list_of_jokes[0])
            del list_of_jokes[0]
            bot.register_next_step_handler(message, jokes)
        else:
            bot.send_message(message.chat.id, 'Я просил написать цифру, а ты пытаешься меня сломать! '
                                              'Давай попробуем ещё раз! Напиши цифру от 1 до 9')
            bot.register_next_step_handler(message, jokes)


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


def spam(message):
    markup = types.ReplyKeyboardMarkup()
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        ready = types.KeyboardButton('Да')
        markup.add(ready)
        bot.send_message(message.chat.id, 'Хороший выбор! Злодейству не бывать! Хочешь ещё вместе развлечься? Жми '
                                          'скорее "ДА"!', reply_markup=markup)
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


# @bot.message_handler(content_types=['text'])
# def sus_function(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#     ready = types.KeyboardButton('Да')
#     markup.add(ready)
#     bot.send_message(message.chat.id, 'Хочешь ещё вместе развлечься? Жми скорее "ДА"!', reply_markup=markup)


bot.polling(none_stop=True)
