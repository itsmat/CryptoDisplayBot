import discord
import requests
from decimal import Decimal
from discord.ext import commands, tasks

CryptoDisplay = discord.Client(intents=discord.Intents.all())
REFRESH = 180 #REFRESH TIME 
TOKEN = "123abc" #BOT TOKEN


# [COLORI]
from colorama import Fore
c = Fore.LIGHTCYAN_EX
g = Fore.LIGHTGREEN_EX
r = Fore.LIGHTRED_EX
y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX
m = Fore.LIGHTMAGENTA_EX

async def prezzo(crypto):
    richiesta = requests.get(f'https://api.coingecko.com/api/v3/coins/{crypto}').json()
    prezzo_attuale = round(Decimal(richiesta["market_data"]["current_price"][f'{"eur".lower()}']), 2)
    ultime_24h = float(richiesta["market_data"]['price_change_percentage_24h'])
    if ultime_24h >= 0:
        bollino = "🟢 ↗"
    else:
        bollino = "🔴 ↘"
    nomecrypto = richiesta["symbol"]
    nomestanza = f"{bollino} {nomecrypto.upper()}: {prezzo_attuale}€"
    return nomestanza

@CryptoDisplay.event
async def on_ready():
    print(f'{g}{CryptoDisplay.user} connesso! - https://github.com/itsmat{w}')
    await CryptoDisplay.change_presence(activity=discord.Game(name=f"Crypto Display Bot - github.com/itsmat"))
    if REFRESH < 180:
        print(f"{r}[Attenzione] Refresh time troppo basso, usare un refresh time inferiore a 180 secondi potrebbe far ratelimitare il bot.{w}")
    aggiornaprezzi.start()

@CryptoDisplay.event
async def on_guild_join(server):
    print(f"{g}[{server.name}] Bot aggiunto.{w}")
    embed=discord.Embed(title="Grazie per avermi aggiunto in questo server!", description=f"Source code: https://github.com/itsmat/CryptoDisplayBot", color=0x4bee13)
    await server.text_channels[0].send(embed=embed)
    try:
        perms = {
                server.default_role: discord.PermissionOverwrite(view_channel = True, connect=False),
            }
        await server.create_voice_channel(name=await prezzo("bitcoin"), overwrites=perms)
        await server.create_voice_channel(name=await prezzo("litecoin"), overwrites=perms)
        await server.create_voice_channel(name=await prezzo("ethereum"), overwrites=perms)
        print(f"{g}[{server.name}] Canali creati.{w}")
    except Exception as errore:
        print(f"{r}[{server.name}] Errore nella creazione dei canali, {errore}.{w}")


@tasks.loop(seconds=REFRESH)
async def aggiornaprezzi():
    for server in CryptoDisplay.guilds:
        print(f"{m}[{server.name}] Aggiornamento...{w}")
        for channel in server.channels:
            if "BTC:" in channel.name:
                nome = await prezzo("bitcoin")
                print(F"{c}[{server.name}] Update BTC: {channel.id}{w}")
                await channel.edit(name=nome)
            if "LTC:" in channel.name:
                nome = await prezzo("litecoin")
                print(F"{c}[{server.name}] Update LTC: {channel.id}{w}")
                await channel.edit(name=nome)
            if "ETH:" in channel.name:
                nome = await prezzo("ethereum")
                print(F"{c}[{server.name}] Update ETH: {channel.id}{w}")
                await channel.edit(name=nome)

CryptoDisplay.run(TOKEN)
