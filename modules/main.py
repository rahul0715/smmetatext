import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import api_id, api_hash, bot_token
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Function to handle video download from various APIs
async def handle_video_download(url: str, name: str, raw_text2: str, thumb: str):
    if "edukemy.com/videodetails/" in url:
        # Handle EDU_VIDEO API
        response = requests.get(url)
        video_data = response.json()
        video_url = video_data.get('video_url')
        if video_url:
            cmd = f'yt-dlp -f "b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba" "{video_url}" -o "{name}.mp4"'
            # Execute download command
            os.system(cmd)
            await bot.send_video(chat_id=m.chat.id, video=f'{name}.mp4', thumb=thumb, caption=f"**Name**: {name}\n**Resolution**: {raw_text2}")
            os.remove(f'{name}.mp4')
    elif "edukemy-v2-assets" in url or "visionias" in url:
        # Handle EDU_PDF and VISION_PDF
        try:
            pdf_url = url  # Assuming url is the direct link to the PDF
            response = requests.get(pdf_url)
            pdf_path = f"{name}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            await bot.send_document(chat_id=m.chat.id, document=pdf_path, caption=f"**Name**: {name}\n**Type**: PDF")
            os.remove(pdf_path)
        except Exception as e:
            await bot.send_message(chat_id=m.chat.id, text=f"**Error**: {str(e)}")
    else:
        # Handle other URLs with existing logic
        Show = f"**⥥ Downloading »**\n\n**Name »** `{name}\nQuality » {raw_text2}`\n\n**Url :** `{url}`"
        prog = await bot.send_message(chat_id=m.chat.id, text=Show)
        res_file = await helper.download_video(url, cmd, name)
        filename = res_file
        await prog.delete(True)
        await helper.send_vid(bot, m, f"** {str(count).zfill(3)}.** {name}♌️", filename, thumb, name, prog)

@bot.on_message(filters.command(["start"]))
async def start(_, message):
    await message.reply_photo(photo="https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg", caption="**𝙷𝚒!**\n\n**𝙶𝚒𝚟𝚎 /Leo ♌️ 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 T𝚘 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚛𝚘𝚖 A 𝚃𝚎𝚡𝚝 F𝚒𝚕𝚎.**🎓✨",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/tigerxy09"),
                                 InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/tigerxy09")]
                            ]))

@bot.on_message(filters.command("Restart"))
async def restart_handler(_, m):
    await m.reply_text("**Restarted**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["Leo"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('**Hi!**\n\n**To download a text file, send it here.** » 🎓✨')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"
    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split("://", 1) for i in content]
        os.remove(x)
    except:
        await m.reply_text("Invalid File Input.")
        os.remove(x)
        return

    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From Where You Want To Download Initial Is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("**Enter Resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    
    res = {"144": "256x144", "240": "426x240", "360": "640x360", "480": "854x480", "720": "1280x720", "1080": "1920x1080"}.get(raw_text2, "UN")

    await editable.edit("Enter A Caption To Add Otherwise Send   **no**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    MR = highlighter if raw_text3 == 'no' else raw_text3

    await editable.edit("Now Send the **Thumb url**\nEg » ```https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg```\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = "thumb.jpg" if raw_text6.startswith("http://") or raw_text6.startswith("https://") else "no"
    if thumb == "thumb.jpg":
        getstatusoutput(f"wget '{raw_text6}' -O 'thumb.jpg'")

    count = 1 if len(links) == 1 else int(raw_text)
    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + V

            await handle_video_download(url, f'{str(count).zfill(3)}) {links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()[:60]}', raw_text2, thumb)
            count += 1
            time.sleep(1)

    except Exception as e:
        await m.reply_text(f"**Downloading Interrupted**\n{str(e)}\n**Name**: {name}\n**Link**: `{url}`")
    await m.reply_text("Done Leo♌️")

bot.run()
