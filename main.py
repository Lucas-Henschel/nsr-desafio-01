import telebot
import requests
from datetime import datetime

KEY_BOT = "6734944049:AAFnUpHfYWUSEjBeD0CJASHxlyX8Slt4o-M"
bot = telebot.TeleBot(KEY_BOT)

KEY_NASA = "vpeLfEp1xeFNAyJf2fHfQ4eIaG0n5cYWfURGw7Ip"
url = "https://api.nasa.gov/planetary/apod?api_key=" + KEY_NASA

user_data = {}

def validateData(data_str):
    try:
        datetime.strptime(data_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

@bot.message_handler(commands=["commands"])
def listCommands(message):
    text = """
✨ Recursos do Bot:
    
    /apod - Receba a imagem mais recente do APOD da NASA.
    /data - Escolha uma data específica para ver a imagem do APOD.
    """

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["data"])
def sendImageWithDate(message):
    bot.send_message(message.chat.id, "Por favor, digite a data no formato 'DD/MM/AAAA'")
    user_data[message.chat.id] = "date_loading"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id) == "date_loading")
def processar_data(message):
    if not validateData(message.text):
        sendImageWithDate(message)
        return

    formatedDate = datetime.strptime(message.text, "%d/%m/%Y").strftime("%Y-%m-%d")
    chat_id = message.chat.id

    response = requests.get(url + "&date=" + formatedDate)

    if response.status_code == 200:
        jsonData = response.json()
        imageURL = jsonData["url"]
        imageTitle = jsonData["title"]
        imageDescription = jsonData["explanation"]
        bot.send_photo(chat_id, imageURL)

        text = f"""
            🌌 {imageTitle} 🌌
            
            {imageDescription}
        """
        bot.send_message(message.chat.id, text)
    else:
        print(f"A requisição falhou com o código de status {response.status_code}")

    listCommands(message)
    del user_data[message.chat.id]

@bot.message_handler(commands=["apod"])
def sendImageToday(message):
    response = requests.get(url)
    chat_id = message.chat.id

    if response.status_code == 200:
        jsonData = response.json()
        imageURL = jsonData["url"]
        imageTitle = jsonData["title"]
        imageDescription = jsonData["explanation"]
        bot.send_photo(chat_id, imageURL)

        text = f"""
           🌌 {imageTitle} 🌌

            {imageDescription}
        """
        bot.send_message(message.chat.id, text)
    else:
        print(f"A requisição falhou com o código de status {response.status_code}")

    listCommands(message)

def toCheck(message):
    return True

@bot.message_handler(func=toCheck)
def defaultMessage(message):
    text = """
    🚀 Bem-vindo ao nosso Bot do APOD! 🌌

    Este bot é o seu portal para explorar as maravilhas do cosmos todos os dias. Com o Astronomy Picture of the Day (APOD), você receberá diariamente uma imagem espetacular do espaço, juntamente com uma descrição fascinante.
    
✨ Recursos do Bot:
    
    /apod - Receba a imagem mais recente do APOD da NASA.
    /data - Escolha uma data específica para ver a imagem do APOD.
    /commands - Lista todos os camanhos do bot.
    
🌟 Como usar o Bot:
    
    Basta digitar um dos comandos acima no chat, e o nosso bot irá responder prontamente com a imagem ou informações que você deseja. Explore o universo, aprenda mais sobre o espaço e compartilhe essas descobertas com seus amigos!
    """
    bot.reply_to(message, text)

bot.polling()
