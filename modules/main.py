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

# Function to fetch the selected URL based on priority
def fetch_selected_url(url):
    if "tencdn.classplusapp" in url and "videos.classplusapp" in url and "media-cdn.classplusapp.com" in url:
        try:
            # Make request to fetch signed URL
            r1 = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTI0NzM1ODc2LCJvcmdJZCI6NDE4OTYxLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTkwMjQ1NTQ1NzYiLCJuYW1lIjoiUmFodSIsImVtYWlsIjoicmFodWxjaG91aGFuMDc4MTVAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOmZhbHNlLCJvcmdDb2RlIjoiZXV0cWQiLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiYjQwNDAxZTQ5MjFmM2IwZmFjMzM2OTQ3MDUxZTIiLCJpYXQiOjE3MjAzMzI4ODksImV4cCI6MTcyMDkzNzY4OX0.aMMH3B852Gu9Sof4AkXfHZsxgG0v53o00SNrzagnVpQgfsw_6b4ZHvqIFQ7dSBbU'})

            # Extract signed URL from response
            signed_url = r1.json()['url']

            # Fetch content from signed URL
            r2 = requests.get(signed_url, headers={"X-CDN-Tag": "empty"}).text

            # Define regex pattern to match URLs in playlist
            pattern = r'^(\d+)/\1p\.m3u8(.*)$'

            # Finding matches in the playlist
            matches = re.findall(pattern, r2, flags=re.MULTILINE)

            # Priority order for selection
            priority_order = ['720', '480', '360']

            # Selecting the first matched URL based on priority
            selected_url = None
            for priority in priority_order:
                for match in matches:
                    if match[0] == priority:
                        selected_url = f"{match[0]}/{match[0]}p.m3u8{match[1]}"
                        break
                if selected_url:
                    break

            # Constructing the final URL if selected
            if selected_url:
                final_url = f"{url.replace('master.m3u8', '')}{selected_url}"
                return final_url
            else:
                return None
        
        except Exception as e:
            print(f"Error fetching or processing URL: {e}")
            return None
    else:
        print("URL does not match required domains.")
        return None


bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)

@bot.on_message(filters.command(["start"]))
async def start(_, message):
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

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com","youtube.com")
            if 'https://tencdn.classplusapp.com/courses' not in links[i]:
                await bot.send_message(
                    chat_id=m.chat.id,
                    text='Error Processing.',

                )

            else:
                s = await bot.send_message(
                    chat_id=m.chat.id,
                    text="🎓The file is being uploaded...",
                    reply_to_message_id=m.message_id
                )
              
                try:
                    if thumb != "no":
                        await bot.send_document(
                            chat_id=m.chat.id,
                            document=V,
                            thumb=thumb,
                            caption=MR,
                            disable_notification=True,
                            progress=progress_bar,
                            reply_to_message_id=m.message_id
                        )
                    else:
                        await bot.send_document(
                            chat_id=m.chat.id,
                            document=V,
                            caption=MR,
                            disable_notification=True,
                            progress=progress_bar,
                            reply_to_message_id=m.message_id
                        )
                    await s.delete()
                except Exception:
                    pass

    except Exception as e:
        await bot.send_message(m.chat.id, str(e))


if __name__ == "__main__":
    bot.run()

