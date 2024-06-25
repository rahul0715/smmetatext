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
    bot_token=bot_token)


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
           await m.reply_text(f"Invalid File Input: {str(e)}")
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
    
    await editable.edit("Enter A Caption To Add Otherwise Send **no**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
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
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V
            
            # Integrate API call to modify the URL if needed
            fetch_url_api = f"https://noxapi-0a195c5b9f8f.herokuapp.com/fetch_urls/{url}"
            response = requests.get(fetch_url_api)
            
            if response.status_code == 200:
                url = response.json()['url']

            # Rest of your URL handling logic remains unchanged
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            # Continue with the rest of your URL processing logic
            # Add more conditions for different URL sources and their respective processing

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif 'd1wy033kfw4qbc.cloudfront.net' in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" --referer "https://iasscore.edugyaan.com/" -o "{name}.mp4"'
            elif 'penpencilvod.pc.cdn.bitgravity.com' in url :
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg2MjY2ODMuMzU0LCJkYXRhIjp7Il9pZCI6IjY2NjZlMWNlZjZhM2IzZTRlNzgyMjE1ZCIsInVzZXJuYW1lIjoiOTAyNDU1NDU3NiIsImZpcnN0TmFtZSI6IlJhaHVsIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlDb2RlIjoiNDIzIiwicm9sZSI6WyIxIl0sImlhdCI6MTYyNDYyNjY4M30.ZfBjZ-NNSHrckWS1pyfZaln-DXYrlhsC1LrC7YoCVwU" --force-generic-extractor'
            elif 'sec.ch9.ms' in url :
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header "x-ms-via-two: [RC1]" -o "{name}.mp4" --add-header referer:"https://sec.ch9.ms/sessions/build/2021/KEY" --add-header "x-ms-via-two: [RC1]" --force-generic-extractor'
            elif 'request.euwest.services' in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" -o "{name}.mp4" --add-header referer:"https://id.visionias.in/" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg2MjY2ODMuMzU0LCJkYXRhIjp7Il9pZCI6IjY2NjZlMWNlZjZhM2IzZTRlNzgyMjE1ZCIsInVzZXJuYW1lIjoiOTAyNDU1NDU3NiIsImZpcnN0TmFtZSI6IlJhaHVsIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlDb2RlIjoiNDIzIiwicm9sZSI6WyIxIl0sImlhdCI6MTYyNDYyNjY4M30.ZfBjZ-NNSHrckWS1pyfZaln-DXYrlhsC1LrC7YoCVwU" --force-generic-extractor'
            elif "soc" in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header "x-ms-via-two: [RC1]" -o "{name}.mp4" --add-header referer:"https://api.xl" -o "{name}.mp4" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg2MjY2ODMuMzU0LCJkYXRhIjp7Il9pZCI6IjY2NjZlMWNlZjZhM2IzZTRlNzgyMjE1ZCIsInVzZXJuYW1lIjoiOTAyNDU1NDU3NiIsImZpcnN0TmFtZSI6IlJhaHVsIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlDb2RlIjoiNDIzIiwicm9sZSI6WyIxIl0sImlhdCI6MTYyNDYyNjY4M30.ZfBjZ-NNSHrckWS1pyfZaln-DXYrlhsC1LrC7YoCVwU" --force-generic-extractor'
            elif "soc" in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header "x-ms-via-two: [RC1]" -o "{name}.mp4" --add-header referer:"https://api.xl" -o "{name}.mp4" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg2MjY2ODMuMzU0LCJkYXRhIjp7Il9pZCI6IjY2NjZlMWNlZjZhM2IzZTRlNzgyMjE1ZCIsInVzZXJuYW1lIjoiOTAyNDU1NDU3NiIsImZpcnN0TmFtZSI6IlJhaHVsIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlDb2RlIjoiNDIzIiwicm9sZSI6WyIxIl0sImlhdCI6MTYyNDYyNjY4M30.ZfBjZ-NNSHrckWS1pyfZaln-DXYrlhsC1LrC7YoCVwU" --force-generic-extractor'
            elif 'd1wy033kfw4qbc.cloudfront.net' in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" --referer "https://iasscore.edugyaan.com/" -o "{name}.mp4"'
            elif 'penpencilvod.pc.cdn.bitgravity.com' in url :
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg2MjY2ODMuMzU0LCJkYXRhIjp7Il9pZCI6IjY2NjZlMWNlZjZhM2IzZTRlNzgyMjE1ZCIsInVzZXJuYW1lIjoiOTAyNDU1NDU3NiIsImZpcnN0TmFtZSI6IlJhaHVsIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlDb2RlIjoiNDIzIiwicm9sZSI6WyIxIl0sImlhdCI6MTYyNDYyNjY4M30.ZfBjZ-NNSHrckWS1pyfZaln-DXYrlhsC1LrC7YoCVwU" --force-generic-extractor'
            elif "sec.ch9.ms" in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header "x-ms-via-two: [RC1]" --add-header referer:"https://sec.ch9.ms/sessions/build/2021/KEY" --add-header "x-ms-via-two: [RC1]" --force-generic-extractor'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --force-generic-extractor'

            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            await m.reply_photo(
                photo = thumb,
                caption = MR,
                reply_to_message_id = m.message_id,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Search ️", url=f"{url}")],
                        [InlineKeyboardButton(text="Pen Drive Google Play Store", url="https://ift.tt/3gzdthh")],
                    ]
                )
            )

            count += 1

    except Exception as e:
        await m.reply_text(f"Error Occurred {str(e)}")


@bot.on_message(filters.command("pause"))
async def account_login(bot: Client, m: Message):
    os.system("killall -s SIGSTOP yt-dlp")
    await m.reply_text("**Paused**❄️", True)


@bot.on_message(filters.command("unpause"))
async def account_login(bot: Client, m: Message):
    os.system("killall -s SIGCONT yt-dlp")
    await m.reply_text("**Resumed**🚦", True)


@bot.on_message(filters.command("cancel"))
async def account_login(bot: Client, m: Message):
    os.system("killall -s SIGINT yt-dlp")
    await m.reply_text("**Cancelled**🛑", True)

bot.run()
