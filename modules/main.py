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
async def start(_,message):
  await message.reply_photo(photo="https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg", caption="**𝙷𝚒!**\n\n**𝙶𝚒𝚟𝚎 /Leo ♌️ 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 T𝚘 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚛𝚘𝚖 A 𝚃𝚎𝚡𝚝 F𝚒𝚕𝚎.**🎓✨",
                            reply_markup=InlineKeyboardMarkup([
                           
                [
                  InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/tigerxy09"),
                  InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/tigerxy09")
                ]
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
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
            # print(len(links)
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
    
    

    await editable.edit("Enter A Captio To Add Otherwise Send   **no**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'no':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now Send the **Thumb url**\nEg » ```https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg```\n\nor Send `no`")
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

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url:
                headers = {
                    'Host': 'api.classplusapp.com',
                    'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTI0NzM1ODc2LCJvcmdJZCI6NDE4OTYxLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTkwMjQ1NTQ1NzYiLCJuYW1lIjoiUmFodSIsImVtYWlsIjoicmFodWxjaG91aGFuMDc4MTVAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOmZhbHNlLCJvcmdDb2RlIjoiZXV0cWQiLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiYjQwNDAxZTQ5MjFmM2IwZmFjMzM2OTQ3MDUxZTIiLCJpYXQiOjE3MjAzMzI4ODksImV4cCI6MTcyMDkzNzY4OX0.aMMH3B852Gu9Sof4AkXfHZsxgG0v53o00SNrzagnVpQgfsw_6b4ZHvqIFQ7dSBbU',
                    'user-agent': 'Mobile-Android',
                    'app-version': '1.4.37.1',
                    'api-version': '18',
                    'device-id': 'f16be4e4dcd1b7c6',
                    'device-details': '2848^Google^google Pixel 6 Pro^12^^1',
                    'accept-encoding': 'gzip, deflate',
                    'Content-Type': 'application/json; charset=UTF-8',
                }

                params = {
                    'url': links[i][1],
                    'quality': "",
                    'videoResolution': res,
                }

                url = requests.get('https://api.classplusapp.com/cams/uploader/video/token/generate', params=params, headers=headers).json()["data"]["source"]

            # Download the video using yt-dlp
            download_command = f'yt-dlp -o "{path}/{raw_text0}/{i}.mp4" "{url}"'
            subprocess.run(download_command, shell=True)

            # Apply the watermark using ffmpeg
            watermark = "watermark.png"  # Path to your watermark image
            input_video = f"{path}/{raw_text0}/{i}.mp4"
            output_video = f"{path}/{raw_text0}/{i}_watermarked.mp4"
            watermark_command = f'ffmpeg -i "{input_video}" -i "{watermark}" -filter_complex "overlay=10:10" "{output_video}"'
            subprocess.run(watermark_command, shell=True)

            # Upload the watermarked video
            caption = MR
            if thumb == "no":
                await helper.send_video(bot, m, output_video, caption, "")
            else:
                await helper.send_video(bot, m, output_video, caption, "thumb.jpg")

            os.remove(input_video)
            os.remove(output_video)

    except Exception as e:
        await m.reply_text(str(e))


if __name__ == "__main__":
    bot.run()
