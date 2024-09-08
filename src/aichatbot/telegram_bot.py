import telebot
from telebot import types
import yaml
import logging

logging.basicConfig(
    filename="/var/log/aichatbot.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


with open("bot_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Создаём бота
bot = telebot.TeleBot(config["telegram_token"])
logging.info("Бот запущен")

# Ограничиваем пользователей, чтобы пользоваться ботом могли только сотрудники компании
allowed_users = config["allowed_users"]
logging.info("Разрешенные пользователи: "+str(allowed_users))

# Текст приветственного сообщения
hello_message = config["hello_message"]

# Импортируем модель RAG в зависимости от поставщика ИИ

if config["ai_provider"] == "sber":
    from sber_rag import *

else:
    from yandex_rag import *

# Загружаем документы и создаём LLM машину с режимом QA (questions&answers)
qa_chain, retriever = create_qa_chain("dochub")
logging.info("Создал QA chain")

# Обработка входящих команд (на будущее)
@bot.message_handler(commands=['start'])
def get_text_messages(message):
    logging.info(str(message.text))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Знаток документов")
    item2 = types.KeyboardButton("Разработчик go")
    markup.add(item1, item2)
    bot.send_message(message.from_user.id, hello_message, reply_markup=markup)

#Обработка входящих сообщений: отправляем их в ИИ, ответ отправляем в телегу
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    global qa_chain, retriever
    if message.from_user.username in allowed_users:
        if(message.text == "Знаток документов"):
            bot.send_message(message.chat.id, text="В этом режиме я буду отвечать исходя из содержимого DocHub")            
            qa_chain, retriever = create_qa_chain("dochub")
        elif(message.text == "Разработчик go"):
            bot.send_message(message.chat.id, text="В этом режиме я буду отвечать исходя из содержимого репозитория go")
            qa_chain, retriever = create_qa_chain("go")
        else:
            logging.info("Получил от "+str(message.from_user.username)+" сообщение: "+str(message.text))
            ai_response = ask_llm(message.text)
            logging.info("Ответ ИИ: "+ai_response)
            bot.reply_to(message, ai_response)
    else:
        bot.reply_to(message, config["refuse_message"])
        logging.error("Отклонена попытка обращения от: "+str(message.from_user.username))

def ask_llm(question):
    if config["ai_provider"] == "sber":
        message = str(question)
        llm_response = qa_chain({"query": message})
        bot_response = llm_response['result']
    else:
        bot_response = question_ai(qa_chain, retriever, question)
    return bot_response

bot.polling(none_stop=True, timeout=10, long_polling_timeout = 5)
