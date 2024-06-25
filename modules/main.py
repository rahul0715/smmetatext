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

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Hi!\n\nGive /Leo ♌️ Command to Download From a Text file.\n")

@bot.on_message(filters.command("Restart"))
async def restart_handler(_, m):
    await m.reply_text("**Restarted**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["Leo"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('Hi\n\nTo Download A Text File Send Here » ')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"Error reading file: {str(e)}")
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
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except Exception:
        res = "UN"

    await editable.edit("Enter A Caption To Add Otherwise Send `no`")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'no':
        MR = highlighter
    else:
        MR = raw_text3

    await editable.edit("Now Send the **Thumb URL**\nEg » `https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg`\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + V
            
            # Check if the URL is a CPVOD link and fetch the actual URL using the API
            if "tencdn.classplusapp" in url or "videos.classplusapp" in url or "d26g5bnklkwsh4.cloudfront.net" in url or "d1d34p8vz63oiq.cloudfront.net" in url:
                fetch_url_api = f"https://noxapi-0a195c5b9f8f.herokuapp.com/fetch_urls/{url}"
                response = requests.get(fetch_url_api)
                if response.status_code == 200:
                    url = response.json()['url']

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # Rest of the download logic remains unchanged

    except Exception as e:
        await m.reply_text(f"Error during download: {str(e)}")

    await m.reply_text("Done Leo♌️")

bot.run()
