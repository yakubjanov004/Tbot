from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State,StatesGroup
import asyncio
import logging
from db import create_user, info_users,info_usernames


TOKEN = "6858399276:AAF3PaCiVmqnOcZjLfRqdfGsMsB7MM87wFo"
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

class SavolUchun(StatesGroup):
    savol = State()

def start_buttons() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text="Bot haqida🙂")
    button_2 = KeyboardButton(text="Rasm")
    button_3 = KeyboardButton(text="Link📎")
    button_4 = KeyboardButton(text="Nmadir")
    button_5 = KeyboardButton(text="Botga start berganlar!")
    button_6 = KeyboardButton(text="Mening ma'lumotlarim")
    button_7 = KeyboardButton(text="Savollar bo'lsa😁")

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2],
            [button_3, button_4],
            [button_5, button_6],
            [button_7]
        ], resize_keyboard=True
    )
    return reply_buttons

def link_buttons() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text="Telegram")
    button_2 = KeyboardButton(text="Instagram")
    button_3 = KeyboardButton(text="Facebook")
    button_4 = KeyboardButton(text="Telegram kanal")
    button_5 = KeyboardButton(text="Orqaga")

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2],
            [button_3, button_4],
            [button_5]
        ], resize_keyboard=True
    )
    return reply_buttons





# Update the corresponding message handler in bot.py
@dp.message(CommandStart())
async def start_button(message: Message, state: FSMContext):
    # Check if the user is already in the database
    user_info = info_users()
    user_exists = any(user[0] == message.from_user.username for user in user_info)
    if not user_exists:
        # If not in the database, add the user
        create_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        text = f"""
        Start bosildi!!!
        Username: @{message.from_user.username}
        Name: {message.from_user.first_name}
        Last name: {message.from_user.last_name}
        """
        await bot.send_message(chat_id=1978574076, text=text)
    else:
        await bot.send_message(chat_id=1978574076, text="User already exists in the database.")
        # Get usernames if the user has clicked /start before
        usernames = info_usernames()
        if usernames:
            print("Usernames:")
            print("\n".join(usernames))
        else:
            print("No users found in the database.")
    
    # Send the start buttons
    await message.answer("😊", reply_markup=start_buttons())






    

@dp.message(F.text == "Bot haqida🙂")
async def bot_haqida(message: Message): 
    await message.answer("Bu yerda bot nima qila olishi haqida yozilisi kerak edi...")


@dp.message(F.text == "Rasm")
async def rasm_chiqarish(message: Message): 
    await bot.send_photo(chat_id=1978574076, photo='https://www.befunky.com/images/prismic/5418fdb1-d4fd-4c3b-8ab9-e6eb9a5e7d82_photo-of-a-woman-with-green-hair-3886347-cartoonized-original.jpeg?auto=avif,webp&format=jpg&width=863')


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
    await message.answer("Xali telegram kanal yo'q...")

@dp.message(F.text == "Orqaga")
async def back(message: Message): 
    await message.answer(text="back🔙",reply_markup=start_buttons())





@dp.message(F.text == "Nmadir")
async def qanaqadir_funksiya(message: Message): 
    await message.answer("bu qanaqadir funksiya qo'shiladi...")


@dp.message(F.text == "Botga start berganlar!")
async def info_users3(message: types.Message):
    data = info_users()
    await message.answer("Username, First name, Last name")
    text = ""
    for user in data:
        text += f"@{user[0]},  {user[1]},  {user[2]}\n"

    await message.answer(text)
    await message.answer("Bu xammaga ko'rinadi")


    
    
    


@dp.message(F.text == "Mening ma'lumotlarim")
async def text_chiqarish(message: Message): 
    name = "Ulug'bek"
    age = 20
    tugilgan_kun = "03.02.2004"                       
    await message.answer(text=f"Ism: {name},\nYosh: {age},\nTug'ilgan sana: {tugilgan_kun}\n")


@dp.message(F.text == "Savollar bo'lsa😁")
async def savol(message: types.Message, state:FSMContext): 
    await message.answer("Savolingiz bo'lsa yuboring🙁😅")
    await state.set_state(SavolUchun.savol)

@dp.message(SavolUchun.savol)
async def set_savol(message: types.Message, state: FSMContext):
    await state.update_data(savol=message.text)
    data = await state.get_data()
    text = f"""
    Savol yuborishibti...
    ...
    Kimdan: @{message.from_user.username}   {message.from_user.first_name}   {message.from_user.last_name}
    ...
    {data['savol']}
    """
    await message.answer("Savol yuborildi...")
    await message.answer("Javob qaytarishga xarakat qilaman😌")
    await bot.send_message(chat_id=1978574076,text=text)

    


async def main():
    print("Bot muvaffaqiyatli ishga tushdi !!!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())