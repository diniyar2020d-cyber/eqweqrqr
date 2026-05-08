import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReactionTypeEmoji

BOT_TOKEN = 'потом'  # Замени на свой токен

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== 1. ПОЛУЧЕНИЕ ID ФОТОГРАФИИ ==========
@dp.message(Command('get_photo_id'))
async def get_photo_id_command(message: Message):
    await message.answer(
        "📸 Отправь мне **любую фотографию** (не файлом, а именно как фото),\n"
        "и я пришлю тебе её file_id и file_unique_id\n\n"
        "💡 file_id можно использовать для отправки этого фото в будущем"
    )

@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    # Берем самую большую доступную версию фото (последняя в списке)
    photo = message.photo[-1]
    
    # Формируем ответ
    response = (
        f"🖼 **Информация о фото:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📎 **file_id:**\n`{photo.file_id}`\n\n"
        f"🔑 **file_unique_id:**\n`{photo.file_unique_id}`\n\n"
        f"📏 **Размер:** {photo.width}x{photo.height}\n"
        f"⚖️ **Вес:** {photo.file_size} байт\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"✅ Скопируй file_id для использования в боте"
    )
    
    await message.answer(response, parse_mode='Markdown')

# ========== 2. ПОЛУЧЕНИЕ ID ПРЕМИУМ ЭМОДЗИ ==========
@dp.message(Command('get_emoji_id'))
async def get_emoji_id_command(message: Message):
    await message.answer(
        "😎 Отправь мне **премиум эмодзи** (кастомный эмодзи из Telegram Premium),\n"
        "и я покажу его ID и информацию\n\n"
        "⚠️ Обычные эмодзи (😂, ❤️, 👍) не подойдут — только Premium!"
    )

@dp.message(lambda message: message.text and message.text.startswith(':'))
async def handle_premium_emoji(message: Message):
    text = message.text
    
    # Проверяем, содержит ли сообщение кастомный эмодзи
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                emoji_id = entity.custom_emoji_id
                emoji_text = text[entity.offset:entity.offset + entity.length]
                
                response = (
                    f"✨ **Информация о Premium эмодзи:**\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🎭 **Эмодзи:** {emoji_text}\n"
                    f"🆔 **custom_emoji_id:**\n`{emoji_id}`\n"
                    f"━━━━━━━━━━━━━━━━━━━\n\n"
                    f"✅ Скопируй этот ID для отправки Premium эмодзи в боте"
                )
                
                await message.answer(response, parse_mode='Markdown')
                return
    
    # Если эмодзи не найден или это обычный эмодзи
    await message.answer("❌ Это не премиум эмодзи! Отправь кастомный эмодзи, который доступен только с Telegram Premium.")

# ========== 3. ДОПОЛНИТЕЛЬНО: ПОЛУЧЕНИЕ ID СТИКЕРА ==========
@dp.message(Command('get_sticker_id'))
async def get_sticker_id_command(message: Message):
    await message.answer("🎨 Отправь мне **стикер**, и я пришлю его file_id")

@dp.message(lambda message: message.sticker)
async def handle_sticker(message: Message):
    sticker = message.sticker
    
    response = (
        f"🎨 **Информация о стикере:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📎 **file_id:**\n`{sticker.file_id}`\n\n"
        f"🔑 **file_unique_id:**\n`{sticker.file_unique_id}`\n\n"
        f"📏 **Размер:** {sticker.width}x{sticker.height}\n"
        f"⚖️ **Вес:** {sticker.file_size} байт\n"
        f"😊 **Emoji:** {sticker.emoji or 'Нет'}\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"✅ Используй этот file_id для отправки стикера"
    )
    
    await message.answer(response, parse_mode='Markdown')

# ========== 4. КОМАНДА ПОМОЩИ ==========
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "🤖 **Бот для получения ID объектов**\n\n"
        "📸 **/get_photo_id** — Получить ID фотографии\n"
        "😎 **/get_emoji_id** — Получить ID Premium эмодзи\n"
        "🎨 **/get_sticker_id** — Получить ID стикера\n"
        "❓ **/help** — Эта справка\n\n"
        "💡 Как использовать:\n"
        "1. Нажми на нужную команду\n"
        "2. Отправь соответствующий объект (фото/эмодзи/стикер)\n"
        "3. Скопируй полученный ID"
    )

# ========== ЗАПУСК ==========
async def main():
    print("🚀 Бот запущен!")
    print("Команды:")
    print("  /get_photo_id - получить ID фото")
    print("  /get_emoji_id - получить ID премиум эмодзи")
    print("  /get_sticker_id - получить ID стикера")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())