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
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

# Initialize bot
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@bot.on_message(filters.command(["start"]))
async def start(_, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/1d0c6fe5961f466d596fa.jpg",
        caption="**𝙷𝚒!**\n\n**𝙶𝚒𝚟𝚎 /Leo ♌️ 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 T𝚘 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚛𝚘𝚖 A 𝚃𝚎𝚡𝚝 F𝚒𝚕𝚎.**🎓✨",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/tigerxy09"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/tigerxy09")
            ]
        ])
    )

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
    except Exception as e:
        await m.reply_text(f"Invalid File Input. Error: {e}")
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
        res_map = {
            "144": "256x144",
            "240": "426x240",
            "360": "640x360",
            "480": "854x480",
            "720": "1280x720",
            "1080": "1920x1080"
        }
        res = res_map.get(raw_text2, "UN")
    except Exception:
        res = "UN"

    await editable.edit("Enter A Caption To Add Otherwise Send **no**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = "️ ⁪⁬⁮⁮⁮"
    MR = highlighter if raw_text3.lower() == 'no' else raw_text3

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
        thumb = "no"

    count = int(raw_text) if len(links) > 1 else 1

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url:
                headers = {
                    'Host': 'api.classplusapp.com',
                    'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTI0NzM1ODc2LCJvcmdJZCI6NDE4OTYxLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTkwMjQ1NTQ1NzYiLCJuYW1lIjoiUmFodSIsImVtYWlsIjoicmFodWxjaG91aGFuMDc4MTVAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOmZhbHNlLCJvcmdDb2RlIjoiZXV0cWQiLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiYjQwNDAxZTQ5MjFmM2IwZmFjMzM2OTQ3MDUxZTIiLCJpYXQiOjE3MjAzMzI4ODksImV4cCI6MTcyMDkzNzY4OX0.aMMH3B852Gu9Sof4AkXfHZsxgG0v53o00SNrzagnVpQgfsw_6b4ZHvqIFQ7dSBbU',
                    'user-agent': 'Mobile-Android',
                    'app-version': '1.4.37.1',
                    'api-version': '18',
                    'device-id': '5d0d17ac8b3c9f51',
                    'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30',
                    'accept-encoding': 'gzip'
                }
                response = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers)
                url = response.json().get('url')

            elif 'd26g5bnklkwsh4.cloudfront.net' in url or 'd1d34p8vz63oiq.cloudfront.net' in url:
                id = url.split("/")[-2]
                url = f"https://penpencilvod.pc.cdn.bitgravity.com/{id}/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]" if "youtu" in url else f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif 'd1wy033kfw4qbc.cloudfront.net' in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" --referer "https://iasscore.edugyaan.com/" -o "{name}.mp4"'
            elif 'penpencilvod.pc.cdn.bitgravity.com' in url:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header authorization:"Bearer YOUR_BEARER_TOKEN"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'** {str(count).zfill(3)}.** {name1}{MR}♌️.mkv\n\n**Batch Name :** {raw_text0}\n\n**Downloaded By** : **{MR}**'
                cc1 = f'** {str(count).zfill(3)}.** {name1}{MR}♌️.pdf \n\n**Batch Name :** {raw_text0}\n\n**Downloaded By** : **{MR}**'

                if "drive" in url:
                    cc = f'** {str(count).zfill(3)}.** {name1}{MR}♌️.mp4 \n\n**Batch Name :** {raw_text0}\n\n**Downloaded By** : **{MR}**'
                filename = f'{name}.mp4'

                duration_cmd = f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{filename}"'
                duration = subprocess.getoutput(duration_cmd)

                thumbnail = "thumb.jpg" if thumb != "no" else None

                await m.reply_video(
                    video=f"{name}.mp4",
                    duration=int(float(duration)),
                    caption=cc,
                    supports_streaming=True,
                    thumb=thumbnail,
                    quote=True,
                    progress=progress_bar,
                )

            except Exception as e:
                await m.reply_text(f"Error uploading {name}.mp4: {str(e)}")

            count += 1

    except FloodWait as e:
        await asyncio.sleep(e.x)
    except Exception as e:
        await m.reply_text(f"Error downloading video: {str(e)}")

# Start the bot
bot.run()
