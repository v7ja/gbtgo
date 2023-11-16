from pyrogram import Client,filters,idle
from pyrogram.types import InlineKeyboardButton,Message,InlineKeyboardMarkup,CallbackQuery
from OpsAi import Ai
from io import BytesIO

from aiohttp import ClientSession
import sys
import traceback
from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

OWNER_ID = 5565674333

API_ID = 14170449
API_HASH = "03488b3c030fe095667e7ca22fe34954"
TOKEN = "6696024805:AAGzVeaJIp6SzVH3CSviKGiLKU5RHN16PCw"


app = Client("Test"+TOKEN.split(":")[0],API_ID,API_HASH,bot_token=TOKEN)

app.start()

Mode_Name = []


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result

def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "ERROR | {} | {}\n\n {} \n\n{}\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await Client.send_message(OWNER_ID, x)
            raise err

    return capture


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ClientSession().post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image




@app.on_message(filters.command("Art"))
@capture_err
async def carbon_func(c:Client, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            txt = message.reply_to_message.text
        else:
            return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    else:
        try:
            txt = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    m = await message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...")
    carbon = await make_carbon(txt)
    await m.edit_text("ᴜᴩʟᴏᴀᴅɪɴɢ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ...")
    await c.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"» ʀᴇᴏ‌ᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}",
    )
    await m.delete()
    carbon.close()
	
@app.on_message(filters.private,group=1)
async def StartMsg(c:Client,m:Message):
	text = m.text
	Msg = f"Hi {m.from_user.mention} ! I'm ChatGPT bot implemented with OpenAI API 🤖"
	Msg2 = f"Hi {m.from_user.mention} ! I'm ChatGPT bot implemented with OpenAI API 🤖\nSelect chat mode (15 modes available):"
	if text == "/start":
		await app.send_message(chat_id=m.chat.id,text =Msg)
		FirstMsg = InlineKeyboardMarkup([
		[InlineKeyboardButton("General Assistant 👨‍💻",callback_data="GA")],
		[InlineKeyboardButton("Code Assistant 👩‍💻",callback_data="CA")],
		[InlineKeyboardButton("Artist 🕵️‍♀️",callback_data="ART")],
		[InlineKeyboardButton("English Tutor 🧏‍♂️",callback_data="ENTU")],
		[InlineKeyboardButton("Startup Idea General 🫁",callback_data="STUP")],
		[InlineKeyboardButton("»",callback_data="Next1")]
		])
		await app.send_message(chat_id=m.chat.id,text = Msg2,reply_markup=FirstMsg)

@app.on_message(filters.private,group=4)
async def echo(c:Client, m:Message):
    if m.text == "/start":
    	print("Hello")
    else:
    	a = m.text
    	s = Ai(query = a)
    	await app.send_message(chat_id=m.chat.id, text=s.chat())
		
@app.on_callback_query(group=3)
async def use(c:Client, query: CallbackQuery):
	FirstMsg = InlineKeyboardMarkup([
		[InlineKeyboardButton("General Assistant 👨‍💻",callback_data="GA")],
		[InlineKeyboardButton("Code Assistant 👩‍💻",callback_data="CA")],
		[InlineKeyboardButton("Artist 🕵️‍♀️",callback_data="ART")],
		[InlineKeyboardButton("English Tutor 🧏‍♂️",callback_data="ENTU")],
		[InlineKeyboardButton("Startup Idea General 🫁",callback_data="STUP")],
		[InlineKeyboardButton("»",callback_data="Next1")]
		])
		
	TwoMsg = InlineKeyboardMarkup([
	[InlineKeyboardButton("Text improver 📃",callback_data="TexIm")],
	[InlineKeyboardButton("Psychologist 🧠",callback_data="PSY")],
	[InlineKeyboardButton("Elon Musk 💁‍♂️",callback_data="ELMU")],
	[InlineKeyboardButton("Motivator 🕯",callback_data="MOT")],
	[InlineKeyboardButton("Money Maker 🪙",callback_data="MOMA")],
	[InlineKeyboardButton("«",callback_data="Back1"),
	InlineKeyboardButton("»",callback_data="Next2")]
	])
	
	ThreeMsg = InlineKeyboardMarkup([
	[InlineKeyboardButton("SQL Assistant 📊",callback_data="SQLAss")],
	[InlineKeyboardButton("Travel Guide 📲",callback_data="TraGu")],
	[InlineKeyboardButton("Rick Sanchez (Rick and Morty)",callback_data="Rick")],
	[InlineKeyboardButton("Accountant 🧮",callback_data="Acco")],
	[InlineKeyboardButton("Movie Expert 🎥",callback_data="Movie")],
	[InlineKeyboardButton("«",callback_data="Back2")]
	])
	
	data = query.data
	Msg = f"Hi {query.from_user.mention} ! I'm ChatGPT bot implemented with OpenAI API 🤖\nSelect chat mode (15 modes available):"
	
	if data == "Next1":
		await query.edit_message_text(Msg,reply_markup=TwoMsg)
	
	if data == "Next2":
		await query.edit_message_text(Msg,reply_markup=ThreeMsg)
		
	if data == "Back1":
		await query.edit_message_text(Msg,reply_markup=FirstMsg)
		
	if data == "Back2":
		await query.edit_message_text(Msg,reply_markup=TwoMsg)
	

	
@app.on_callback_query(group=2)
async def response(c:Client, query: CallbackQuery):
		data = query.data
		if data == "GA":
		    Mode_Name.clear()
		    Mode_Name.append("General Assistant")
		    await query.message.reply("Hi, I'm **General Assistant**. How can I help you?",quote=True)
			
		
		if data == "CA":
			Mode_Name.clear()
			Mode_Name.append("Code Assistant")
			await query.message.reply("Hi, I'm **Code Assistant**. How can I help you?",quote=True)
		
		if data == "ART":
			Mode_Name.clear()
			Mode_Name.append("Artist")
			await query.message.reply("Hi, I'm **Artist.** I'll draw anything you write me\nto use `/Art + Text` or reply text",quote=True)
			
		if data == "ENTU":
			Mode_Name.clear()
			Mode_Name.append("English Tutor")
			await query.message.reply("Hi, I'm **English Tutor**. How can I help you?",quote=True)
			
		if data == "STUP":
			Mode_Name.clear()
			Mode_Name.append("Startup Idea General")
			await query.message.reply("Hi, I'm **Startup Idea Generator**. How can I help you?",quote=True)
			
		########
		if data == "TexIm":
			Mode_Name.clear()
			Mode_Name.append("Text improver")
			await query.message.reply("Hi, I'm **Text Improver**. Send me any text – I'll improve it and correct all the mistakes",quote=True)
		
		if data == "PSY":
			Mode_Name.clear()
			Mode_Name.append("Psychologist")
			await query.message.reply("Hi, I'm **Psychologist.** How can I help you?",quote=True)
		
		if data == "ELMU":
			Mode_Name.clear()
			Mode_Name.append("Elon Musk")
			await query.message.reply("Hi, I'm **Elon Musk**, CEO of Tesla, Twitter and SpaceX. Let's talk about space, electric cars, and the future!",quote=True)
		
		if data == "MOT":
			Mode_Name.clear()
			Mode_Name.append("Motivator")
			await query.message.reply("Hi, I'm **Motivator**. How can I help you?",quote=True)
			
		if data == "MOMA":
			Mode_Name.clear()
			Mode_Name.append("Money Maker")
			
			await query.message.reply("Hi, I'm **Money Maker**. My goal it to turn your capital initial into as much money as possible. I will tell you specific steps, what to do to make money.",quote=True)
			
		########
		if data == "SQLAss":
			Mode_Name.clear()
			Mode_Name.append("SQL Assistant")
			await query.message.reply("Hi, I'm **SQL Assistant**. How can I help you?",quote=True)
			
		if data == "TraGu":
			Mode_Name.clear()
			Mode_Name.append("Travel Guide")
			await query.message.reply("Hi, I'm **Travel Guide**. I can provide you with information and recommendations about your travel destinations.",quote=True)
			
		if data == "Rick":
			Mode_Name.clear()
			Mode_Name.append("Rick Sanchez (Rick and Morty)")
			await query.message.reply("Hey, I'm **Rick Sanchez** from Rick and Morty. Let's talk about science, dimensions, and whatever else you want!",quote=True)
			
		if data == "Acco":
			Mode_Name.clear()
			Mode_Name.append("Accountant")
			await query.message.reply("Hi, I'm **Accountant**. How can I help you?",quote=True)
			
		if data == "Movie":
			Mode_Name.clear()
			Mode_Name.append("Movie Expert")
			await query.message.reply("Hi, How can I help you?",quote=True)
			
		
print("App Is Run....")
idle()
