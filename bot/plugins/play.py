'''
VoiceChatStreamer, An Telegram Bot Project
Copyright (c) 2021 Anjana Madu <https://github.com/AnjanaMadu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

import os, asyncio, pafy
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from bot import video_link_getter, yt_video_search, match_url
from bot import vcusr

STREAM = {8}
GROUP_CALLS = {}
    
@vcusr.on_message(filters.command("help", "?"))
async def help_vc(client, message):
    text = '''====== Help Menu ======
**Play as Audio**
- ?play __(reply to audio / youtube url / search query)__
- ?radio __(radio stream url)__

**Play as Video**
- ?stream __(reply to video / youtube url / search query)__
- ?live __(youtube live stream url)__

**Extra**
- ?endvc: Leave from vc
- ?video: Download url or search query in video format
- ?audio: Download url or search query in audio format'''
    await message.reply(text)

@vcusr.on_message(filters.command("endvc", "?"))
async def leave_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    group_call = GROUP_CALLS.get(CHAT_ID)
    if group_call:
        await group_call.stop()
        await message.reply("__UDAH DI END ASU__")

@vcusr.on_message(filters.command("live", "?"))
async def live_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("⏳ __Sabar ya NGENTOD__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __KASI URL YANG BENER BANGSAT!__")
    if match_url(INPUT_SOURCE, key="yt") is None:
        return await msg.edit("🔎 __Gak nemu Live nya__")
    #ytlink = await run_cmd(f"youtube-dl -g {INPUT_SOURCE}")
    videof = pafy.new(INPUT_SOURCE)
    ytlink = videof.getbest().url
    if match_url(ytlink) is None:
        return await msg.edit(f"`{ytlink}`")
    try:
        group_call = GROUP_CALLS.get(CHAT_ID)
        if group_call is None:
            group_call = GroupCallFactory(vcusr, outgoing_audio_bitrate_kbit=512).get_group_call()
            GROUP_CALLS[CHAT_ID] = group_call
        if group_call.is_connected:
            await group_call.stop()
            await asyncio.sleep(3)
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Live nya udah mulai__")
        await group_call.start_video(ytlink, repeat=False, enable_experimental_lip_sync=True)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@vcusr.on_message(filters.command("radio", "?"))
async def radio_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __All radio stations listed [here](https://github.com/AnjanaMadu/radio_stations). Please get link from [here](https://github.com/AnjanaMadu/radio_stations)__", disable_web_page_preview=True)
    if match_url(INPUT_SOURCE) is None:
        return await msg.edit("🔎 __Give me a valid URL__")
    try:
        group_call = GROUP_CALLS.get(CHAT_ID)
        if group_call is None:
            group_call = GroupCallFactory(vcusr, outgoing_audio_bitrate_kbit=512).get_group_call()
            GROUP_CALLS[CHAT_ID] = group_call
        if group_call.is_connected:
            await group_call.stop()
            await asyncio.sleep(3)
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Radio Playing...__")
        await group_call.start_audio(INPUT_SOURCE, repeat=False)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
    
@vcusr.on_message(filters.command("play", "?"))
async def play_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Lagi di download__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 **KALAU NGASI URL ITU YANG BENER VIDIONYA GA NEMU!**")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("**VIDIO NYA GAK KETEMU**🤷‍♂️")
        await msg.edit("📥 __Lagi di download__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="a")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        group_call = GROUP_CALLS.get(CHAT_ID)
        if group_call is None:
            group_call = GroupCallFactory(vcusr, outgoing_audio_bitrate_kbit=512).get_group_call()
            GROUP_CALLS[CHAT_ID] = group_call
        if group_call.is_connected:
            await group_call.stop()
            await asyncio.sleep(3)
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __UDAH MULAI!__")
        await group_call.start_audio(LOCAL_FILE, repeat=False)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@vcusr.on_message(filters.command("stream", "?"))
async def stream_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("⏳ __SABAR NGENTOD__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Download dulu__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 **KALAU KASI URL YANG BENER DIKIT NGENTOD**")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("**GAADA VIDIONYA** 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="v")
        if LOCAL_FILE == 500: return await msg.edit("EROR BANGSAT 🤷‍♂️")
         
    try:
        group_call = GROUP_CALLS.get(CHAT_ID)
        if group_call is None:
            group_call = GroupCallFactory(vcusr, outgoing_audio_bitrate_kbit=512).get_group_call()
            GROUP_CALLS[CHAT_ID] = group_call
        if group_call.is_connected:
            await group_call.stop()
            await asyncio.sleep(3)
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 **UDAH MULAI YA ANJG!**")
        await group_call.start_video(LOCAL_FILE, repeat=False, enable_experimental_lip_sync=True)
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
