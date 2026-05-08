import asyncio
import ssl
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

BOT_TOKEN = '8653683580:AAH81AISKRGOZrQwK8wipm7DGIC8UyQWeRI'  # ВСТАВЬ СВОЙ ТОКЕН

# Отключаем проверку SSL (временно, для теста)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class CustomSession:
    def __init__(self):
        self.connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=self.connector)
    
    async def close(self):
        await self.session.close()

# Создаем бота с кастомной сессией
from aiogram.client.session.aiohttp import AiohttpSession
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("✅ Бот работает! Отправь /help для списка команд")

@dp.message(Command('get_photo_id'))
async def get_photo_id(message: Message):
    await message.answer("📸 Отправь мне фотографию")

@dp.message(lambda msg: msg.photo)
async def get_photo(msg: Message):
    photo = msg.photo[-1]
    await msg.answer(f"✅ file_id: `{photo.file_id}`", parse_mode='Markdown')

@dp.message(Command('help'))
async def help_cmd(msg: Message):
    await msg.answer("/get_photo_id - получить ID фото\n/start - начало")

async def main():
    try:
        print("Запуск бота...")
        me = await bot.get_me()
        print(f"✅ Бот запущен: @{me.username}")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(main())