import discord
import feedparser
import asyncio
from discord.ext import tasks

# Discord bot token
TOKEN = 'acf8b69fc37efbb5b08f0a21f26723d16b75fec3d125788641bd61ce68280251'

# RSS feed URL-k
rss_feeds = {
    "index-hu": "https://index.hu/24ora/rss/",
    "444-hu": "https://444.hu/feed",
    "esport1-hu": "https://esport1.hu/rss",
    "portfolio-hu": "https://www.portfolio.hu/rss/all.xml",
    "telex-hu": "https://telex.hu/rss",
    "bitcoin-hu": "https://bitcoin.hu/feed/",
    "24-hu": "https://24.hu/feed/",
    "kriptomagazin-hu": "https://kriptomagazin.hu/feed/",
     "ign-hu": "https://hu.ign.com/rss",
}

# Szobák (channel id-k, amiket be kell állítani)
channels = {
    "index-hu": 1318217477590880348, 
    "444-hu": 1318149148809367582, 
    "esport1-hu": 1318217532057849907,
    "portfolio-hu": 1318217580476891176,
    "telex-hu": 1318217628245954670, 
    "bitcoin-hu": 1318217674802728960,
    "24-hu": 1318217703319670904,
    "kriptomagazin-hu": 1318217746995216527,
    "ign-hu":  1318217778548838502
}

# Egyedi név, avatar, és embed beállítások minden RSS feedhez
feed_settings = {
    "index-hu": {
        "name": "Index.hu Hírek",
        "avatar": "https://index.hu/img/logo.png", 
        "embed_color": discord.Color.blue(),  
        "footer": "Index.hu - Friss hírek" 
    },
    "444-hu": {
        "name": "444.hu Hírek",
        "avatar": "https://444.hu/img/logo.png",  
        "embed_color": discord.Color.green(), 
        "footer": "444.hu - Friss hírek" 
    },
    "esport1-hu": {
        "name": "Esport1 Hírek",
        "avatar": "https://esport1.hu/img/logo.png", 
        "embed_color": discord.Color.purple(),
        "footer": "Esport1.hu - Esport hírek" 
    },
    "portfolio-hu": {
        "name": "Portfolio.hu Hírek",
        "avatar": "https://www.portfolio.hu/img/logo.png", 
        "embed_color": discord.Color.dark_gold(),  
        "footer": "Portfolio.hu - Gazdasági hírek"
    },
    "telex-hu": {
        "name": "Telex.hu Hírek",
        "avatar": "https://telex.hu/img/logo.png",  
        "embed_color": discord.Color.orange(), 
        "footer": "Telex.hu - Friss hírek"  
    },
    "bitcoin-hu": {
        "name": "Bitcoin.hu Hírek",
        "avatar": "https://bitcoin.hu/img/logo.png",  
        "embed_color": discord.Color.gold(), 
        "footer": "Bitcoin.hu - Kriptovaluta hírek" 
    },
    "24-hu": {
        "name": "24.hu Hírek",
        "avatar": "https://24.hu/img/logo.png",
        "embed_color": discord.Color.red(), 
        "footer": "24.hu - Friss hírek" 
    },
    "kriptomagazin-hu": {
        "name": "Kriptomagazin.hu Hírek",
        "avatar": "https://kriptomagazin.hu/img/logo.png", 
        "embed_color": discord.Color.blue(), 
        "footer": "Kriptomagazin.hu - Kriptovaluta hírek"  
    },
    "ign-hu": {
        "name": "IGN.hu Hírek",
        "avatar": "https://hu.ign.com/img/logo.png", 
        "embed_color": discord.Color.red(), 
        "footer": "IGN.hu - Játékok és tech hírek"
    }
}


# Discord bot intents beállítása
intents = discord.Intents.default()
intents.messages = True  # Ha a botnak szüksége van üzenetek olvasására, engedélyezni kell

# Discord bot kliens
client = discord.Client(intents=intents)

# Funkció, amely lekéri az RSS feedeket és elküldi a híreket embed üzenetekben
async def fetch_rss():
    await client.wait_until_ready()
    
    # RSS feedek folyamatos ellenőrzése 5 percenként
    while not client.is_closed():
        for feed_name, feed_url in rss_feeds.items():
            feed = feedparser.parse(feed_url)
            channel = client.get_channel(channels[feed_name])
            
            # Legutolsó hír
            latest_entry = feed.entries[0]
            title = latest_entry.title
            link = latest_entry.link
            published = latest_entry.published  # RSS hír publikálásának ideje
            
            # Egyedi beállítások az embedhez
            bot_name = feed_settings[feed_name]["name"]
            bot_avatar_url = feed_settings[feed_name]["avatar"]
            embed_color = feed_settings[feed_name]["embed_color"]
            footer = feed_settings[feed_name]["footer"]
            
            # Embed üzenet készítése
            embed = discord.Embed(
                title=title,
                description=f"[Olvasd el a teljes hírt itt]({link})",
                color=embed_color,  # Szín
                timestamp=published  # Publikálás ideje
            )
            embed.set_footer(text=footer)  # Aláírás
            embed.set_author(name=bot_name, icon_url=bot_avatar_url)  # Bot név és avatar

            # Ha a cikk tartalmaz képet, állítsuk be azt
            if 'media:content' in latest_entry:
                embed.set_image(url=latest_entry['media:content'][0]['url'])

            # Küldjük el az embed üzenetet a megfelelő szobába
            await channel.send(embed=embed)
        
        # 5 perc várakozás
        await asyncio.sleep(300)  # 300 másodperc = 5 perc

# Bot indítása
@client.event
async def on_ready():
    print(f'Bot elindult: {client.user.name}')
    # RSS frissítés indítása
    client.loop.create_task(fetch_rss())

# Bot indítása
client.run(TOKEN)
