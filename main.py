import threading
import time
import sys
import discord
import requests
from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks
from decouple import config
import random
import asyncio

from responses import (
    handle_numbers,
    handle_response,
    handle_roll,
    handle_submit,
    handle_getLinks,
    handle_getAllLinks,
    handle_deleteLink,
)


TOKEN = config("TOKEN")


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()


intents = discord.Intents.all()
bot = Bot(intents=intents)


async def send_links():
    channel = await bot.fetch_channel(1179121530769248297)
    await channel.send(handle_getAllLinks())


# timer = 4
tiempo = random.randint(4, 6)  # tiene como 2 minutos de desfase
test_timer = random.randint(15, 25)


def setNewHeader():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    ]

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en;q=0.9",
        "dnt": "1",
        "referer": "https://www.ebay.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-full-version": '"102.0.5005.63"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(user_agents),
    }

    return headers


async def views_test(views: int):
    global test_timer
    channel = await bot.fetch_channel(1179121530769248297)
    try:
        links = handle_getAllLinks()
        for y in links:
            for i in range(views):
                headers = setNewHeader()
                print(f"agregando vista {i+1}... al link {y} ")
                r = requests.get(y, headers=headers)
                print(r.status_code)
            await asyncio.sleep(test_timer)
            print(f"agregado {views} en tantos {test_timer} segundos")
            await channel.send(
                f"agregando {views} vistas en {test_timer} segundos al link {y}"
            )
            test_timer = random.randint(25, 35)
            print(f"nuevo contador: {test_timer}")
            await channel.send(f"nuevo contador: {test_timer}")

    except Exception as e:
        print(f"Un error ha ocurrido en: {str(e)}")


async def message_test():
    channel = await bot.fetch_channel(1179121530769248297)
    await channel.send(f"han pasado {tiempo} minutos")


@tasks.loop(minutes=tiempo)
async def testMessage():
    global tiempo
    await views_test(45)
    await message_test()
    tiempo = random.randint(1445, 1560)
    testMessage.change_interval(minutes=tiempo)


@testMessage.before_loop
async def before_test():
    await bot.wait_until_ready()


@bot.hybrid_command(
    name="add_link", description="agrega un link de un producto a la base de datos"
)
@app_commands.describe(arg="link to add")
@app_commands.rename(arg="link")
async def add_link(interaction: discord.Interaction, arg: str):
    author = interaction.author.mention
    await interaction.reply(content=handle_submit(arg, author))


@bot.hybrid_command(name="view_links", description="muestra todos tus links")
async def response(interaction: discord.Interaction):
    await interaction.reply(content=handle_getLinks())


@bot.hybrid_command(
    name="stop_task", description="para la funcion de agregar vistas automaticamente"
)
async def response(interaction: discord.Interaction):
    author = interaction.author.mention
    testMessage.cancel()
    testMessage.stop()
    await interaction.reply(
        content=f"se ha parado la tarea de agregar vistas por {author}"
    )


@bot.hybrid_command(
    name="start_task", description="inicia la funcion de agregar vistas automaticamente"
)
async def response(interaction: discord.Interaction):
    author = interaction.author.mention
    testMessage.start()
    await interaction.reply(
        content=f"se ha iniciado la tarea de agregar vistas por {author}"
    )


@bot.hybrid_command(
    name="add_views", description="pone x vistas a un producto dado un link"
)
@app_commands.describe(
    arg="link of the product to add view to", arg2="number of views to add"
)
@app_commands.rename(arg="link", arg2="number")
async def response(interaction: discord.Interaction, arg: str, arg2: int):
    try:
        author = interaction.author.mention
        embed = discord.Embed(
            title="Vies",
            description=f"Adding {arg2} views...",
        )
        embed.add_field(name="Link", value=arg, inline=True)
        await interaction.reply(
            content=f"{author} has added {arg2} views to {arg}", embed=embed
        )
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9",
            "dnt": "1",
            "referer": "https://www.ebay.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            "sec-ch-ua-full-version": '"102.0.5005.63"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }

        for i in range(arg2):
            r = requests.get(arg, headers=headers)
            print(r.status_code)
            print(f"adding view {i+1}...")

        embed = discord.Embed(
            title="Views",
            description=f"Added {arg2} views!",
        )
        embed.add_field(name="Link", value=arg, inline=True)
        await interaction.reply(content=f"Added {arg2} views!", embed=embed)
    except Exception as e:
        await interaction.reply(content=f"An error occurred: {str(e)}")


@bot.hybrid_command(
    name="add_views_to_all",
    description="agrega x vistas a todos los productos de forma manual",
)
@app_commands.describe(arg="add x views to all the links")
@app_commands.rename(arg="number")
async def response(interaction: discord.Interaction, arg: int):
    try:
        links = handle_getAllLinks()
        embed = discord.Embed(
            title="Views",
            description=f"Adding {arg} views to all links...",
        )

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9",
            "dnt": "1",
            "referer": "https://www.ebay.co.uk/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            "sec-ch-ua-full-version": '"102.0.5005.63"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }

        await interaction.reply(
            content=f"Starting to add {arg} views to the links", embed=embed
        )
        for y in links:
            for i in range(arg):
                print(f"adding view {i+1}... to {y} ")
                r = requests.get(y, headers=headers)
                print(r.status_code)
            await asyncio.sleep(10)
            embed = discord.Embed(
                title="Views",
                description=f"Added {arg} views to {y}!",
            )
            embed.add_field(name="Link", value=arg, inline=True)

    except Exception as e:
        await interaction.reply(content=f"An error occurred: {str(e)}")


@bot.hybrid_command(name="delete_link", description="borra un link de la base de datos")
@app_commands.describe(arg="link to delete")
@app_commands.rename(arg="link")
async def response(interaction: discord.Interaction, arg: str):
    await interaction.reply(content=handle_deleteLink(arg))


bot.run(TOKEN)
