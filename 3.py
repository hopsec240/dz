import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# ========== КАТЕГОРИИ И СЛОВА ==========
CATEGORIES = {
    "🏠 Дом": ["гостиная", "кухня", "ванная", "спальня", "гараж", "подвал", "балкон", "коридор"],
    "🏢 Офис": ["директор", "секретарь", "кухня", "принтер", "кофеварка", "конференция", "кулер", "отдел кадров"],
    "✈️ Аэропорт": ["стойка регистрации", "багаж", "табло", "посадка", "пилот", "паспорт", "дьюти фри", "зал ожидания"],
    "🏨 Отель": ["лобби", "номер люкс", "лифт", "ресепшн", "шведский стол", "консьерж", "мини-бар", "прачечная"],
    "🎢 Парк": ["аттракцион", "мороженое", "фонтан", "прокат лодок", "лавочка", "тир", "американские горки", "карусель"],
    "🍕 Ресторан": ["меню", "шеф-повар", "столик", "официант", "винная карта", "кухня", "десерт", "бронь"],
    "🚂 Поезд": ["проводник", "плацкарт", "купе", "ресторан", "станция", "билет", "багаж", "туалет"],
    "🎭 Театр": ["сцена", "зрительный зал", "гримерка", "партер", "гардероб", "антракт", "аплодисменты", "билетер"],
    "🏛️ Музей": ["экспонат", "экскурсовод", "зал живописи", "скульптура", "сувенирный киоск", "касса", "гардероб", "кафе"],
    "🏖️ Пляж": ["шезлонг", "зонт", "спасатель", "море", "волна", "пляжный волейбол", "кафе", "душ"]
}

TOKEN = "8664734049:AAGRaKzKHP0Wehhro5xVsAZNIs1FJXVn6SQ"  # Вставь свой токен!

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

active_games = {}

def get_categories_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for cat in CATEGORIES.keys():
        keyboard.add(InlineKeyboardButton(cat, callback_data=f"cat_{cat}"))
    return keyboard

def get_join_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("✅ Я играю!", callback_data="join_game"))
    return keyboard

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🎮 Начать новую игру", callback_data="new_game"))
    keyboard.add(InlineKeyboardButton("❌ Закончить игру", callback_data="end_game"))
    return keyboard

@dp.message_handler(commands=['start', 'game'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        await message.reply("👋 Привет! Добавь меня в группу и используй /game")
    else:
        await message.reply(
            "🎲 *Игра Шпион*\n\nНажми на кнопку, чтобы начать игру",
            reply_markup=get_start_keyboard(),
            parse_mode='Markdown'
        )

@dp.callback_query_handler(lambda c: True)
async def button_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    await callback_query.answer()
    
    if data == "new_game":
        await callback_query.message.edit_text(
            "🎯 *Выберите категорию игры:*",
            reply_markup=get_categories_keyboard(),
            parse_mode='Markdown'
        )
    
    elif data.startswith("cat_"):
        category = data[4:]
        words = CATEGORIES.get(category, [])
        
        active_games[chat_id] = {
            "category": category,
            "words": words,
            "players": [],
            "status": "waiting_players",
            "message_id": callback_query.message.message_id
        }
        
        await callback_query.message.edit_text(
            f"📚 *Категория:* {category}\n\n"
            f"👇 *Нажми на кнопку, чтобы присоединиться!*\n"
            f"⏱️ У тебя есть 60 секунд.",
            reply_markup=get_join_keyboard(),
            parse_mode='Markdown'
        )
        
        asyncio.create_task(join_timer(callback_query.message, chat_id))
    
    elif data == "join_game":
        game = active_games.get(chat_id)
        if not game or game["status"] != "waiting_players":
            await callback_query.answer("Игра уже началась или закончилась!")
            return
        
        if user_id not in game["players"]:
            game["players"].append(user_id)
            await callback_query.answer("✅ Ты присоединился к игре!")
            
            players_count = len(game["players"])
            try:
                await bot.edit_message_text(
                    text=f"📚 *Категория:* {game['category']}\n\n"
                         f"👥 *Игроков присоединилось:* {players_count}\n\n"
                         f"👇 *Присоединяйся!*\n"
                         f"⏱️ Осталось время...",
                    chat_id=chat_id,
                    message_id=game["message_id"],
                    reply_markup=get_join_keyboard(),
                    parse_mode='Markdown'
                )
            except:
                pass
        else:
            await callback_query.answer("Ты уже в игре!")
    
    elif data == "end_game":
        if chat_id in active_games:
            del active_games[chat_id]
        await callback_query.message.edit_text("❌ Игра отменена.")

async def join_timer(message, chat_id):
    await asyncio.sleep(60)
    
    game = active_games.get(chat_id)
    if game and game["status"] == "waiting_players":
        if len(game["players"]) < 3:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Недостаточно игроков (нужно минимум 3). Игра отменена."
            )
            del active_games[chat_id]
        else:
            await start_game(chat_id)

async def start_game(chat_id):
    game = active_games.get(chat_id)
    if not game:
        return
    
    game["status"] = "playing"
    players = game["players"]
    words = game["words"]
    
    available_words = words.copy()
    random.shuffle(available_words)
    spy_index = random.randint(0, len(players) - 1)
    
    for i, player_id in enumerate(players):
        if i == spy_index:
            word = "🕵️‍♂️ ШПИОН"
            text = f"🔍 *Ты - ШПИОН!*\n\nТвоя задача - понять, где все находятся, но не выдать себя.\nКатегория: *{game['category']}*"
        else:
            if available_words:
                word = available_words.pop(0)
            else:
                word = random.choice(words)
            text = f"🎯 *Твое слово:* {word}\n\nКатегория: *{game['category']}*\nНе называй слово прямо! Задавай наводящие вопросы."
        
        try:
            await bot.send_message(chat_id=player_id, text=text, parse_mode='Markdown')
        except Exception as e:
            print(f"Не удалось отправить сообщение {player_id}: {e}")
    
    players_mentions = []
    for player_id in players:
        try:
            user = await bot.get_chat_member(chat_id, player_id)
            players_mentions.append(f"@{user.user.username}" if user.user.username else f"[игрок](tg://user?id={player_id})")
        except:
            players_mentions.append(f"[игрок](tg://user?id={player_id})")
    
    await bot.send_message(
        chat_id=chat_id,
        text=f"🎲 *ИГРА НАЧАЛАСЬ!*\n\n👥 Игроки: {', '.join(players_mentions)}\n📚 Категория: {game['category']}\n\n🕵️ Один из вас - шпион!\n💬 Задавайте вопросы друг другу.\n⭐ После обсуждения напишите /vote, чтобы проголосовать.",
        parse_mode='Markdown'
    )

@dp.message_handler(commands=['vote'])
async def vote(message: types.Message):
    chat_id = message.chat.id
    
    game = active_games.get(chat_id)
    if not game or game["status"] != "playing":
        await message.reply("Сейчас нет активной игры.")
        return
    
    spy_id = game["players"][game.get("spy_index", 0)]
    
    await message.reply(
        f"🕵️ *Шпионом был* [игрок](tg://user?id={spy_id})\n\nИгра окончена! Спасибо за игру! 🎉",
        parse_mode='Markdown'
    )
    
    del active_games[chat_id]

@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message):
    chat_id = message.chat.id
    if chat_id in active_games:
        del active_games[chat_id]
    await message.reply("Игра отменена.")

if __name__ == '__main__':
    print("🤖 Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
