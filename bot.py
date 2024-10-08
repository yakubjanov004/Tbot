from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio, random, logging, emoji, sqlite3, sys 
from contextlib import closing

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("bot.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )

TOKEN = "7143096410:AAEdYgERHb0_0UoJVPZFv-4a0kHBK5C6KXk"  
bot = Bot(TOKEN)
dp = Dispatcher()

def create_user(*args):
    with closing(sqlite3.connect('telegram_bot.db')) as connection:
        with closing(connection.cursor()) as cursor:
            sql = """INSERT INTO foydalanuvchilar_soni(username, first_name, last_name)
                     VALUES (?, ?, ?)"""
            cursor.execute(sql, args)
            connection.commit()

def info_users():
    with closing(sqlite3.connect('telegram_bot.db')) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT username, first_name, last_name FROM foydalanuvchilar_soni")
            return cursor.fetchall()

def info_usernames():
    with closing(sqlite3.connect('telegram_bot.db')) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT username FROM foydalanuvchilar_soni")
            return [row[0] for row in cursor.fetchall()]

def initialize_database():
    with closing(sqlite3.connect('telegram_bot.db')) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS foydalanuvchilar_soni(
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT
                )"""
            )
            connection.commit()

initialize_database()

def start_buttons() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Bot haqida🙂"), KeyboardButton(text="Rasm🔄")],
        [KeyboardButton(text="Link📎"), KeyboardButton(text="Rasm🙂")],
        [KeyboardButton(text="Botga start berganlar!"), KeyboardButton(text="Mening ma'lumotlarim")],
        [KeyboardButton(text="Video🔄"), KeyboardButton(text="vv")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def link_buttons() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Telegram"), KeyboardButton(text="Instagram")],
        [KeyboardButton(text="Facebook"), KeyboardButton(text="Telegram kanal")],
        [KeyboardButton(text="Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(CommandStart())
async def start_button(message: Message, state: FSMContext):
    user_info = info_users()
    user_exists = any(user[0] == message.from_user.username for user in user_info)
    if not user_exists:
        create_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await message.answer("😊", reply_markup=start_buttons())


@dp.message(F.text == "Bot haqida🙂")
async def bot_haqida(message: Message): 
    await message.answer(
        "😊 *Salom!*\n\n"
        "Bu bot orqali siz:\n\n"
        "1️⃣ Rasmlar almashishingiz 📸\n"
        "2️⃣ Foydali havolalarni ko'rishingiz 🔗\n"
        "3️⃣ Bot foydalanuvchilarini ko'rishingiz 👥\n"
        "4️⃣ Shaxsiy ma'lumotlaringizni ko'rishingiz mumkin 👤\n\n"
        "Bot oddiy echo emas! Men o'zim javob yozishim mumkin ✍️, "
        "shuningdek, bot emojilarga random emoji bilan avto javob qaytaradi! 🤖😊\n\n"
        "Bot shunchaki yaratilgan, va start bosgan foydalanuvchilarni saqlab boradi 📊."
    )

image_urls = [
    'https://w0.peakpx.com/wallpaper/344/317/HD-wallpaper-red-love-hearts-dark-neon-love-hearts-loveurhunny-pretty-thumbnail.jpg',
    'https://i.pinimg.com/originals/3b/62/0b/3b620b88711b4205e1274c603dbfbe7b.jpg',
    'https://www.classicdriver.com/sites/default/files/users/82800/cars_images/82800-887158-car-20220201_131557-1.jpg',
    'https://wallpapers.com/images/hd/black-and-white-heart-750-x-1332-background-7goeyde5jitleu3b.jpg',
    'https://dlcdnwebimgs.asus.com/gain/161DFF39-ECAE-48F6-B10E-52179600208F',
    'https://i.pinimg.com/736x/b9/6d/ba/b96dba2c130bfa40adb3928ca9c3d45c.jpg',
    'https://tuit.uz/logos/tuit_slide_two.jpg',
]

user_images = {}

@dp.message(F.text == "Rasm🔄")
async def rasm_chiqarish(message: Message):
    user_id = message.from_user.id

    if user_id not in user_images:
        user_images[user_id] = list(image_urls)  

    if not user_images[user_id]:  
        user_images[user_id] = list(image_urls)

    random_image_url = user_images[user_id].pop(0)  
    await bot.send_photo(chat_id=message.from_user.id, photo=random_image_url)

@dp.message(F.text == "Link📎")
async def link(message: Message): 
    await message.answer("Link...", reply_markup=link_buttons())

@dp.message(F.text == "Instagram")
async def instagram(message: Message): 
    await message.answer("Instagram⬇️")
    await message.answer("https://www.instagram.com/yakubjanov_004?igsh=MTBhMWYyZXVlaGgzZw==")

@dp.message(F.text == "Facebook")
async def facebook(message: Message): 
    await message.answer("Facebook⬇️")
    await message.answer("https://www.facebook.com/profile.php?id=100088112914912&mibextid=ZbWKwL")

@dp.message(F.text == "Telegram")
async def telegram(message: Message): 
    await message.answer("Telegram link⬇️")
    await message.answer("username: @yakubjanov_004")

@dp.message(F.text == "Telegram kanal")
async def telegram_channel(message: Message): 
    await message.answer("Telegram kanal link⬇️")
    await message.answer("https://t.me/Ali_dev004")
    await message.answer("Bu mening kanalim emas(!menda kanal yo'q!),\nlekin adminman😁")

@dp.message(F.text == "Orqaga")
async def back(message: Message): 
    await message.answer(text="back🔙", reply_markup=start_buttons())

image_urls1 = [
    'https://imgur.com/a/post-PUnUzb9',
    'https://imgur.com/a/8dy9SDB',
    'https://imgur.com/a/Bq38dmO',
    'https://imgur.com/a/FL7zxXO',
    'https://imgur.com/a/GWOTHQg',
    'https://imgur.com/a/kR11d9P',
    'https://imgur.com/a/XjB0xKL',
    'https://imgur.com/a/HKBGkxq',

]

user_images1 = {}

@dp.message(F.text == "Rasm🙂")
async def rasm_chiqarish(message: Message):
    user_id1 = message.from_user.id

    if user_id1 not in user_images1:
        user_images1[user_id1] = list(image_urls1)  

    if not user_images1[user_id1]:  
        user_images1[user_id1] = list(image_urls1)

    random_image_url1 = user_images1[user_id1].pop(0)  
    await bot.send_photo(chat_id=message.from_user.id, photo=random_image_url1)


video_urls = [
    'https://www.dropbox.com/scl/fi/auw17d6m0hp4890qud2e1/VID_20231118_084818_012.mp4?raw=1',
    'https://www.dropbox.com/scl/fi/xxkjd7iqo3ljnl07hf38l/20240712_224156.mp4?raw=1',
]

user_videos = {}

@dp.message(F.text == "Video🔄")
async def video_chiqarish(message: Message):
    user_id = message.from_user.id

    if user_id not in user_videos or not user_videos[user_id]:
        user_videos[user_id] = list(video_urls)
        random.shuffle(user_videos[user_id])

    random_video_url = user_videos[user_id].pop(0)
    try:
        await bot.send_video(chat_id=message.from_user.id, video=random_video_url)
    except Exception as e:
        await message.answer("Kechirasiz, videoni yuklashda xatolik yuz berdi.")


@dp.message(F.text == "Botga start berganlar!")
async def info_users3(message: types.Message):
    data = info_users()
    if data:
        text = "Username, First name\n\n"
        text += "\n".join(f"{idx+1}. @{user[0]}, {user[1]}" for idx, user in enumerate(data))
        await message.answer(text)
        await message.answer("Bu xammaga ko'rinadi!!!")


@dp.message(F.text == "Mening ma'lumotlarim")
async def text_chiqarish(message: Message): 
    name = "Ulug'bek"
    familiya = "Yoqubjonov"                       
    await message.answer(text=f"Ism: {name},\nFamiliya: {familiya}")

emoji_list = [
    "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃", "😉", "😊", "😇", 
    "🥰", "😍", "🤩", "😘", "😗", "☺️", "😚", "😙", "😋", "😛", "😜", "🤪", "😝", 
    "🤑", "🤗", "🤭", "🤫", "🤔", "🤐", "🤨", "😐", "😑", "😶", "😏", "😒", "🙄", 
    "😬", "😮‍💨", "🤥", "😌", "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕", "🤢", "🤮", 
    "🤧", "🥵", "🥶", "😵", "😵‍💫", "🤯", "🤠", "🥳", "😎", "🤓", "🧐", "😕", "😟", 
    "🙁", "☹️", "😮", "😯", "😲", "😳", "🥺", "😦", "😧", "😨", "😰", "😥", "😢", 
    "😭", "😱", "😖", "😣", "😞", "😓", "😩", "😫", "🥱", "😤", "😡", "😠", "🤬", 
    "😈", "👿", "💀", "☠️", "💩", "🤡", "👹", "👺", "👻", "👽", "👾", "🤖", "😺", 
    "😸", "😹", "🙊", "😼", "😽", "🙀", "😿", "😾", "🙈", "🙉", "🙊", "💋", "💌", 
    "💘", "💝", "💖", "💗", "💓", "💞", "💕", "💟", "❣️", "💔", "❤️‍🔥", "❤️‍🩹", 
    "❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍", "👋", "🤚", "🖐", "✋️", 
    "🖖", "🤟", "👌", "🤏", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", 
    "👇", "☝️", "👍", "👎", "✊️", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲", "🤝", 
    "🙏", "✍️"
]

def is_only_emoji(text):
    return all(char in emoji.EMOJI_DATA for char in text)

@dp.message()
async def handle_message(message: types.Message):
    text = message.text
    if is_only_emoji(text):
        random_emoji = random.choice(emoji_list)
        await message.answer(random_emoji)

async def main():
    logging.info("Bot polling rejimida ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  
    asyncio.run(main())