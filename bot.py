import telebot
from telebot import types
from nltk.corpus import wordnet
from pyaspeller import YandexSpeller

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=["start"])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('English', 'Russian', 'Help')
    bot.send_message(message.chat.id,
                     'Hello! Please choose language:\n'
                     'Привет! Пожалуйста, выберите язык:',
                     reply_markup=markup)

def token_func(message):
    import nltk
    import string
    nltk.download('omw-1.4')
    from nltk.probability import FreqDist
    from nltk import word_tokenize
    text = message.text
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…'
    def remove_chars_from_text(text, chars):
        return "".join([ch for ch in text if ch not in chars])
    text = remove_chars_from_text(text, spec_chars)
    STOPWORDS = set(nltk.corpus.stopwords.words('english'))
    s = ' '.join([word for word in text.split() if word not in STOPWORDS])
    text_tokens = word_tokenize(s)
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)
    a = fdist.most_common(5)

    bot.send_message(message.chat.id, 'Your most frequently used word: ' + str(a))

def rus_token_func(message):
    import nltk
    import string
    nltk.download('omw-1.4')
    from nltk.probability import FreqDist
    from nltk import word_tokenize
    text = message.text
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…'

    def remove_chars_from_text(text, chars):
        return "".join([ch for ch in text if ch not in chars])
    text = remove_chars_from_text(text, spec_chars)

    STOPWORDS = set(nltk.corpus.stopwords.words('russian'))
    s = ' '.join([word for word in text.split() if word not in STOPWORDS])

    text_tokens = word_tokenize(s)
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)

    a = fdist.most_common(5)
    bot.send_message(message.chat.id, 'Ваше самое часто встречающее слово: ' + str(a))

def orfo_func(message):
    speller = YandexSpeller()
    fixed = speller.spelled(message.text)
    bot.send_message(message.chat.id, fixed)

def eng_orf_func(message):
    import nltk

    from nltk.metrics.distance import edit_distance

    nltk.download('words')
    from nltk.corpus import words
    correct = words.words()

    my_word = [message.text]

   
    for word in my_word:
        temp = [(edit_distance(word, w), w) for w in correct if w[0] == word[0]]
        a = (sorted(temp, key=lambda val: val[0])[0][1])

        bot.send_message(message.chat.id, a)
def antonym_func(message):
    for syn in wordnet.synsets(message.text):
        for i in syn.lemmas():
            if i.antonyms():
                a = (i.antonyms()[0].name())
                bot.send_message(message.chat.id, a)
    bot.send_message(message.chat.id, 'Please write verb')

def syn_func(message):
    for i in wordnet.synsets(message.text):
        for lemma in i.lemmas():
            a = lemma.name()
            bot.send_message(message.chat.id, a)

def rus_syn_func(message):
    import requests
    from urllib.parse import unquote
    from lxml.html import fromstring

    w = message.text
    u = str(('https://text.ru/synonym/' + w))
    url = u
    response = requests.get(url)
    root = fromstring(response.text)
    synonyms = root.xpath('//td[@class="ta-l"]/a[@href]')

    for synonym in synonyms:
        a = synonym.text
        bot.send_message(message.chat.id, a)

def rus_antonym_func(message):
    import requests
    from urllib.parse import unquote
    from lxml.html import fromstring
    w = message.text
    u = str('https://razbiraem-slovo.ru/antonyms/' + w)
    url = u
    response = requests.get(url)
    root = fromstring(response.text)
    antonyms = root.xpath('//div[@class="words-columns__breaker"]/a[@href]')

    for antonym in antonyms:
        a = antonym.text
        bot.send_message(message.chat.id, a)

def summarized_func(message):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    text = message.text

    stopWords = set(stopwords.words('English'))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0

    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if(sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += ' ' + sentence

    bot.send_message(message.chat.id, summary)

def rus_summarized_func(message):
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    text = message.text

    stopWords = set(stopwords.words('Russian'))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0

    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += ' ' + sentence

    bot.send_message(message.chat.id, summary)

@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Help':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Back')
        bot.send_message(message.chat.id, 'Hey! This bot can do all sorts of things with text!\n'
                                          'Spelling\n'
                                          'This function corrects misspelled words, if any, and sends the corrected version.\n'
                                          'Synonym\n'
                                          'This function finds synonyms and sends them all.\n'
                                          'Antonym\n'
                                          'This function finds antonyms and sends them all.\n'
                                          'Tokenization\n'
                                          'This function takes text and sends the most frequently occurring words.\n'
                                          'Summarize\n'
                                          'This function accepts text and sends a shortened version of the text.')
        bot.send_message(message.chat.id, 'Привет! Этот бот может делать с текстом все что угодно!\n'
                                           'Орфография\n'
                                           'Эта функция исправляет слова с ошибками, если таковые имеются, и отправляет исправленную версию.\n'
                                           'Синоним\n'
                                           'Эта функция находит синонимы и отправляет их все.\n'
                                           'Антоним\n'
                                           'Эта функция находит антонимы и отправляет их все.\n'
                                           'Токенизация\n'
                                           'Эта функция берет текст и отправляет наиболее часто встречающиеся слова.\n'
                                           'Суммаризация\n'
                                           'Эта функция принимает текст и отправляет сокращенную версию текста».', reply_markup=markup)
    if message.text == "Russian":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Орфография', 'Синоним', "Антоним")
        markup.row('Ключевые слова', "Суммаризация", 'Назад')
        bot.send_message(message.chat.id, 'Выбери что хочешь сделать: ', reply_markup=markup)

    if message.text == 'Суммаризация':
        sent_msg = bot.send_message(message.chat.id, 'Пожалуйста поставьте свой текст: ')
        bot.register_next_step_handler(sent_msg, rus_summarized_func)

    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('English', 'Russian', 'Help')
        bot.send_message(message.chat.id,
                         'Hello! Please choose language:\n'
                         'Привет! Пожалуйста, выберите язык:',
                         reply_markup=markup)

    if message.text == 'Back':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('English', 'Russian', 'Help')
        bot.send_message(message.chat.id,
                         'Hello! Please choose language:\n'
                         'Привет! Пожалуйста, выберите язык:',
                         reply_markup=markup)

    if message.text == 'Синоним':
        sent_msg = bot.send_message(message.chat.id, 'Пожалуйста поставьте свой текст: ')
        bot.register_next_step_handler(sent_msg, rus_syn_func)

    if message.text == 'Ключевые слова':
        sent_msg = bot.send_message(message.chat.id, 'Пожалуйста поставьте свой текст: ')
        bot.register_next_step_handler(sent_msg, rus_token_func)

    if message.text == 'Антоним':
        sent_msg = bot.send_message(message.chat.id, 'Пожалуйста поставьте свой текст: ')
        bot.register_next_step_handler(sent_msg, rus_antonym_func)

    if message.text == 'Орфография':
        sent_msg = bot.send_message(message.chat.id, 'Пожалуйста поставьте свой текст: ')
        bot.register_next_step_handler(sent_msg, orfo_func)

    if message.text == "English":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Spelling', 'Synonym', 'Antonym')
        markup.row('Keywords',  'Summarized' , 'Back')

        bot.send_message(message.chat.id, 'Choose what you want to do: ', reply_markup=markup)

    if message.text == 'Summarized':
        sent_msg = bot.send_message(message.chat.id, 'Please write your text: ')
        bot.register_next_step_handler(sent_msg, summarized_func)

    if message.text == 'Spelling':
        sent_msg = bot.send_message(message.chat.id, 'Please write your text: ')
        bot.register_next_step_handler(sent_msg, eng_orf_func)

    if message.text == 'Synonym':
        sent_msg = bot.send_message(message.chat.id, 'Please write your text: ')
        bot.register_next_step_handler(sent_msg, syn_func)

    if message.text == 'Keywords':
        sent_msg = bot.send_message(message.chat.id, 'Please write your text: ')
        bot.register_next_step_handler(sent_msg, token_func)

    if message.text == 'Antonym':
        sent_msg = bot.send_message(message.chat.id, 'Please write your text: ')
        bot.register_next_step_handler(sent_msg, antonym_func)

bot.polling()
