import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

# загрузка токена из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# у каждого пользователя свой сдвиг (по умолчанию 3) (проблема - если сервера перезагрузятся, сдвиг сбросится)
user_shift = {}

# функция шифра Цезаря (латиница + кириллица)
def caesar(text, shift):
    result = ""

    for ch in text:
        # латиница A-Z
        if "A" <= ch <= "Z":
            result += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
        # латиница a-z
        elif "a" <= ch <= "z":
            result += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
        # кириллица А-Я
        elif "А" <= ch <= "Я":
            result += chr((ord(ch) - ord("А") + shift) % 32 + ord("А"))
        # кириллица а-я
        elif "а" <= ch <= "я":
            result += chr((ord(ch) - ord("а") + shift) % 32 + ord("а"))
        else:
            result += ch  # символы без изменений
    return result

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # команда /start
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        user_shift[message.from_user.id] = 3  # сдвиг по умолчанию
        await message.answer("Ку, я напиши текст, я его зашифрую! (по умолчанию сдвиг - 3) \n/help — помощь")

    # команда /help
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        await message.answer("/start — начать\n/help — помощь\n/setshift N — установить сдвиг\n")

    # команда /setshift
    @dp.message(Command("setshift"))
    async def cmd_setshift(message: types.Message):
        try:
            n = int(message.text.split()[1])
            user_shift[message.from_user.id] = n
            await message.answer(f"Сдвиг изменён на {n}")
            print(f"Пользователь {message.from_user.id} установил сдвиг = {n}")  # вывод в консоль
        except:
            await message.answer("Нужно написать вот так: /setshift n, где n — целое число.")

    # обработка текста
    @dp.message(lambda m: m.text)
    async def on_text(message: types.Message):
        shift = user_shift.get(message.from_user.id, 3)
        encrypted = caesar(message.text, shift)
        await message.answer(f"Твой текст зашифрован:\n{encrypted}")

    # обработка фото (просто отправляем обратно)
    @dp.message(lambda m: m.photo)
    async def on_photo(message: types.Message):
        file_id = message.photo[-1].file_id
        await message.answer_photo(file_id, caption="Вот твоя картинка обратно!")
        
    # для удобства в консоли пишем, что бот запущен
    print("Бот запущен... нажать Ctrl+C для остановки.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
