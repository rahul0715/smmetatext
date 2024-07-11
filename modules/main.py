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

                    # Code For Txt Extract

@bot.on_message(filters.command(["start"]) & filters.chat(sudo_group))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id}) \n use /txt to download txt\n")

@bot.on_message(filters.command("stop") & filters.chat(sudo_group))
async def restart_handler(_, m):
    await m.reply_text("**STOPPED**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart") & (filters.chat(sudo_group)))
async def restart_handler(_, m):
    await m.reply_text("**Restarted! बस करो Bro अब थक गया हु 🥹**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["txt"]) & filters.chat(sudo_group))
async def txt_handler(bot: Client, m: Message):
    
    if batch != []:
        await m.reply("**Already Process Running**", quote=True)
        return
    else:
        batch.append(f'{m.from_user.id}')
        editable = await m.reply_text(f"**Hello <b> [{m.from_user.first_name}](tg://user?id={m.from_user.id}),"\
        "\n\n**I'm Txt Uploader Bot**"\
            "\n\nSend TXT  file :-</b>**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        #await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit =  "**Downloaded by :**" + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        # credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"

        
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
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
   
    await editable.edit(f"**Total Links in File are :-** `{len(links)}`\n\n**Send index no. 1 or where you want to download**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0
    
    await editable.edit("**Enter Video Resolution**")
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
            res = "NA"
    except Exception:
            res = "NA"

    await editable.edit("**Enter Your Name or send `de` for use default or** skip ")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'de':
        CR = credit
    elif raw_text3 == 'skip':
        CR = ''
    else:
        CR = f'Downloaded By: {raw_text3}'
      
    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    thumb = input6.text

    await editable.edit("**Send the chat id where You want to forward Video or Send** `de` **for default Channel**")
    input69 = message = await bot.listen(editable.chat.id)
    chat_id = input69.text
    await input69.delete(True)
    if chat_id == 'de':
        chat_id = -1002184158958
    else:
        chat_id = chat_id

    await editable.delete()

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
            await bot.send_message(chat_id=int(chat_id), text=f"**𝐁𝐀𝐓𝐂𝐇 ➨ {b_name}**\n**TOTAL FILE ➨** **{len(links)}**")
            for i in range(count - 1, len(links)):

                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="101", "Not=A?Brand";v="99"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

                
                elif "tencdn.classplusapp" in url:
                	headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA1NDYwMjk1LCJvcmdJZCI6MjIzLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwMDkxMDA1MTIiLCJuYW1lIjoiUGFua2FqIiwiZW1haWwiOm51bGwsImlzSW50ZXJuYXRpb25hbCI6MCwiZGVmYXVsdExhbmd1YWdlIjoiRU4iLCJjb3VudHJ5Q29kZSI6IklOIiwiY291bnRyeUlTTyI6IjkxIiwidGltZXpvbmUiOiJHTVQrNTozMCIsImlzRGl5IjpmYWxzZSwib3JnQ29kZSI6Im1hbHVrYSIsImlzRGl5U3ViYWRtaW4iOjAsImZpbmdlcnByaW50SWQiOiJiNDA0MDFlNDkyMWYzYjBmYWMzMzY5NDcwNTFlMiIsImlhdCI6MTcyMDU0MTgwNSwiZXhwIjoxNzIxMTQ2NjA1fQ.cH9hN0awcuRjvE4vKEgK4F3utMzoJqo8nWP1mVskvF00hQ0-BDdYq7xzqex-eomN', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                	params = (('url', f'{url}'),)
                	response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                	url = response.json()['url']
                elif "media-cdn-alisg.classplusapp.com" in url:
                	headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA1NDYwMjk1LCJvcmdJZCI6MjIzLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwMDkxMDA1MTIiLCJuYW1lIjoiUGFua2FqIiwiZW1haWwiOm51bGwsImlzSW50ZXJuYXRpb25hbCI6MCwiZGVmYXVsdExhbmd1YWdlIjoiRU4iLCJjb3VudHJ5Q29kZSI6IklOIiwiY291bnRyeUlTTyI6IjkxIiwidGltZXpvbmUiOiJHTVQrNTozMCIsImlzRGl5IjpmYWxzZSwib3JnQ29kZSI6Im1hbHVrYSIsImlzRGl5U3ViYWRtaW4iOjAsImZpbmdlcnByaW50SWQiOiJiNDA0MDFlNDkyMWYzYjBmYWMzMzY5NDcwNTFlMiIsImlhdCI6MTcyMDU0MTgwNSwiZXhwIjoxNzIxMTQ2NjA1fQ.cH9hN0awcuRjvE4vKEgK4F3utMzoJqo8nWP1mVskvF00hQ0-BDdYq7xzqex-eomN', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                	params = (('url', f'{url}'),)
                	response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                	url = response.json()['url']
                elif "videos.classplusapp" in url:
                	headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA1NDYwMjk1LCJvcmdJZCI6MjIzLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwMDkxMDA1MTIiLCJuYW1lIjoiUGFua2FqIiwiZW1haWwiOm51bGwsImlzSW50ZXJuYXRpb25hbCI6MCwiZGVmYXVsdExhbmd1YWdlIjoiRU4iLCJjb3VudHJ5Q29kZSI6IklOIiwiY291bnRyeUlTTyI6IjkxIiwidGltZXpvbmUiOiJHTVQrNTozMCIsImlzRGl5IjpmYWxzZSwib3JnQ29kZSI6Im1hbHVrYSIsImlzRGl5U3ViYWRtaW4iOjAsImZpbmdlcnByaW50SWQiOiJiNDA0MDFlNDkyMWYzYjBmYWMzMzY5NDcwNTFlMiIsImlhdCI6MTcyMDU0MTgwNSwiZXhwIjoxNzIxMTQ2NjA1fQ.cH9hN0awcuRjvE4vKEgK4F3utMzoJqo8nWP1mVskvF00hQ0-BDdYq7xzqex-eomN', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                	params = (('url', f'{url}'),)
                	response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                	url = response.json()['url']

                elif '/master.mpd' in url:
                    id =  url.split("/")[-2]
                    url =  "https://penpencilvod.pc.cdn.bitgravity.com/" + id + "/master.m3u8"
                

                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
              
               # if "https://d1d34p8vz63oiq.cloudfront.net/" in url:
                  #id =  url.split("/")[-2]
                  #url =  "https://psitoffers.store/testkey.php?vid=" + id + "&quality=" + raw_text2
                  #ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                #elif 'https://d1d34p8vz63oiq.cloudfront.net/' in url:
                  #id =  url.split("/")[-2]
                  #url =  "https://psitoffers.store/testkey.php?vid=" + id + "&quality=" + raw_text2
                 # ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                  
                  

                if "youtu" in url:
                    ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                else:
                    ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                else:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

                try:                               
                    cc = f'**{str(count).zfill(3)}.**{name1} **({res})**\n\n**Batch:- {b_name}**\n**{CR}**'
                    cc1 = f'**{str(count).zfill(3)}.**{name1}.pdf\n\n**Batch Name :- {b_name}**\n**{CR}**'
                    if "drive" in url:
                        try:
                            ka = await helper.download(url, name)
                            copy = await bot.send_document(chat_id=int(chat_id),document=ka, caption=cc1)
                            count+=1
                            os.remove(ka)
                            time.sleep(-5)
                        except FloodWait as e:
                            await bot.send_message(chat_id=int(chat_id), text=str(e))
                            time.sleep(e.x)
                            continue
                    elif ".pdf" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=int(chat_id), document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await bot.send_message(chat_id=int(chat_id), text=str(e))
                            time.sleep(e.x)
                            continue
                    else:
                        prog = await bot.send_message(chat_id=int(chat_id), text=f"**Downloading....**\n\n** {name}")
                        res_file = await helper.download_video(url, cmd, name)
                        filename = res_file
                        await prog.delete(True)
                        await helper.send_vid(bot, m, cc, filename, thumb, name, chat_id)
                        count += 1

                except Exception as e:
                    await m.reply_text(f"{name}:{url}")
                    count += 1
                    continue

        except Exception as e:
            await m.reply_text(e)
        await m.reply_text("Done ")
        await bot.send_message(chat_id=int(chat_id),text=f"Done")
        batch.clear()

bot.run()
