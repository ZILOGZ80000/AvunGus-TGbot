import asyncio
from aiogram import F, Router
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import gtts
from deep_translator import GoogleTranslator
import re
import os
import random
from pathlib import Path

#список админов интересно а надо юзы или ид ??????
#ответ: фиг знает 
#ахахахахах
admin_list = ["humans_i_am_not_human"]
#ладно пусь будут юзернеймы

"pattern = r'\b([xх][yу][яйиеёю]|п[иё]зд|бля)\b' # антимат "

pattern = r'(?iu)(?<![а-яё])(?:x[хx][уy\u045e]?[яйиеёю]|п[иіїё]*зд|бля(?:[ьъ]?[хx]?)|сучк[а-яё])(?![а-яё])'



notmat = ""
roatee = 0
text_to_be_translated = ""

BOT_TOKEN = "7603862674:AAHWuJpvkLaNj6gJL4SMpxsu3zBLRrYvY_I"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

@dp.message(Command("info"))
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
найти его можно в канале @Sushi_Studios

чтобы получить кота введи команду /cat 

а пока это все :)
""")

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
        # как можно получить 2 параметра?(текст и юзернейм)
        # ответ: мозги мои думайтеееееееее аааааааа кажется мой мозг набирает IQ 👩‍💻👩‍💻👩‍💻 я умнею уууу 😃😃😃 мое икю уже больше 0 афигеть вот это я умный 😎😎😎 йа придумал вот как можно вытажить 2 параметра: жопа туся на туся на ладно я умный 😎😎😎
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

    if len(args) < 2 or not args[1].strip():
        await message.reply("ℹ️ Напиши имя котика и прикрепи изображение или ASCII-арт!")
        return

    await message.reply("✅ Твой котик отправлен на модерацию. Спасибо!")

    # Редкое достижение (1% шанс)
    if random.randint(1, 100) == 62:
        achievement_msg = [
            "🐱 Мяу?",
            "🎉 Ты получил редкое достижение «Мяу-удача»!",
            "🌟 Теперь есть шанс стать админом в @Sushi_Studios!"
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

""""router = Router()

# Словарь языков для перевода
LANGUAGES = {
    "английский": "en",
    "русский": "ru",
    "белорусский": "be",
    "украинский": "uk",
    "немецкий": "de",
    "китайский": "zh",
    "японский": "ja"
}

@router.message(Command("translite"))
async def translite_command(message: Message):
    # Извлекаем текст после команды
    text_to_translate = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not text_to_translate:
        await message.reply("❗ Напиши текст для перевода после команды.\nПример: /translite Привет")
        return

    # Создаем клавиатуру
    builder = InlineKeyboardBuilder()
    for lang_name, lang_code in LANGUAGES.items():
        builder.button(text=lang_name, callback_data=f"lang_{lang_code}_{text_to_translate}")

    builder.adjust(2)  # 2 кнопки в ряду
    await message.answer("Выбери язык перевода:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("lang_"))
async def handle_translation(callback: CallbackQuery):
    # Разбираем данные из callback
    _, lang_code, text_to_translate = callback.data.split("_", 2)

    # Выполняем перевод
    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text_to_translate)
        await callback.message.edit_text(f"🔤 Перевод: {translated}")
    except Exception as e:
        await callback.message.edit_text(f"⚠ Ошибка перевода: {str(e)}")

    await callback.answer()"""

router = Router()  # Создаем отдельный роутер

# Подключаем роутер к диспетчеру в основном файле:
# dp.include_router(router)

LANGUAGES = {
    "английский": "en",
    "русский": "ru",
    "белорусский": "be",
    "украинский": "uk",
    "немецкий": "de",
    "китайский": "zh",
    "японский": "ja"
}

@dp.message(Command("translator"))  # Фильтр команды без учёта состояния
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

@router.callback_query(F.data.startswith("lang_"))
async def handle_translation(callback: CallbackQuery):
    try:
        _, lang_code, text = callback.data.split("_", 2)
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        await callback.message.edit_text(f"✅ Перевод: {translated}")
    except Exception as e:
        await callback.message.edit_text(f"⚠ Ошибка: {e}")
    finally:
        await callback.answer()

    
@dp.message()
async def reverse_text(message: Message):
    match = re.search(pattern,message.text, flags=re.IGNORECASE)
    if match:
        await message.reply("Эээ полегче, не используй маты \n Ок? :)")
        return
    """if message.chats.type == ChatType.PRIVATE:
        print("заглушка") # я не знаю какая команда используется для заглушки поэтому принт лол
    elif message.chats.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if message.text[1] != "/":
            return"""
    # если сообщение в группе не начинается с "/" то игнорируем его иначе ославной код
    if roatee == 1:
        await message.reply(message.text[::-1])
    else:
        await message.reply(message.text)


async def main():
   await dp.start_polling(bot)

if __name__ == "__main__":
    print("amongus")
    asyncio.run(main())
