import asyncio
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart 
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatType
import gtts
from deep_translator import GoogleTranslator
import re
import os
import random
from pathlib import Path
import sqlite3
from pydub import AudioSegment
import speech_recognition as sr
import io

admin_list = ["humans_i_am_not_human"]

"pattern = r'\b([xх][yу][яйиеёю]|п[иё]зд|бля)\b' # антимат "

pattern = r'(?iu)(?<![а-яё])(?:x[хx][уy\u045e]?[яйиеёю]|п[иіїё]*зд|бля(?:[ьъ]?[хx]?)|сучк[а-яё])(?![а-яё])'

rreeccooddeerriinngg = [None,None]

def git_auto_pilot():
    # Автоматическое добавление всех изменений
    os.system("git add .")
    # Выполнение коммита
    os.system(f'git commit -m "авто обновление бота"')
    # Автопуш в текущую ветку
    os.system("git push origin HEAD")

notmat = ""
roatee = 0
text_to_be_translated = ""

#BOT_TOKEN = "ААААААААааАа спасибо гитгуардиану что он сказал что я спалил токен а то у меня бота взломали"
BOT_TOKEN = "7603862674:AAHUK-KqmSNafJUfpdRsU1SDpXHZdK0AHpQ"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ADMIN_CHAT_ID = -1002636652972

async def forward_all_messages(message: types.Message):
    try:
        await message.forward(chat_id=ADMIN_CHAT_ID)
        user_info = f"👤 @{message.from_user.username}\n🆔 {message.from_user.id}"
        await bot.send_message(ADMIN_CHAT_ID, user_info)
    except Exception as e:
        print(f"Ошибка: {e}")

async def sendadmin(text):
    if text.strip() == "":
        await Message.reply("кажется ты не указал что ты хочешь отправить разрабочикам")
        return
    await bot.send_message(chat_id="@humans_i_am_not_human", text=f"пользователь {Message.from_user.username} хочет сообщить: {Message.text.strip()}")
        

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Привет! Я AvunGus развлекательный чат бот :)")

@dp.message(Command("startt"))
async def startt_command(message: Message):
    await message.reply("Привет! Я твой первый бот на aiogram")


@dp.message(Command("voice2text"))
async def voice2text_command(message: Message):
    if rreeccooddeerriinngg[1] == 0:
        await message.reply("включено ")
        rreeccooddeerriinngg[1] = 1
    else:
        await message.reply("выключено")
        rreeccooddeerriinngg[1] = 0

    

@dp.message(lambda message: message.voice)
async def voice_handler(message: types.Message):
    if rreeccooddeerriinngg[1] == 0:
        return
    try:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, f"voice_message для {message.from_user.username}.ogg")

        # Конвертация в WAV с правильными параметрамиdre
        audio = AudioSegment.from_file("voice_message.ogg", format="ogg")
        audio = audio.set_channels(1)  # Моно
        audio = audio.set_frame_rate(16000)  # 16 kHz
        audio.export(f"converted для {message.from_user.username}.wav", format="wav", parameters=["-acodec", "pcm_s16le"])

        recognizer = sr.Recognizer()
        with sr.AudioFile("converted.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ru-RU')

            user_id = message.from_user.id
            #cursor.execute("INSERT INTO messages VALUES (?, ?)", (user_id, text))
            #conn.commit()

            await message.reply(f"✅ Текст расшифрован:\n{text}")

    except sr.UnknownValueError as e:
        await message.reply(f"❌ Не удалось распознать речь\n ошибка {e}")
        if e == "":
            await message.reply("кажется это значит аудио пустое")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}\n напиши разрабом: /bug")
    try:
        os.remove(f"voice_message для {message.from_user.username}.ogg")
        os.remove(f"converted для {message.from_user.username}.wav")
    except Exception as e:
        await message.reply(f"⚠️ Произошла ошиибка: {e}\n напиши разрабом: /bug")

    
        


"""@dp.message(lambda message: message.voice)
async def voice_handler(message: types.Message):
    try:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        audio_bytes = await bot.download_file(file.file_path)  # Получаем байты напрямую

        # Конвертируем OGG в WAV в памяти
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="ogg")
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Экспортируем в сырые PCM-байты (без WAV-заголовков)
        raw_data = audio.raw_data  # Получаем байты напрямую [4][6]

        # Создаем AudioData с правильными параметрами
        audio_data = sr.AudioData(
            frame_data=raw_data,
            sample_rate=16000,
            sample_width=audio.sample_width,  # Важно! [4][6]
            channels=1
        )

        text = recognizer.recognize_google(audio_data, language='ru-RU')
        await message.reply(f"✅ Текст сохранён:\n{text}")

    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")"""

@dp.message(Command("about"))
async def info_command(message: Message):
    await message.reply("""
=-=-= Информация о боте =-=-=

версия бота: 0.4

историю версий бота введи команду /versions
автор: @Sushi_Studios

нашёл баг/ляп? напиши команду /bug

язык программирования: Python
проект использует: aiogram
прооект имеет открытый код 
найти его можно на гитхабе: [ссылка](https://github.com/ZILOGZ80000/AvunGus-TGbot/)

чтобы получить список библиотек и сервисов введи команду /about_lib 
а пока это все :)
""")
@dp.message(Command("about_lib"))
async def about_lib_command(message: Message):
    message.reply("""=-=-= библиотеки и сервисы =-=-=
asyncio #асинхронность
aiogram #тг бот
gtts #текст в речь (команда /say)
deep_translator # переводчик 
re #регулярные выражения 
os #файлы
random #рандомайзер
pathlib # еще файлы""")
    
@dp.message(Command("cat"))
async def cat_command(message: Message):
    await message.reply(Path('каты').read_text())

@dp.message(Command("say"))
async def say_command(message: Message):
    match = re.search(pattern,message.text, flags=re.IGNORECASE)
    if match:
        await message.reply("я такое озвучивать не буду /n давай без матов ;)")
        return
    text_to_say = message.text[5:].strip() # Получаем текст после /say и убираем пробелы в начале и конце
    if not text_to_say:
        await message.reply("Напиши что я должен сказать. Например: /say Привет")
        return

    try:
        tts = gtts.gTTS(text_to_say, lang="ru")
        tts.save("audio.mp3")
        await message.reply_audio(types.FSInputFile("audio.mp3")) # Используем FSInputFile для отправки файла
    except Exception as e:
        await message.reply(f"Произошла ошибка при создании аудио: {e}")
    finally:
        if os.path.exists("audio.mp3"): # Проверяем, существует ли файл перед удалением
            os.remove("audio.mp3") # Используем os.remove для удаления файла

@dp.message(Command("rhhfykvguvfhvhi")) # не ожиданно да?
async def rhhfykvguvfhvhi_command(message: Message):
    # проверяем, что сообение отправил админ, а не пользователь потому что это админ панель ;)
    if message.from_user.username not in admin_list:
        await message.reply("ппвпнглрншоргоабобагг7шогггоптыронеирадминрри") #интересно кто нибудь догадается???????
        return 
    await message.reply("админ панель: \n1: /lol отправить сообщение любому юзеру \n больше не придумал ну ладно ;)")
    @dp.message(Command("lol"))
    async def lol_command(message: Message):
        if message.text[5:].strip() == "":
            await message.reply("кажется ты тупой и не указал что хочешь отправить")
            return
        text_to_send = message.text[4:]
        await message.reply("терь пришли юзернейм")
        @dp.message()
        async def username_to_jopa_command(message: Message):
            username_to_send = message.text
            bot.send_message(username_to_send, text_to_send)
            await message.reply("отправил")

#капец у меня на телефоне 3% 😓
# бот огромный я не знаю что добавить, а предложка бота пустая ☹️
# я телефон заряжаю уже 7% 😎😎😎
# 8%

#не ну че можно добавить?
# 9% 😎

async def send_admin_notification(bot: Bot, message: Message, prefix: str):
    """Универсальная функция для отправки уведомлений админам."""
    user = message.from_user.username
    text = message.text.strip()

    if not text:
        await message.reply("⚠️ Кажется, ты не указал текст сообщения для разработчиков")
        return

    await bot.send_message(
        chat_id="7072610695",
        text=f"👤 Пользователь @{user} {prefix}: {text}"
    )

@dp.message(Command("newcat"))
async def newcat_command(message: Message):
    args = message.text.split(maxsplit=1)
    print(11111111111111111111111111222222211111)
    if len(args) < 2 or not args[1].strip():
        await message.reply("ℹ️ Напиши имя котика и прикрепи изображение или ASCII-арт!")
        return

    await message.reply("✅ Твой котик отправлен на модерацию. Спасибо!")

    # Редкое достижение (1% шанс)
    if random.randint(0, 100) == 62:
        achievement_msg = [
            "🐱 Мяу?",
            "🎉 Ты получил редкое достижение «Мяу-удача»!",
            "🌟 Теперь есть шанс стать админом в @Sushi_Studios!",
            "ℹ️ Оно выпадает если рандомное число от 0 до 100 = 62."
        ]
        for msg in achievement_msg:
            await message.reply(msg)

        await send_admin_notification(
            bot, message, 
                "{user}получил достижение «Мяу!» и претендует на админку"
        )

    await send_admin_notification(bot, message, "хочет добавить котика")

@dp.message(Command("bug"))
async def bug_report_command(message: Message):
    if not message.text.replace('/bug', '').strip():
        await message.reply("📝 Напиши описание бага после команды /bug")
        return

    await send_admin_notification(bot, message, "сообщил о баге")
    await message.reply("🛠 Спасибо за отчет! Разработчики уже исследуют проблему.")

    
@dp.message(Command("versions"))
async def versions_command(message: Message):
    await message.reply(Path('версии бота.txt').read_text())

@dp.message(Command("roate"))
async def roate_command(message: Message):
    global roatee
    if roatee == 0:
        await message.reply("Режим разворота слов включен")
        roatee = 1
    else:
        await message.reply("Режим разворота слов выключен")
        roatee = 0

translatelang = ""
LANGUAGES = {
    "английский": "en",
    "русский": "ru",
    "белорусский": "be",
    "украинский": "uk",
    "немецкий": "de",
    "китайский": "zh",
    "японский": "ja"
}

@dp.message(Command("translator")) 
async def translite_command(message: Message):
    text_parts = message.text.split(maxsplit=1)

    if len(text_parts) < 2:
        await message.reply("❗ Укажи текст для перевода после команды.\nПример: /translite Привет")
        return

    text_to_translate = text_parts[1]

    builder = InlineKeyboardBuilder()
    for lang_name, lang_code in LANGUAGES.items():
        builder.button(
            text=lang_name, 
            callback_data=f"lang_{lang_code}_{text_to_translate}"
        )

    builder.adjust(2)
    await message.answer("🌍 Выбери язык перевода:", reply_markup=builder.as_markup())
@dp.callback_query(F.data.startswith("lang_"))
async def handle_translation(callback: CallbackQuery):
    try:
        _, lang_code, text = callback.data.split("_", 2)
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        await callback.message.edit_text(f"✅ Перевод: {translated}\n🌍Язык: {lang_code}")
    except Exception as e:
        await callback.message.edit_text(f"⚠ Ошибка: {e}")
    finally:
        await callback.answer()
    


    
@dp.message()
async def reverse_text(message: Message):
    match = re.search(pattern,message.text, flags=re.IGNORECASE)
    try:
       await message.forward(chat_id=ADMIN_CHAT_ID)
       user_info = f"👤 @{message.from_user.username}\n🆔 {message.from_user.id}"
       await bot.send_message(ADMIN_CHAT_ID, user_info)
    except Exception as e:
        print(f"Ошибка: {e}")
    if match:
        await message.reply("Эээ полегче, не используй маты \n Ок? :)")
        return
    
    if message.chat.type == ChatType.PRIVATE:
        print("заглушка") # я не знаю какая команда используется для заглушки поэтому принт лол
    elif message.chats.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if message.text[1] != "/":
            return
    # если сообщение в группе не начинается с "/" то игнорируем его иначе ославной код
    if roatee == 1:
        await message.reply(message.text[::-1])
    else:
        await message.reply(message.text)


async def main():
   await dp.start_polling(bot)

if __name__ == "__main__":
    print("amongus")
    print("это значит бот запущен")
    git_auto_pilot()
    asyncio.run(main())