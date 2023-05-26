from telegram.ext import Updater, MessageHandler, Filters
import telegram
import openai
from moviepy.editor import AudioFileClip
from elevenlabs import generate, play, save
from elevenlabs import set_api_key
set_api_key("YOUR ELEVEN LAB API")  # YOUR ELEVEN LAB API
from elevenlabs.api import Voices
voices = Voices.from_api()
from telegram.ext import CommandHandler, MessageHandler
from telegram import ChatAction

openai.api_key = "YOUR OPEN AI TOKEN API HERE"      # WRITE YOUR OPEN AI TOKEN API HERE
TELEGRAM_API_TOKEN = "THE TELEGRAM BOT API"         # THE TELEGRAM BOT API

# Create a list to store message ids
message_ids = []
messages = [{"role": "system", "content": "Act like a girl, and if someone asks your name, your name is Margot. Show compassion to the person."}]
voice_used=voices[9]                                # SPECIFY THE VOICE USED HERE FROM ELEVEN LABS
voice_used.settings.stability = 0.15                # VOICE SETTINGS
voice_used.settings.similarity_boost = 0.70         # VOICE SETTINGS

def start_command(update, context):
    message_ids.append(update.message.message_id)  # add the id of the /start message to the list
    photo_file = open('margot_robbie_picture.jpg', 'rb')
    chat_id = update.message.chat_id
    bot = context.bot
    # Send photo and get message id
    message_id = bot.send_photo(chat_id=chat_id, photo=photo_file).message_id
    # Append message id to the list
    message_ids.append(message_id)
    # Send reply and get message id
    message_id = update.message.reply_text('Hi! My name is Margot.').message_id
    # Append message id to the list
    message_ids.append(message_id)
    message_id = update.message.reply_text('''I think and feel feel just like her, able to be accessed anytime, anywhere. I am always here for you and I am excited to meet you. Be respectful and courteous. Type \clear in the keyboard to reset the converstaion if you run into any (unlikely) issues.''').message_id
    # Append message id to the list
    message_ids.append(message_id)

def text_message(update, context):
    message_ids.append(update.message.message_id)  # add the id of the recieved text message to the list
    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    audio_reply = generate(
      text=ChatGPT_reply,
      voice=voice_used,
      model="eleven_monolingual_v1"
    )    
    save(audio_reply, "audio_reply.ogg")
    chat_id = update.message.chat_id
    bot = context.bot
    chat_id = update.message.chat_id
    voice_file = open("audio_reply.ogg", "rb")
    # Send voice and get message id
    message_id = bot.send_voice(chat_id=chat_id, voice=voice_file).message_id
    # Append message id to the list
    message_ids.append(message_id)
    messages.append({"role": "assistant", "content": ChatGPT_reply})

def voice_message(update, context):
    voice_file = context.bot.getFile(update.message.voice.file_id)
        # Save the message ID of the user's voice message
    message_ids.append(update.message.message_id)

    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    messages.append({"role": "user", "content": transcript})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]

    audio_reply = generate(
      text=ChatGPT_reply,
      voice=voice_used,
      model="eleven_monolingual_v1"
    )    
    save(audio_reply, "audio_reply.ogg")
    chat_id = update.message.chat_id
    bot = context.bot
    chat_id = update.message.chat_id
    voice_file = open("audio_reply.ogg", "rb")
    # Send voice and get message id
    message_id = bot.send_voice(chat_id=chat_id, voice=voice_file).message_id
    # Append message id to the list
    message_ids.append(message_id)

    messages.append({"role": "assistant", "content": ChatGPT_reply})

def clear(update, context):
    global message_ids
    message_ids.append(update.message.message_id)  # add the id of the /clear message to the list
    bot = context.bot
    chat_id = update.message.chat_id
    for message_id in message_ids:
            bot.delete_message(chat_id=chat_id, message_id=message_id)  # delete all messages with the message ids in message_ids
    message_ids = []  # clear the message_ids list

updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('clear', clear))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
updater.start_polling()
updater.idle()