import os
import re
import sys
import time
import requests
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from aiohttp import ClientSession

import core as helper
from utils import progress_bar
from vars import api_id, api_hash, bot_token

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Function to fetch normal URLs asynchronously
async def fetch_normal_urls(url):
    response = await bot.loop.run_in_executor(None, lambda: requests.get(f"https://noxapi-0a195c5b9f8f.herokuapp.com/fetch_urls/{url}"))
    return response.json()

# Function to fetch DRM URLs asynchronously
async def fetch_drm_urls(url):
    response = await bot.loop.run_in_executor(None, lambda: requests.get(f"https://noxapi-0a195c5b9f8f.herokuapp.com/drm_urls/{url}"))
    return response.json()

@bot.on_message(filters.command("start"))
async def start_handler(bot: Client, m: Message):
    await m.reply_text("Hi!\n\nSend /Leo command to download from a text file.")

@bot.on_message(filters.command("Restart"))
async def restart_handler(_, m: Message):
    await m.reply_text("**Restarted**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("Leo"))
async def leo_handler(bot: Client, m: Message):
    editable = await m.reply_text('Hi\n\nTo download a text file, send it here »')
    input_message = await bot.listen(editable.chat.id)
    downloaded_file = await input_message.download()
    await input_message.delete(True)

    # Process the downloaded file
    try:
        with open(downloaded_file, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split("://", 1)[1] for i in content]  # Extract only the URL part
        os.remove(downloaded_file)
    except Exception as e:
        await m.reply_text(f"Invalid File Input. Error: {str(e)}")
        os.remove(downloaded_file)
        return

    await editable.edit(f"Total links found: {len(links)}\n\nSend from where you want to start downloading (1-{len(links)})")
    input_start = await bot.listen(editable.chat.id)
    start_index = int(input_start.text)
    await input_start.delete(True)

    try:
        for url in links[start_index - 1:]:
            try:
                # Fetch DRM URLs if it's a CPVOD link
                if "cpvod" in url:
                    drm_data = await fetch_drm_urls(url)
                    await m.reply_text(f"DRM Data for {url}: {drm_data}")

                # Fetch normal URLs otherwise
                else:
                    normal_data = await fetch_normal_urls(url)
                    await m.reply_text(f"Normal Data for {url}: {normal_data}")
                
                # Add your downloading logic here based on `drm_data` or `normal_data`

            except Exception as e:
                await m.reply_text(f"Failed to fetch data for {url}: {str(e)}")
                continue

    except Exception as e:
        await m.reply_text(f"Error during processing: {str(e)}")

    await m.reply_text("Download complete.")

bot.run()
