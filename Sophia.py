import discord
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl as yt
import os
import asyncio

bot = commands.Bot(command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    print("เรียกฉันหรอคะ? นายท่าน")

@bot.command()
async def sleep(ctx):
    print('good night')
    await ctx.channel.send('ฝันดีค่ะ นายท่าน')
    await bot.logout()

@bot.event
async def on_message(ctx):
    if ctx.content == "สวัสดี":
        await ctx.channel.send('อรุณสวัสดิ์ค่ะ นายท่านนนน')
    await bot.process_commands(ctx)


@bot.command()
async def play(ctx, url:str):
    Channel = get(ctx.guild.voice_channels, name='General')
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice is None:
        if not voice.is_connected():
            voice = await Channel.connect()
    else:
        voice = await Channel.connect()

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        ydl_opts = {'format': 'bestaudio', 'verbose': True}

    if not voice is None:
        if not voice.is_playing():
            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                print(info)
            URL = info['formats'][0]['url']
            voice.play(discord.FFmpegPCMAudio(URL))

@bot.command()
async def replay(ctx, url:str):
    Channel = get(ctx.guild.voice_channels, name='General')
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice == None
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ydl_opts = {'format': 'bestaudio', 'verbose': True}

    if not voice is None:
        if not voice.is_playing():
            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice.play(discord.FFmpegPCMAudio(URL))

@bot.command()
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice is None:
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("นายท่าน โปรดนำฉันเข้าช่องพูดคุยก่อนค่ะ")
    else:
        await ctx.send("นายท่าน โปรดนำฉันเข้าช่องพูดคุยก่อนค่ะ")

@bot.command()
async def help(ctx):
    Text = discord.Embed(title="ช่วยเหลือ!!!", description="ความสามารถของน้อง+ฟังค์ชั่นต่างๆ")
    Text.add_field(name='!help', value='ช่วยเหลือ', inline=False)
    Text.add_field(name='!play', value='ให้น้องเข้าช่องแชท(!play ลิ้งค์เพลง)', inline=False)
    Text.add_field(name='!replay', value='ให้น้องเล่นเพลงต่อโดยจะใช้คำสั่งนี้ได้ก็ต่อเมื่อน้องอยู่ในช่องแชทเท่านั้น(!replay ลิ้งค์เพลง)', inline=False)
    Text.add_field(name='!pause', value='ให้น้องหยุดเพลงที่กำลังเล่นอยู่', inline=False)
    Text.add_field(name='!resume', value='ให้น้องเล่นเพลงที่หยุด', inline=False)
    Text.add_field(name='!leave', value='ให้น้องออกจากห้อง>_<', inline=False)
    Text.set_thumbnail(url='https://cdn.donmai.us/sample/8f/1b/__hoshimachi_suisei_hololive_drawn_by_envyvanity__sample-8f1b0027e6b89b7b287d64bf60215866.jpg')
    await ctx.channel.send(embed=Text)

@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        ctx.send("นายท่าน โปรดนำฉันเข้าช่องพูดคุยก่อนค่ะ")
        return

    voice.pause()
    
@bot.command()
async def showlog(ctx, info):
    await ctx.channel.send(info)

@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        ctx.send("นายท่าน โปรดนำฉันเข้าช่องพูดคุยก่อนค่ะ")
        return

    voice.resume()

bot.run('Token')
