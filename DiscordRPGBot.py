#!/usr/bin/env python
# coding: utf-8
import discord
import pymysql
import threading
import asyncio
import time
import random
import os
import random
import urllib.request
import json
import sys
import ftplib
import subprocess
import base64
import glob
import json
import linecache
from urllib.request import urlopen
from datetime import datetime


def getConfig():
    try:
        with open("config.json") as json_file:
            data = json.load(json_file)
            return data
    except:
        return None

    return None


config = getConfig()
if config == None:
    print("Error loading the configuration file.")

rp_channel = config["rp_channel"]
botGuild = config["bot_guild"]
ownersId = config["owners"]
blackGuilds = config["black_guilds"]
ownerNameRole = config["owner_role"]
blockedCommands = config["blocked_commands"]
closedForUsers = config["closed"]

roles = {
    99: {"name": "Luisa RPG Player", "color": "808000", "price": 0},
    100: {"name": "[R] Polícia", "color": "1C1C1C", "price": 38000},
    101: {"name": "[R] Hacker", "color": "F0FFFF", "price": 20000},
    102: {"name": "[R] Bombeiro", "color": "A52A2A", "price": 27000},
    103: {"name": "[R] Advogado", "color": "48D1CC", "price": 10000},
    104: {"name": "[R] Médico", "color": "A9A9A9", "price": 25000}
}

itemsList = {
    1: {"name": "AK-47", "price": "45000", "food": False, "gun": True, "whitegun": False, "damage": 10, "bullets": False, "westcoast": False},
    2: {"name": "M5", "price": "18000", "food": False, "gun": True, "whitegun": False, "damage": 7, "bullets": False, "westcoast": False},
    3: {"name": "Glock", "price": "7000", "food": False, "gun": True, "whitegun": False, "damage": 3, "bullets": False, "westcoast": False},
    4: {"name": "DesertEagle", "price": "14000", "food": False, "whitegun": False, "gun": True, "damage": 4, "bullets": False, "westcoast": False},
    5: {"name": "M3", "price": "15000", "food": False, "gun": True, "whitegun": False, "damage": 5, "bullets": False, "westcoast": False},
    6: {"name": "UMP", "price": "19000", "food": False, "gun": True, "whitegun": False, "damage": 6, "bullets": False, "westcoast": False},
    7: {"name": "MP9", "price": "22000", "food": False, "gun": True, "whitegun": False, "damage": 7, "bullets": False, "westcoast": False},
    8: {"name": "Taurus", "price": "4000", "food": False, "gun": True, "whitegun": False, "damage": 4, "bullets": False, "westcoast": False},
    9: {"name": "Faca", "price": "1000", "food": False, "gun": False, "whitegun": True, "damage": 2, "bullets": False, "westcoast": False},
    10: {"name": "Espada", "price": "2000", "food": False, "gun": False, "whitegun": True, "damage": 3, "bullets": False, "westcoast": False},
    11: {"name": "Celular", "price": "10000", "food": False, "gun": False, "whitegun": False, "bullets": False, "westcoast": False},
    12: {"name": "Colete", "price": "10000", "food": False, "gun": False, "whitegun": False, "bullets": False, "westcoast": True},
    13: {"name": "10 balas", "price": "500", "food": False, "amount": 10, "whitegun": False, "gun": False, "bullets": True, "westcoast": False},
    14: {"name": "50 balas", "price": "2100", "food": False, "amount": 50, "whitegun": False, "gun": False, "bullets": True, "westcoast": False},
    15: {"name": "100 balas", "price": "4100", "food": False, "amount": 100, "whitegun": False, "gun": False, "bullets": True, "westcoast": False},
    16: {"name": "200 balas", "price": "8100", "food": False, "amount": 200, "whitegun": False, "gun": False, "bullets": True, "westcoast": False},
    17: {"name": "Sanduíche", "price": "95", "food": True, "eating": 20, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    18: {"name": "Salgado", "price": "50", "food": True, "eating": 10, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    19: {"name": "Coxinha", "price": "40", "food": True, "eating": 5, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    20: {"name": "Espetinho", "price": "15", "food": True, "eating": 4, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    21: {"name": "Sorvete", "price": "20", "food": True, "eating": 5, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    22: {"name": "Presunto", "price": "35", "food": True, "eating": 15, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    23: {"name": "Cachorro Quente", "price": "105", "food": True, "eating": 25, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    24: {"name": "Hambúrguer", "price": "110", "food": True, "eating": 30, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    25: {"name": "Água", "price": "12", "food": True, "eating": 2, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    26: {"name": "Suco", "price": "15", "food": True, "eating": 4, "whitegun": False, "gun": False, "bullets": False, "westcoast": False},
    27: {"name": "Pizza", "price": "20", "food": True, "eating": 5, "whitegun": False, "gun": False, "bullets": False, "westcoast": False}
}


class Bot(discord.Client):
    prefix = "!"
    debug = True
    database = None
    cycleTask = []
    countCycle = 0
    lastNote = {}
    colours = [discord.Colour(0xe91e63), discord.Colour(
        0x0000FF0), discord.Colour(0x00FF00), discord.Colour(0xFF0000)]

    async def info(self, message):
        print("[%s][INFO][RPG BOT] %s" %
              (datetime.now().strftime("%H:%M:%S"), message))

        guild = client.get_guild(botGuild)
        if guild != None:
            channel = await self.getChannel("luisa-logs", guild)
            if channel != None:
                await channel.send("**[%s][INFO][RPG BOT]** %s" % (datetime.now().strftime("%H:%M:%S"), message))

    async def debug(self, message):
        print("[%s][DEBUG][RPG BOT] %s" %
              (datetime.now().strftime("%H:%M:%S"), message))

        guild = client.get_guild(botGuild)
        if guild != None:
            channel = await self.getChannel("luisa-logs", guild)
            if channel != None:
                await channel.send("**[%s][DEBUG][RPG BOT]** %s" % (datetime.now().strftime("%H:%M:%S"), message))

    async def error(self, message):
        print("[%s][ERROR][RPG BOT] %s" %
              (datetime.now().strftime("%H:%M:%S"), message))

        guild = client.get_guild(botGuild)
        if guild != None:
            channel = await self.getChannel("luisa-logs", guild)
            if channel != None:
                await channel.send("**[%s][ERROR][RPG BOT]** %s" % (datetime.now().strftime("%H:%M:%S"), message))

        if "Already closed" in str(message):
            await self.destroy()
            if self.debug:
                await self.debug("Restarting the BOT...")
            subprocess.Popen('py -3 DiscordRPGBot.py')
            os._exit(0)

    async def destroy(self):
        self.database = None
        self.countCycle = 0
        self.cycleTask = []
        self.lastNote = {}
        for x in client.voice_clients:
            if x.is_connected():
                await x.disconnect()

    async def getChannel(self, channel, guild):
        return discord.utils.find(lambda item: channel in item.name, guild.channels)

    async def getMemberUsername(self, user):
        try:
            if user.nick != None:
                return user.nick
        except:
            return user.name

        return user.name

    async def getUser(self, userId, guildId):
        cursor = await self.getCursor()
        if cursor != None:
            cursor.execute(
                "select * from users where guild_id = '%s' and user_id = '%s'" % (guildId, userId))
            userInfo = cursor.fetchone()

            try:
                guild = client.get_guild(guildId)
                if guild != None:
                    member = discord.utils.get(guild.members, id=int(userId))
                    if member is not None and discord.utils.get(member.roles, name=roles[99]["name"]) is None:
                        role = discord.utils.get(
                            guild.roles, name=roles[99]["name"])
                        if role is not None:
                            await member.add_roles(role)
            except:
                pass

            if userInfo != None:
                return userInfo
            else:
                cursor.execute(
                    "insert into users (user_id,guild_id) values (%s,%s)" % (userId, guildId))
                self.database.commit()
                return await self.getUser(userId, guildId)

        return None

    async def updateUser(self, table, userId, amount, guildId):
        cursor = await self.getCursor()
        if cursor != None:
            cursor.execute("update users set %s = '%s' where user_id = '%s' and guild_id = '%s'" % (
                table, amount, userId, guildId))
            self.database.commit()

    async def updateLevel(self, user, progress, channel, guildId):
        if user != None:
            level = user["level"]
            progress = user["progress_level"] + progress
            if progress >= 100:
                await self.updateUser("level", user["user_id"], level + 1, guildId)
                await self.updateUser("progress_level", user["user_id"], 0, guildId)
                member = discord.utils.get(
                    client.get_all_members(), id=int(user["user_id"]))
                if member is not None:
                    await channel.send(":star: | Parabéns **%s**, você avançou para o nível **%s**!" % (member.mention, level + 1))

            else:
                await self.updateUser("progress_level", user["user_id"], progress, guildId)

    async def haveItem(self, itemID, rpgUser):
        if rpgUser["items"] == "" or rpgUser["items"] == None:
            return False

        return discord.utils.find(lambda item: item == itemID, eval(rpgUser["items"]))

    async def connectDatabase(self):
        try:
            self.database = pymysql.connect(config["mysql_host"], config["mysql_user"], config["mysql_pass"], config["mysql_database"],
                                            port=3306, cursorclass=pymysql.cursors.DictCursor, charset='utf8')
            self.database.ping()
        except Exception as e:
            await self.error(e)

    async def getCursor(self):
        try:
            if self.database is not None:
                self.database.commit()
                return self.database.cursor()
        except:
            await self.connectDatabase()
            return self.database.cursor()

    async def hungerCycle(self, guild):
        while not client.is_closed():
            await asyncio.sleep(100)
            hourNow = datetime.now().hour

            cursor = await self.getCursor()
            if cursor != None and hourNow <= 23 and hourNow > 6:
                channel = await self.getChannel(rp_channel, guild)
                cursor.execute(
                    "select * from users where guild_id = '%s'" % guild.id)
                data = cursor.fetchall()
                for user in data:
                    member = discord.utils.get(
                        guild.members, id=int(user["user_id"]))
                    if member is not None and discord.utils.get(member.roles, name=roles[99]["name"]) is None:
                        role = discord.utils.get(
                            guild.roles, name=roles[99]["name"])
                        if role is not None:
                            await member.add_roles(role)

                    totalHunger = int(user["hunger"] - 2)
                    if totalHunger > 0:
                        if totalHunger != 0:
                            await self.updateUser("hunger", user["user_id"], totalHunger, guild.id)
                            member = discord.utils.get(
                                guild.members, id=int(user["user_id"]))
                            if totalHunger < 8 and channel != None and member != None and random.choice([0, 0, 0, 1]) == 1:
                                await channel.send(":cut_of_meat: | **%s**, você precisa se alimentar para não morrer, sua fome está muito **baixa**, alimente-se imediatamente." % member.mention)
                    else:
                        await self.updateUser("hunger", user["user_id"], 0, guild.id)
                        await self.updateUser("health", user["user_id"], 0, guild.id)
                        await self.updateUser("kills", user["user_id"], user["kills"] + 1, guild.id)
                        if user["hunger"] != 0:
                            await channel.send(":skull: | **%s**, você não se alimentou e **morreu**." % member.mention)

            await asyncio.sleep(11500)

    async def botCycle(self):
        while not client.is_closed():

            hourNow = datetime.now().hour
            with open("LelQVDu.png" if 18 < hourNow and hourNow > 7 else "0t9XS2J.jpg", "rb") as f:
                icon = f.read()
                await client.user.edit(avatar=icon)

            randomPresence = random.choice(["1", "2", "3", "4"])
            presence = ""
            if randomPresence == "1":
                presence = self.prefix + str('ajuda')
            elif randomPresence == "2":
                presence = "várias mortes."
            elif randomPresence == "3":
                presence = "tiroteio em Beverly Hills."
            elif randomPresence == "4":
                presence = "roubo no banco central."
            await client.change_presence(activity=discord.Streaming(name=presence, url="https://www.twitch.tv/raddiszao"))

            await asyncio.sleep(500)

    async def cycle(self, guild):
        while not client.is_closed():
            if discord.utils.get(guild.roles, name=ownerNameRole) is None:
                await guild.create_role(permissions=discord.Permissions(manage_channels=True, manage_messages=True, manage_nicknames=True, manage_roles=True), name=ownerNameRole, colour=discord.Colour(0x808080))

            ownerRole = discord.utils.get(guild.roles, name=ownerNameRole)
            if ownerRole != None:
                for ownerId in ownersId:
                    ownerMember = discord.utils.get(guild.members, id=ownerId)
                    if ownerMember is not None:
                        await ownerMember.add_roles(ownerRole)

            i = 0
            for role in roles:
                if discord.utils.get(guild.roles, name=roles[role]["name"]) is None:
                    hex_int = int("0x" + str(roles[role]["color"]), 16)
                    await guild.create_role(name=roles[role]["name"], colour=discord.Colour(hex_int))
                i += 1

            strongCarSort = random.choice([0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                                           0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            channel = await self.getChannel(rp_channel, guild)
            hourNow = datetime.now().hour

            cursor = await self.getCursor()
            if strongCarSort == 1 and hourNow < 23 and hourNow > 10:
                if channel != None and not closedForUsers:
                    sort = random.randint(1000, 3000)
                    embed = discord.Embed(title=":moneybag: | Um carro forte da polícia acabou de capotar!", description="Um carro forte acabou de capotar em sentido a Beverlly Hills com **%s** reais, **REAJA** para roubá-lo! Mas lembre-se, você será procurado pela polícia!" %
                                          sort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S"))
                    strongCarMessage = await channel.send(embed=embed)
                    await strongCarMessage.add_reaction("💰")

                    def check(reaction, user):
                        rpgUser = None
                        if cursor != None:
                            cursor.execute(
                                "select * from users where guild_id = '%s' and user_id = '%s'" % (guild.id, user.id))
                            rpgUser = cursor.fetchone()

                        return reaction.message.id == strongCarMessage.id and reaction.emoji == "💰" and rpgUser != None and rpgUser["stuck"] == "0" and client.user.id != user.id

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
                    except asyncio.TimeoutError:
                        await strongCarMessage.delete()
                    else:
                        await strongCarMessage.delete()
                        rpgUser = await self.getUser(user.id, guild.id)
                        if rpgUser != None:
                            await self.updateUser("xp_points", user.id, rpgUser["xp_points"] + sort, guild.id)
                            await self.updateUser("wanted", user.id, 1, guild.id)
                            await self.updateLevel(rpgUser, 4, channel, guild.id)
                            await channel.send(":moneybag: | **%s** roubou **%s** reais do carro forte e agora está sendo **procurado(a)** pela polícia!" % (user.mention, sort))

            countMsgBot = 0

            if channel != None:
                async for x in channel.history(limit=5):
                    if x.author.bot:
                        countMsgBot += 1

                notesSort = random.choice([1, 1, 0, 1, 0, 1, 1])
                if notesSort == 1 and countMsgBot < 4:
                    notes = ["É novo? Está com dúvidas? Digite **%sajuda**." % self.prefix, "Você pode iniciar trabalhando como **carteiro** ou **lixeiro**.", "**Cuidado!** Ao dar um soco ou atirar pela madrugada você tem muitas chances de ser preso!", "Adicione-me em seu servidor! Digite **%sbot** e clique no link!" % self.prefix, "Nunca deixe um valor alto de reais em sua carteira, pois você poderá ser roubado por outras pessoas.",
                             "Certifique-se de manter sempre comida em seu inventário, pois se você for preso não poderá comprar.", "Mantenha sempre dinheiro reserva em sua carteira, pois se for preso você não poderá sacar dinheiro do banco.", "Se você é um policial, tenha cuidado ao usar comandos fora da lei, você poderá perder seu cargo."]
                    await channel.send(":notepad_spiral: | %s" % random.choice(notes))

            if cursor != None:
                cursor.execute(
                    "select * from users where stuck_time > 0 and guild_id = '%s'" % guild.id)
                data = cursor.fetchall()
                for user in data:
                    stuckTime = int(user["stuck_time"])
                    stuckMember = discord.utils.get(
                        guild.members, id=int(user["user_id"]))
                    if time.time() > stuckTime and channel != None and stuckMember != None:
                        await channel.send(":man_raising_hand: | **%s**, seu tempo na cadeia acabou, **você está livre**!" % stuckMember.mention)
                        await self.updateUser("stuck", user["user_id"], 0, guild.id)
                        await self.updateUser("stuck_time", user["user_id"], 0, guild.id)
                        await self.updateUser("wanted", user["user_id"], 0, guild.id)

            await asyncio.sleep(240)

    async def on_voice_state_update(self, member, before, after):
        if member != client.user.name:
            if before.channel is None and after.channel is not None:
                pass

    async def on_member_update(self, before, after):
        pass

    async def on_member_join(self, member):
        pass

    async def on_guild_join(self, guild):
        if guild.id in blackGuilds:
            await guild.leave()
            return

        if self.debug:
            await self.debug("%s joined in the server: %s" % (client.user.name, guild.name))

        rpChannel = discord.utils.find(
            lambda x: x.name == rp_channel, guild.text_channels)
        if rpChannel == None:
            rpChannel = await guild.create_text_channel(name=rp_channel)

        self.cycleTask.append(client.loop.create_task(self.cycle(guild)))
        self.cycleTask.append(client.loop.create_task(self.hungerCycle(guild)))
        await rpChannel.send(embed=discord.Embed(title="Olá!", description="Olá, meu nome é **%s**, um BOT Roleplay desenvolvido por **Raddis**. Este é meu canal onde você poderá usar meus comandos, para ver meus comandos digite **%sajuda**.\n\nQualquer bug reporte ao proprietário do bot. (**raddis#4444**)" % (client.user.name, self.prefix), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Roleplay BOT desenvolvido por raddis#4444.").set_author(icon_url=client.user.avatar_url, name=client.user.name).set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/rpg-1691444-1441510.png"))

    async def on_guild_remove(self, guild):
        if self.debug:
            await self.debug("%s left the server: %s" % (client.user.name, guild.name))

    async def on_member_remove(self, member):
        pass

    async def on_message_edit(self, before, after):
        await self.parseCommands(after)

    async def on_message_delete(self, after):
        pass

    async def on_reaction_add(self, reaction, user):
        if user.id == client.user.id:
            return

    async def on_ready(self):
        await self.info("Bot successfully connected!")
        await self.info("ID: %s" % client.user.id)
        await self.info("Name: %s" % client.user.name)
        await self.info("Commands prefix: %s" % self.prefix)
        await self.connectDatabase()
        self.cycleTask.append(client.loop.create_task(self.botCycle()))
        guilds = ""
        for guild in client.guilds:
            if guild.id in blackGuilds:
                await guild.leave()
            self.lastNote[guild.id] = ""
            self.cycleTask.append(client.loop.create_task(self.cycle(guild)))
            self.cycleTask.append(
                client.loop.create_task(self.hungerCycle(guild)))
            guilds += "%s (%s)(%s), " % (guild.name,
                                         len(guild.members), guild.id)
        await self.info("Online in guilds: %s" % (guilds[:-2]))
        print("================================================================================")

    async def on_message(self, message):
        if (message.author.id == client.user.id or message.author.bot) or (message.content.startswith(self.prefix) and len(message.content) <= 2):
            return

        if self.debug:
            if message.content.startswith(self.prefix) and not message.guild == None:
                await self.debug("[%s] %s executed the command: %s" % (message.guild.name, message.author, message.content))

            if message.guild == None:
                await self.debug("%s sent a private message: %s" % (await self.getMemberUsername(message.author), message.content))

        await self.parseCommands(message)

    async def parseCommands(self, message):
        try:
            if message.content.startswith(self.prefix) or message.content.startswith(self.prefix.upper()) and message.guild != None:
                cursor = await self.getCursor()
                if cursor == None:
                    await message.channel.send(message.author.mention, embed=discord.Embed(title="Ops!", description="Parece que meu servidor está offline, volto já!", colour=0xFF0000))
                    return

                permissions = []
                for perm, allowed in message.author.permissions_in(message.channel):
                    if allowed:
                        permissions.append(perm)

                if message.guild != None and (not 'administrator' in permissions or not 'manage_channels' in permissions) and not rp_channel in message.channel.name.lower() and not message.author.id in ownersId:
                    # await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar comandos neste canal, use o canal de comandos de roleplay.", colour=0xFF0000))
                    return

                values = message.content.split(" ")
                command = values[0].lower().split(self.prefix)[1].strip()
                args = values[1:]
                argsCount = len(args)
                argsNotSplited = " ".join(args)

                if message.guild != None:
                    try:
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser != None:
                            role = discord.utils.get(
                                message.author.roles, name=roles[100]["name"])
                            if role is not None and rpgUser["wanted"] == "1":
                                await message.channel.send(message.author.mention, embed=discord.Embed(title=":detective: | A casa caiu!", description="Você foi pego desobedecendo as leis e por isso perdeu seu cargo de policial.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                await message.author.remove_roles(role)
                                return
                    except:
                        pass

                    canCommand = True
                    if message.guild.id in blockedCommands:
                        canCommand = discord.utils.find(
                            lambda b: b == command, blockedCommands)

                    if not canCommand:
                        await message.channel.send(":no_entry: | **%s**, comando indisponível neste servidor." % (message.author.mention))
                        return

                if closedForUsers and not message.author.id in ownersId:
                    await message.channel.send(":no_entry: | **%s**, no momento meu servidor está offline para atualizações, voltarei em breve." % (message.author.mention))
                    return

                if command in ['saldo', 'banco', 'carteira']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        embed = discord.Embed(title=":dollar: | Confira seu saldo %s:" % (await self.getMemberUsername(message.author)), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        embed.add_field(name="Carteira", value=str(
                            rpgUser["xp_points"]), inline=False)
                        embed.add_field(name="Banco", value=str(
                            rpgUser["xp_deposited"]), inline=False)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['botinfo', 'infobot', 'info', 'bot']:
                    async with message.channel.typing():
                        embed = discord.Embed(colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Roleplay BOT desenvolvido por raddis#4444.").set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)).set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/rpg-1691444-1441510.png")
                        embed.add_field(name="Desenvolvedor",
                                        value="Raddis", inline=False)
                        embed.add_field(name="Membros neste servidor", value=str(
                            len(message.guild.members)), inline=False)
                        embed.add_field(name="Servidores", value=str(
                            len(client.guilds)), inline=False)
                        embed.add_field(name="Adicione-me em seu servidor",
                                        value="[Clique aqui](https://discord.com/api/oauth2/authorize?client_id=%s&permissions=1547042544&scope=bot)" % (client.user.id), inline=False)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['comandos', 'ajuda', 'help']:
                    async with message.channel.typing():
                        title = "Olá %s, confira meus comandos abaixo:" % await self.getMemberUsername(message.author)
                        result = "- **" + \
                            str(self.prefix) + \
                            "saldo** - Mostra as informações do seu saldo.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "perfil** - Mostra o seu perfil.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "apostar __quantidade__** - Teste sua sorte e faça sua aposta.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "daily** - Colete seu prêmio diário.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "week** - Colete seu prêmio semanal.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "month** - Colete seu prêmio mensal.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "depositar __quantidade__** - Deposite o valor desejado no banco.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "sacar __quantidade__** - Saque a quantia desejada.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "transferir __@nome__ __quantidade__** - Transfira a quantia desejada para alguém.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "casar __@nome__** - Case com a sua alma gêmea.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "beijar __@nome__** - Beije sua alma gêmea.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "divorciar** - Cansou da relação? Divorcie-se.\n"
                        # result += "- **" + \
                        #   str(self.prefix) + "matar __@nome__** - Mate alguém.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "soco __@nome__** - Dê um soco em alguém.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "assaltar __@nome__** - Assalte alguém.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "prender __@nome__** - Prenda os ladrõezinhos a solta.\n"
                        result += "- **" + \
                            str(self.prefix) + "enviarmensagem __@nome__ __mensagem__** - Envie uma mensagem com seu celular à outra pessoa.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "mensagens** - Veja sua caixa de entrada de mensagens.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "fiança __@nome [use a menção para pagar a fiança de alguém]__** - Está preso? Pague sua fiança e seja livre.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "trabalhar __ajuda__** - Seja um cidadão de bem e comece trabalhar.\n"
                        result += "- **" + \
                            str(self.prefix) + "hacker** - Hackeie o banco da cidade e fature reais, mas lembre-se você pode ser preso.\n"
                        result += "- **" + \
                            str(self.prefix) + "inv** - Veja seu inventário.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "caracoroa __cara ou coroa__** - Jogue cara ou coroa e fature dinheiro.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "atirar __@nome__** - Atire em alguém que está te incomodando.\n"
                        result += "- **" + \
                            str(self.prefix) + "comer** - Use este comando para não morrer de fome, você pode comprar comidas na loja.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "loja** - Confira a loja com comidas, armas, balas, entre outros.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "comprar __ID do item__ __quantidade__** - Compre um item da loja.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "ranking __[mortes,banco,carteira,presos,nivel]__** - Confira quem está no ranking.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "rankingglobal __[mortes,banco,carteira,presos,nivel]__** - Confira quem está no ranking global.\n"
                        result += "- **" + \
                            str(self.prefix) + \
                            "cor __hex da cor, ex: 1C1C1C__** - Troque a cor do seu nome por **20.000** reais.\n\n"

                        await message.channel.send(message.author.mention, embed=discord.Embed(title=title, description=result, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Roleplay BOT desenvolvido por raddis#4444.").set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)).set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/rpg-1691444-1441510.png"))

                elif command in ['perfil']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        member = None
                        title = "Seu perfil %s:" % (await self.getMemberUsername(message.author))
                        if argsCount < 1:
                            user = rpgUser
                        else:
                            memberValue = args[0]
                            if len(message.mentions) > 0:
                                member = discord.utils.get(
                                    message.guild.members, id=message.mentions[0].id)
                            elif memberValue.isdigit():
                                member = discord.utils.get(
                                    client.get_all_members(), id=int(memberValue))
                            else:
                                member = discord.utils.get(
                                    message.guild.members, name=memberValue)

                            if member:
                                if member.bot:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                title = "Perfil de %s:" % (await self.getMemberUsername(member))
                                user = await self.getUser(member.id, message.guild.id)
                            else:
                                user = rpgUser

                        embed = discord.Embed(title=":bust_in_silhouette: | " + str(title), colour=0xFFBF00).set_thumbnail(url=member.avatar_url if member != None else message.author.avatar_url).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        embed.add_field(name=":dollar: Dinheiro na Carteira", value=str(
                            user["xp_points"]), inline=True)
                        embed.add_field(name=":moneybag: Dinheiro no Banco", value=str(
                            user["xp_deposited"]), inline=True)
                        embed.add_field(
                            name=":skull: Morreu", value="%s vezes." % user["deaths"], inline=True)
                        embed.add_field(
                            name=":gun: Matou", value="%s vezes." % user["kills"], inline=True)
                        embed.add_field(name=":cut_of_meat: Fome",
                                        value=user["hunger"], inline=True)
                        embed.add_field(name=":heart: Vida",
                                        value=user["health"], inline=True)
                        embed.add_field(name=":police_officer: Prendeu",
                                        value="%s pessoas." % user["arrested"], inline=True)
                        embed.add_field(name=":star: Nível", value="%s (%s para nível %s)" % (
                            user["level"], 100 - user["progress_level"], user["level"] + 1), inline=True)
                        embed.add_field(name=":oncoming_police_car: Procurado(a)",
                                        value="Sim" if user["wanted"] == "1" else "Não", inline=True)
                        if await self.haveItem(next(iter(item for item in itemsList if itemsList[item]['name'] == "Colete"), None), user):
                            embed.add_field(
                                name=":shield: Colete", value=user["westcoast"], inline=True)
                        if user["married_id"] != "" and user["married_id"] != "0" and user["married_id"] != None:
                            marriedMember = discord.utils.get(
                                message.guild.members, id=int(user["married_id"]))
                            if marriedMember:
                                embed.add_field(name=":couple_with_heart_woman_man: Casado(a) com", value="%s#%s" % (
                                    marriedMember.name, marriedMember.discriminator), inline=True)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['loja', 'shop']:
                    async with message.channel.typing():
                        itemsEmbeds = [discord.Embed(title=":shopping_cart: | Olá %s, seja bem-vindo à minha loja, confira:" % (await self.getMemberUsername(message.author)), colour=0xFFBF00).set_thumbnail(url="https://shopheroes.com/assets/images/icons/icon-shop01.png").set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))]

                        fields = 0
                        countEmbeds = 0
                        for item in itemsList:
                            fields += 1
                            if fields >= 25:
                                fields = 0
                                countEmbeds += 1
                                itemsEmbeds.append(
                                    discord.Embed(colour=0xFFBF00))

                            itemsEmbeds[countEmbeds].add_field(name=":small_orange_diamond: ID **%s** | %s %s" % (item, itemsList[item]["name"], "- +" + str(itemsList[item]["eating"]) + " de fome" if itemsList[item]["food"] else "- " + str(
                                itemsList[item]["damage"]) + " de dano" if itemsList[item]["gun"] else ""), value="__Preço:__ **%s** reais." % itemsList[item]["price"], inline=True)

                        rolesEmbeds = [discord.Embed(colour=0xFFBF00)]

                        fields = 0
                        countEmbeds = 0
                        for role in roles:
                            if role >= 100:
                                fields += 1
                                if fields >= 25:
                                    fields = 0
                                    countEmbeds += 1
                                    rolesEmbeds.append(
                                        discord.Embed(colour=0xFFBF00))

                                rolesEmbeds[countEmbeds].add_field(name=":small_orange_diamond: ID **%s** | Cargo %s" % (
                                    role, roles[role]["name"]), value="__Preço:__ **%s** reais." % roles[role]["price"], inline=True)

                        i = 1
                        for embed in itemsEmbeds:
                            if i == 1:
                                await message.channel.send(message.author.mention, embed=embed)
                            else:
                                await message.channel.send(embed=embed)
                            i += 1

                        for embed in rolesEmbeds:
                            await message.channel.send(embed=embed)

                        await message.channel.send(":shopping_cart: | Para comprar algo da minha loja, digite **!comprar __ID do item__ __quantidade(opcional)__**.")

                elif command in ['ranking', 'rank', 'rankingglobal', 'rankglobal']:
                    async with message.channel.typing():
                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar o tipo do ranking que deseja ver.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        type = argsNotSplited
                        types = ["mortes", "banco",
                                 "carteira", "presos", "nivel"]
                        if type in types:
                            cursor = await self.getCursor()
                            if cursor == None:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, desculpe **%s**, não foi possível conectar ao banco de dados." % await self.getMemberUsername(message.author), colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            tableTypes = {"mortes": "kills", "banco": "xp_deposited",
                                          "carteira": "xp_points", "presos": "arrested", "nivel": "level"}
                            emoji = {"mortes": ":skull:", "banco": ":moneybag:",
                                     "carteira": ":coin:", "presos": ":police_officer:", "nivel": ":star:"}
                            cursor.execute("select * from users where guild_id = '%s' order by %s desc limit 10" % (message.guild.id,
                                                                                                                    tableTypes[type]) if command in ["ranking", "rank"] else "select * from users order by %s desc" % (tableTypes[type]))
                            data = cursor.fetchall()
                            result = ""
                            count = 1
                            for user in data:
                                if count > 10:
                                    break

                                member = discord.utils.get(
                                    client.get_all_members(), id=int(user["user_id"]))
                                if member is not None:
                                    result += "%s - **%s** - %s %s.\n" % (":first_place:" if count == 1 else ":second_place:" if count == 2 else ":third_place:" if count == 3 else (
                                        "%s️⃣" % count if count < 10 else ":keycap_ten:"), "%s#%s" % (member.name, member.discriminator), user[tableTypes[type]], "reais" if type == "carteira" or type == "banco" else type)
                                count += 1

                            if result == "":
                                result = "Oops, nada foi encontrado. :("

                            await message.channel.send(message.author.mention, embed=discord.Embed(title="%s | Ranking de %s:" % (emoji[type], type), description=result, colour=0xFFBF00).set_thumbnail(url='https://image.flaticon.com/icons/png/512/856/856984.png').set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="O tipo de ranking informado não existe, veja os disponíveis: __%s__." % str(types).replace("'", ""), colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))

                elif command in ['cor']:
                    async with message.channel.typing():
                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, informe a cor que deseja, veja abaixo:", colour=0xFF0000).set_image(url="https://cdn.discordapp.com/attachments/680606294792601613/688800186427768944/hex-color.png").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["level"]) < 5:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 5** para trocar a cor do seu nome.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if 20000 > rpgUser["xp_points"] and not message.author.id in ownersId:
                            await message.channel.send(":no_entry: | **%s**, você precisa de **20.000 reais** em carteira para trocar a cor do seu nome, você tem somente **%s**." % (message.author.mention, rpgUser["xp_points"]))
                            return

                        hex_int = int("0x" + str(args[0].replace("#", "")), 16)
                        myColourRole = discord.utils.get(
                            message.guild.roles, name=str(message.author.id))
                        if myColourRole is None:
                            role = await message.guild.create_role(name=message.author.id, colour=discord.Colour(hex_int))
                            await role.edit(position=max(int(role.position) for role in message.author.roles))
                        else:
                            await myColourRole.edit(colour=hex_int, position=max(int(role.position) for role in message.author.roles) if myColourRole.position == 0 else myColourRole.position)

                        if discord.utils.get(message.author.roles, name=str(message.author.id)) is None:
                            await message.author.add_roles(myColourRole if myColourRole != None else role)

                        await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - 20000, message.guild.id)
                        await message.channel.send(message.author.mention, embed=discord.Embed(title="Cor alterada com sucesso!", description="A cor do seu nome foi alterada com sucesso por **20.000** reais!", colour=hex_int).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))

                elif command in ['atirar', 'ataque']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 15:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **15** de fome para atirar, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        shootTime = int(rpgUser["shoot_time"])
                        if shootTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **1 minuto** para atirar novamente." % (message.author.mention))
                            return

                        hourNow = datetime.now().hour
                        if hourNow > 23 and hourNow < 7:
                            sort = random.choice([1, 1, 0, 0, 1, 0, 0, 0, 0])
                            if sort == 1:
                                await self.updateUser("stuck", message.author.id, 1, message.guild.id)
                                await self.updateUser("stuck_time", message.author.id, time.time() + 86400, message.guild.id)
                                await message.channel.send(":man_police_officer: | **%s**, sua tentativa de atirar falhou e você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                                await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)
                                return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Mencione a pessoa que você deseja atirar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            await self.updateUser("shoot_time", message.author.id, time.time() + 60, message.guild.id)

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode atirar em você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserToBall = await self.getUser(member.id, message.guild.id)
                            if rpgUserToBall == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if int(rpgUserToBall["health"]) < 1:
                                await message.channel.send(":skull: | **%s**, esta pessoa está morta!" % (message.author.mention))
                                return

                            if rpgUserToBall["stuck"] == "1":
                                await message.channel.send(":man_police_officer: | **%s**, você não pode atirar em quem está preso!" % (message.author.mention))
                                return

                            if rpgUser["items"] == "" or rpgUser["items"] == None:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui nenhuma arma, compre algo na **loja**.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":gun: | Escolha a arma que deseja usar %s:" % (await self.getMemberUsername(message.author)), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            myItemList = eval(rpgUser["items"])
                            i = 1
                            for item in sorted(set(myItemList)):
                                if i > 9:
                                    break

                                if not itemsList[int(item)]["gun"] and not itemsList[int(item)]["whitegun"]:
                                    continue

                                embed.add_field(name="%s️⃣ | %s - Dano: %s" % (i, itemsList[int(item)]["name"], itemsList[int(
                                    item)]["damage"]), value="Quantidade: **%s**." % myItemList.count(item), inline=False)
                                i += 1

                            embed.add_field(
                                name="Balas", value=rpgUser["bullets"], inline=False)

                            if i == 1:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Sua lista de itens está vazia, compre alguma arma.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            msgGive = await message.channel.send(message.author.mention, embed=embed)

                            i = 1
                            for item in sorted(set(myItemList)):
                                if i > 9:
                                    break

                                if not itemsList[int(item)]["gun"] and not itemsList[int(item)]["whitegun"]:
                                    continue

                                await msgGive.add_reaction("%s️⃣" % i)
                                i += 1

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == msgGive.id and user == message.author and client.user.id != user.id)
                            except asyncio.TimeoutError:
                                await msgGive.delete()
                            else:
                                await msgGive.delete()

                                sort = random.choice(
                                    [1, 1, 0, 0, 1, 0, 0, 0, 1])
                                if sort == 1:
                                    await message.channel.send(":gun: | **%s**, você errou o tiro, melhore sua mira!" % (message.author.mention))
                                    return

                                i = 1
                                for item in sorted(set(myItemList)):
                                    if i > 9:
                                        break

                                    if not itemsList[int(item)]["gun"] and not itemsList[int(item)]["whitegun"]:
                                        continue

                                    if reaction.emoji == "%s️⃣" % i:
                                        myGun = itemsList[item]

                                        if int(rpgUser["bullets"]) < 1 and not itemsList[int(item)]["whitegun"]:
                                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui balas, compre na **loja**.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                            return

                                        damage = myGun["damage"]

                                        if not itemsList[int(item)]["whitegun"]:
                                            await self.updateUser("bullets", message.author.id, rpgUser["bullets"] - 1, message.guild.id)

                                        policeRole = discord.utils.get(
                                            message.author.roles, name=roles[100]["name"])
                                        if policeRole is None:
                                            await self.updateUser("wanted", message.author.id, 1, message.guild.id)

                                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)

                                        if not await self.haveItem(next(iter(item for item in itemsList if itemsList[item]['name'] == "Colete"), None), rpgUserToBall):
                                            resultMessage = ":broken_heart: | Cuidado **%s**! Você sofreu um ataque de **%s** e agora está com **%s** de vida!" % (
                                                member.mention, myGun["name"], rpgUserToBall["health"] - damage)
                                            await self.updateUser("health", member.id, rpgUserToBall["health"] - damage, message.guild.id)
                                            if rpgUserToBall["health"] - damage < 1:
                                                if policeRole is not None and rpgUserToBall["wanted"] == "0":
                                                    await message.author.remove_roles(policeRole)
                                                    embed = discord.Embed(description="Você foi pego matando pessoas sem motivo e por isso perdeu seu cargo de policial.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                                else:
                                                    await self.updateUser("health", member.id, 0, message.guild.id)
                                                    await self.updateUser("deaths", member.id, rpgUserToBall["deaths"] + 1, message.guild.id)
                                                    await self.updateUser("kills", message.author.id, rpgUser["kills"] + 1, message.guild.id)
                                                    resultMessage = ":broken_heart: | **%s**, você morreu com um ataque de **%s**!" % (
                                                        member.mention, myGun["name"])
                                                    embed = discord.Embed(title=":skull: | Você matou %s!" % await self.getMemberUsername(member), colour=0xFFBF00).set_image(url="https://i.ytimg.com/vi/szXf3hvb_wM/maxresdefault.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                        else:
                                            resultMessage = ":shield: | Cuidado **%s**! Você sofreu um ataque de **%s** e agora está com **%s** de dano em seu colete!" % (
                                                member.mention, myGun["name"], damage - 5)

                                            if rpgUserToBall["westcoast"] - damage + 5 < 1:
                                                if rpgUserToBall["items"] != None and rpgUserToBall["items"] != "":
                                                    userBallItems = eval(
                                                        rpgUserToBall["items"])
                                                    userBallItems.remove(11)
                                                    await self.updateUser("items", member.id, userBallItems, message.guild.id)
                                                    await self.updateUser("westcoast", member.id, 0, message.guild.id)
                                                    resultMessage = ":shield: | **%s**, você sofreu um ataque e perdeu seu colete!" % (
                                                        member.mention)
                                            else:
                                                await self.updateUser("westcoast", member.id, rpgUserToBall["westcoast"] - damage + 5, message.guild.id)

                                        if not (rpgUserToBall["health"] - damage < 1):
                                            embed = discord.Embed(title=(":gun: | Você atirou em %s!" % await self.getMemberUsername(member) if myGun["gun"] else ":dagger: | Você atacou %s." % await self.getMemberUsername(member)), description=("Você atirou em **%s** com sua **%s**, agora você possui **%s** balas." % (member.mention, myGun["name"], rpgUser["bullets"] - 1) if myGun["gun"] else "Você atacou **%s** com sua **%s**." % (member.mention, myGun["name"])), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)).set_image(url="https://i.makeagif.com/media/3-21-2016/49Kkgj.gif" if myGun["gun"] else "https://media1.tenor.com/images/0514c4b5ac57502c189514d1eff028dd/tenor.gif?itemid=14229263")

                                        await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                                        await message.channel.send(resultMessage)
                                    i += 1

                                await message.channel.send(message.author.mention, embed=embed)

                elif command in ['comprar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar o ID do item que deseja comprar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if not args[0].isdigit():
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        itemID = int(args[0].strip())
                        if itemID >= 100 and itemID in roles:
                            role = roles[itemID]
                            dRole = discord.utils.get(
                                message.guild.roles, name=role["name"])
                            if dRole is not None:
                                if discord.utils.get(message.author.roles, name=role["name"]) is not None:
                                    embed = discord.Embed(description="Você já possui esse cargo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    if int(role["price"]) > rpgUser["xp_points"]:
                                        await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para comprar o cargo **%s**." % role["name"], colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                        return

                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - int(role["price"]), message.guild.id)
                                    await self.updateUser("wanted", message.author.id, 0, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 1, message.guild.id)
                                    await self.updateLevel(rpgUser, 1, message.channel, message.guild.id)
                                    embed = discord.Embed(title=":shopping_cart: | Cargo comprado com sucesso!", description="Parabéns, você comprou o cargo **%s** por **%s** reais com sucesso." % (dRole.mention, role["price"]), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await message.author.add_roles(dRole)
                            else:
                                embed = discord.Embed(description="Ocorreu um erro ao comprar o cargo, reporte ao proprietário do bot.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        elif argsCount < 2:
                            if itemID in itemsList:
                                item = itemsList[itemID]
                                itemPrice = int(item["price"])
                                itemName = item["name"]
                                myItemList = []
                                if rpgUser["items"] != None and rpgUser["items"] != "":
                                    myItemList = eval(rpgUser["items"])

                                if itemPrice > rpgUser["xp_points"]:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para comprar **%s**." % itemName, colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if bool(item["bullets"]):
                                    await self.updateUser("bullets", message.author.id, rpgUser["bullets"] + item["amount"], message.guild.id)
                                else:
                                    if bool(item["westcoast"]):
                                        await self.updateUser("westcoast", message.author.id, 100, message.guild.id)
                                        if rpgUser["westcoast"] > 0:
                                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode comprar outro colete enquanto tiver um já em uso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                            return

                                    myItemList.append(itemID)
                                    await self.updateUser("items", message.author.id, myItemList, message.guild.id)

                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 1, message.guild.id)
                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - itemPrice, message.guild.id)
                                await self.updateLevel(rpgUser, 1, message.channel, message.guild.id)
                                embed = discord.Embed(title=":shopping_cart: | Item comprado com sucesso!", description="Parabéns, você comprou **%s** por **%s** reais com sucesso." % (itemName, itemPrice), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            else:
                                embed = discord.Embed(description="O ID do item informado não foi encontrado na loja.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        else:
                            if not args[1].isdigit():
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            amount = int(args[1].strip())
                            if amount < 2:
                                embed = discord.Embed(description="Informe um valor maior que **1**.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                            elif itemID in itemsList:
                                i = 0
                                item = itemsList[itemID]
                                totalPrice = 0
                                myItemList = []
                                if rpgUser["items"] != None and rpgUser["items"] != "":
                                    myItemList = eval(rpgUser["items"])

                                while i < amount:
                                    myItemList.append(itemID)
                                    totalPrice += int(item["price"])
                                    i += 1

                                itemName = item["name"]

                                if totalPrice > rpgUser["xp_points"]:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para comprar __%s__ quantidades de **%s**." % (amount, itemName), colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if bool(item["westcoast"]):
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você só pode comprar **um** colete por vez.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if bool(item["bullets"]):
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Este item não pode ser comprado em quantidade.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                else:
                                    await self.updateUser("items", message.author.id, myItemList, message.guild.id)

                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 1, message.guild.id)
                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - totalPrice, message.guild.id)
                                await self.updateLevel(rpgUser, 1, message.channel, message.guild.id)
                                embed = discord.Embed(title=":shopping_cart: | Item comprado com sucesso!", description="Parabéns, você comprou __%s__ quantidades de **%s** por **%s** reais com sucesso." % (amount, itemName, totalPrice), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            else:
                                embed = discord.Embed(description="O ID do item informado não foi encontrado na loja.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['caracoroa', 'coinflip']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 10:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **10** de fome para jogar cara ou coroa, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        betTime = int(rpgUser["coinflip_time"])
                        if betTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **15 segundos** para jogar novamente." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar cara ou coroa.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        type = args[0].lower()

                        if not type in ["cara", "coroa"]:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar cara ou coroa.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        sort = random.choice(
                            ["cara", "coroa", "coroa", "cara", "cara", "coroa"])
                        if sort == type.lower():
                            coinSort = random.randint(10, 130)
                            embed = discord.Embed(title="Você teve sorte!", description="Você teve sorte e ganhou **%s** reais." % coinSort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + coinSort, message.guild.id)
                            await self.updateLevel(rpgUser, 2 if rpgUser["level"] < 8 else 1, message.channel, message.guild.id)
                        else:
                            embed = discord.Embed(title="Não foi dessa vez :(", description="Não foi dessa vez. Quem sabe na próxima!", colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                        await self.updateUser("coinflip_time", message.author.id, time.time() + 15, message.guild.id)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['apostar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 10:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **10** de fome para apostar, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        betTime = int(rpgUser["bet_time"])
                        if betTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **20 segundos** para apostar novamente." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar a quantidade que deseja apostar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if not args[0].isdigit() and not args[0].lower() in ["tudo", "all"]:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if args[0].lower() in ["tudo", "all"]:
                            amount = rpgUser["xp_points"]
                        else:
                            amount = int(args[0].strip())

                        if amount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Aposte um valor maior que **0**.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if amount > int(rpgUser["xp_points"]):
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para apostar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        sort = random.choice([0, 0, 1, 0, 1, 1, 0, 0, 0, 1])
                        if sort == 1:
                            embed = discord.Embed(title="Você está com sorte!", description="Você teve sorte e ganhou **%s** reais." % amount, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + amount, message.guild.id)
                            await self.updateLevel(rpgUser, 2 if rpgUser["level"] < 8 else 1, message.channel, message.guild.id)
                        else:
                            embed = discord.Embed(title="Não foi dessa vez :(", description="Não foi dessa vez, você perdeu **%s** reais. Quem sabe na próxima!" % amount, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - amount, message.guild.id)

                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 5, message.guild.id)
                        await self.updateUser("bet_time", message.author.id, time.time() + 20, message.guild.id)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['daily', 'diario']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 10:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **10** de fome para pegar seu prêmio, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        dailyTime = int(rpgUser["daily_time"])
                        if dailyTime > time.time():
                            dateToNewDaily = datetime.utcfromtimestamp(
                                int(rpgUser["daily_time"])).strftime('%d/%m/%Y %H:%M:%S')
                            await message.channel.send(":no_entry: | **%s**, você deve esperar até **%s** para coletar seu prêmio novamente." % (message.author.mention, dateToNewDaily))
                            return

                        sort = random.randint(10, 400)
                        embed = discord.Embed(title=":dollar: | Você ganhou %s reais em seu prêmio diário." % sort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                        await self.updateUser("daily_time", message.author.id, time.time() + 86400, message.guild.id)
                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                        await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['week', 'semanal']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 10:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **10** de fome para pegar seu prêmio, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        dailyTime = int(rpgUser["week_time"])
                        if dailyTime > time.time():
                            dateToNewDaily = datetime.utcfromtimestamp(
                                int(rpgUser["week_time"])).strftime('%d/%m/%Y %H:%M:%S')
                            await message.channel.send(":no_entry: | **%s**, você deve esperar até **%s** para coletar seu prêmio novamente." % (message.author.mention, dateToNewDaily))
                            return

                        sort = random.randint(10, 500)
                        embed = discord.Embed(title=":dollar: | Você ganhou %s reais em seu prêmio semanal." % sort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                        await self.updateUser("week_time", message.author.id, time.time() + 604800, message.guild.id)
                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                        await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['mensal', 'month']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 10:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **10** de fome para pegar seu prêmio, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        dailyTime = int(rpgUser["month_time"])
                        if dailyTime > time.time():
                            dateToNewDaily = datetime.utcfromtimestamp(
                                int(rpgUser["month_time"])).strftime('%d/%m/%Y %H:%M:%S')
                            await message.channel.send(":no_entry: | **%s**, você deve esperar até **%s** para coletar seu prêmio novamente." % (message.author.mention, dateToNewDaily))
                            return

                        sort = random.randint(10, 500)
                        embed = discord.Embed(title=":dollar: | Você ganhou %s reais em seu prêmio mensal." % sort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                        await self.updateUser("month_time", message.author.id, time.time() + 2592000, message.guild.id)
                        await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                        await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['depositar', 'dep']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar a quantidade que deseja depositar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if args[0].lower() == "tudo" or args[0].lower() == "all":
                            if rpgUser["xp_points"] < 1:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa ter mais de **1 real** em carteira para depositar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":dollar: | Depósito realizado com sucesso!", description="Você depositou **%s** reais com sucesso no banco." % rpgUser["xp_points"], colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - rpgUser["xp_points"], message.guild.id)
                            await self.updateUser("xp_deposited", message.author.id, rpgUser["xp_deposited"] + rpgUser["xp_points"], message.guild.id)
                        else:
                            if not args[0].isdigit():
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            amount = int(args[0].strip())

                            if amount > int(rpgUser["xp_points"]):
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para depositar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if amount < 1:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Digite um valor maior que 1 para depositar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":dollar: | Você depositou com sucesso!", description="Você depositou **%s** reais com sucesso no banco." % amount, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - amount, message.guild.id)
                            await self.updateUser("xp_deposited", message.author.id, rpgUser["xp_deposited"] + amount, message.guild.id)
                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['sacar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar a quantidade que deseja sacar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if args[0].lower() == "tudo" or args[0].lower() == "all":
                            if rpgUser["xp_deposited"] < 1:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa ter mais de **1 real** em banco para depositar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":dollar: | Saque realizado com sucesso!", description="Você sacou **%s** reais com sucesso do banco." % rpgUser["xp_deposited"], colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_deposited", message.author.id, rpgUser["xp_deposited"] - rpgUser["xp_deposited"], message.guild.id)
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_deposited"] + rpgUser["xp_points"], message.guild.id)
                        else:
                            if not args[0].isdigit():
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            amount = int(args[0].strip())

                            if amount < 1:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Digite um valor maior que 1 para sacar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if amount > int(rpgUser["xp_deposited"]):
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui dinheiro suficiente para sacar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":dollar: | Saque realizado com sucesso!", description="Você sacou **%s** reais com sucesso." % amount, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + amount, message.guild.id)
                            await self.updateUser("xp_deposited", message.author.id, rpgUser["xp_deposited"] - amount, message.guild.id)

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['carroforte']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        channel = await self.getChannel(rp_channel, message.guild)
                        if channel != None:
                            sort = random.randint(1000, 3000)
                            embed = discord.Embed(title=":moneybag: | Um carro forte da polícia acabou de capotar!", description="Um carro forte acabou de capotar em sentido a Beverlly Hills com **%s** reais, **REAJA** para roubá-lo! Mas lembre-se, você será procurado pela polícia!" %
                                                  sort, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S"))
                            strongCarMessage = await channel.send(embed=embed)
                            await strongCarMessage.add_reaction("💰")

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == strongCarMessage.id and reaction.emoji == "💰" and rpgUser != None and rpgUser["stuck"] == "0" and client.user.id != user.id)
                            except asyncio.TimeoutError:
                                await strongCarMessage.delete()
                            else:
                                await strongCarMessage.delete()
                                rpgUser = await self.getUser(user.id, message.guild.id)
                                if rpgUser != None:
                                    await self.updateUser("xp_points", user.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateUser("wanted", user.id, 1, message.guild.id)
                                    await self.updateLevel(rpgUser, 4, channel, message.guild.id)
                                    await channel.send(":moneybag: | **%s** roubou **%s** reais do carro forte e agora está sendo **procurado(a)** pela polícia!" % (user.mention, sort))

                elif command in ['admremove']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if not args[1].isdigit():
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        amount = int(args[1].strip())

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserToDeposited = await self.getUser(member.id, message.guild.id)
                            if rpgUserToDeposited == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            await self.updateUser("xp_points", member.id, rpgUserToDeposited["xp_points"] - amount, message.guild.id)

                            embed = discord.Embed(title=":dollar: | Dinheiro removido com sucesso!", description="Você removeu **%s** reais com sucesso de **%s**." % (amount, member.mention), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['disconnectbot']:
                    async with message.channel.typing():
                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        await message.channel.send(message.author.mention, embed=discord.Embed(title="Aguarde...", description="Aguarde! O BOT está sendo desconectado...", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        await self.destroy()
                        os._exit(0)

                elif command in ['ping']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        before = time.monotonic()
                        message = await message.channel.send(":ping_pong: | **Pong!**")
                        ping = (time.monotonic() - before) * 1000
                        await message.edit(content=f':ping_pong: | **Pong!** `{int(ping)}ms`')

                elif command in ['clear', 'limpar']:
                    async with message.channel.typing():
                        if not 'administrator' in permissions and not 'manage_messages' in permissions:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, você não tem permissão para usar esse comando.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, digite o número de mensagens que deseja deletar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        number = int(args[0].strip())
                        if number > 99:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, digite um número abaixo de 100.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        number = int(number)
                        await message.channel.delete_messages(await message.channel.history(limit=int(number+1)).flatten())
                        await message.channel.send('**%s** mensagens deletadas.' % number, delete_after=2)

                elif command in ['avatar']:
                    async with message.channel.typing():

                        member = None
                        if argsCount > 0:
                            memberValue = args[0]
                            if len(message.mentions) > 0:
                                member = discord.utils.get(
                                    message.guild.members, id=message.mentions[0].id)
                            elif memberValue.isdigit():
                                member = discord.utils.get(
                                    client.get_all_members(), id=int(memberValue))
                            else:
                                member = discord.utils.get(
                                    message.guild.members, name=memberValue)

                        if not member:
                            member = message.author

                        if member:
                            await message.channel.send(message.author.mention, embed=discord.Embed(title="Avatar de %s" % (await self.getMemberUsername(member)), description="Clique [aqui](%s) para baixar a imagem." % member.avatar_url, colour=member.color).set_image(url=member.avatar_url).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, algo deu errado, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))

                elif command in ['allmsg']:
                    async with message.channel.typing():
                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        for guild in client.guilds:
                            rpgRole = discord.utils.get(
                                guild.roles, name=roles[99]["name"])
                            channel = await self.getChannel(rp_channel, guild)
                            if channel != None:
                                cMessage = "" if argsCount <= 1 else argsNotSplited.split(" ", 0)[
                                    0]
                                if cMessage != "":
                                    if rpgRole != None:
                                        cMessage = cMessage.replace(
                                            "@rpg", rpgRole.mention)
                                    await channel.send(cMessage)

                elif command in ['leaveserver']:
                    async with message.channel.typing():
                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        guild = client.get_guild(int(args[0]))
                        if guild != None:
                            await guild.leave()
                            await message.channel.send(":white_check_mark: | Saída do servidor **%s** sucedida." % guild.name)

                elif command in ['servers']:
                    async with message.channel.typing():
                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        guilds = ""
                        for guild in client.guilds:
                            guilds += "[**%s**][__%s__] %s.\n" % (
                                guild.id, len(guild.members), guild.name)
                        await message.channel.send("Online in guilds: \n%s" % (guilds[:-2]))

                elif command in ['admpay']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if not args[1].isdigit():
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        amount = int(args[1].strip())

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserToDeposited = await self.getUser(member.id, message.guild.id)
                            if rpgUserToDeposited == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            await self.updateUser("xp_points", member.id, rpgUserToDeposited["xp_points"] + amount, message.guild.id)

                            embed = discord.Embed(title=":dollar: | Pagamento realizado com sucesso!", description="Você pagou **%s** reais com sucesso para **%s**." % (amount, member.mention), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['setvalue']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                message.guild.members, id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            table = args[1]
                            rpgUserToValue = await self.getUser(member.id, message.guild.id)
                            if rpgUserToValue == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            await self.updateUser(table, member.id, args[2], message.guild.id)
                            await message.channel.send("**%s** %s: %s -> %s" % (member.name, args[1], rpgUserToValue[table], args[2]))
                            return
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['viewvalue']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            table = args[1]
                            rpgUserToValue = await self.getUser(member.id, message.guild.id)
                            if rpgUserToValue == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            await message.channel.send("**%s** %s: %s" % (member.name, args[1], rpgUserToValue[table]))
                            return
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['transferir', 'pay']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos, veja se você digitou corretamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if not args[1].isdigit():
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar um valor inteiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        amount = int(args[1].strip())

                        if amount > int(rpgUser["xp_points"]):
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não possui reais suficientes para transferir.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode transferir para si mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserToDeposited = await self.getUser(member.id, message.guild.id)
                            if rpgUserToDeposited == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            await self.updateUser("xp_points", member.id, rpgUserToDeposited["xp_points"] + amount, message.guild.id)
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - amount, message.guild.id)

                            embed = discord.Embed(title=":dollar: | Transferência realizada com sucesso!", description="Você transferiu **%s** reais com sucesso para **%s**." % (amount, member.mention), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['inv', 'inventario']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if rpgUser["items"] == "" or rpgUser["items"] == None:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Seu inventário está vazio, compre algo na **loja**.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            myItemList = eval(rpgUser["items"])

                            embed = discord.Embed(title="Confira seu inventário %s:" % (await self.getMemberUsername(message.author)), description="Você possui **%s** itens em seu inventário." % len(sorted(set(myItemList))), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)).set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png")
                            for item in sorted(set(myItemList)):
                                embed.add_field(name="%s" % (itemsList[int(
                                    item)]["name"]), value="Quantidade: **%s**." % myItemList.count(item), inline=False)

                            embed.add_field(
                                name="Balas", value=rpgUser["bullets"], inline=False)
                            await message.channel.send(message.author.mention, embed=embed)

                elif command in ['mensagens', 'correio']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["items"] == "" or rpgUser["items"] == None:
                            await message.channel.send(":no_entry: | **%s**, você precisa ter um celular para poder ver suas mensagens, compre-o na **loja**." % (message.author.mention))
                            return

                        if not await self.haveItem(next(iter(item for item in itemsList if itemsList[item]['name'] == "Celular"), None), rpgUser):
                            await message.channel.send(":no_entry: | **%s**, você precisa ter um celular para poder ver suas mensagens, compre-o na **loja**." % (message.author.mention))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 30:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para ver mensagens, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        cursor = await self.getCursor()
                        cursor.execute(
                            "select * from messages where user_to_id = '%s' order by `id` desc" % (message.author.id))
                        messages = cursor.fetchall()

                        cursor.execute(
                            "select * from messages where user_to_id = '%s' and `read` = '0' order by `id` desc" % (message.author.id))
                        noReadMessages = cursor.fetchall()

                        embed = discord.Embed(title=":e_mail: | Veja suas mensagens abaixo %s:" % (await self.getMemberUsername(message.author)), description="Você possui **" + str(len(messages)) + "** " + str("mensagem" if len(messages) < 2 else "mensagens") + ", " + str(("**" + str(len(noReadMessages)) + "** não " + str("lida" if len(noReadMessages) < 2 else "lidas")) if len(noReadMessages) > 0 else "**todas lidas**") + ".\nAs mensagens que você deseja ler serão enviadas para o seu privado, mantenha-o ativado.", colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        i = 1
                        for cMessage in messages:
                            if i > 9:
                                break

                            fromMember = discord.utils.get(
                                client.get_all_members(), id=int(cMessage["user_from_id"]))
                            if not fromMember is None:
                                embed.add_field(name="%s️⃣ | Mensagem enviada por **%s#%s**." % (i, fromMember.name, fromMember.discriminator), value="Em **%s**. **__%s__**" % (
                                    datetime.utcfromtimestamp(cMessage["timestamp"]).strftime('%d/%m/%Y %H:%M:%S'), "Não lida." if cMessage["read"] == "0" else "Lida."), inline=False)
                            i += 1

                        msgGive = await message.channel.send(message.author.mention, embed=embed)

                        i = 1
                        for cMessage in messages:
                            await msgGive.add_reaction("%s️⃣" % i)
                            i += 1

                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == msgGive.id and user == message.author and client.user.id != user.id)
                        except asyncio.TimeoutError:
                            await msgGive.delete()
                        else:
                            await msgGive.delete()
                            i = 1
                            for cMessage in messages:
                                if i > 9:
                                    break

                                if reaction.emoji == "%s️⃣" % i:
                                    fromMember = discord.utils.get(
                                        client.get_all_members(), id=int(cMessage["user_from_id"]))

                                    try:
                                        cursor.execute(
                                            "update messages set `read` = '1' where id = '%s'" % cMessage["id"])
                                        await message.channel.send(embed=discord.Embed(title=":e_mail: | %s, enviei a mensagem para seu privado." % await self.getMemberUsername(message.author), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                        await user.send(embed=discord.Embed(title=":e_mail: | Mensagem enviada por %s#%s:" % (fromMember.name, fromMember.discriminator), description=cMessage["message"], colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    except:
                                        await message.channel.send(":no_entry: | **%s**, não foi possível enviar a mensagem para o seu privado, permita mensagens diretas para recebê-la." % (message.author.mention))

                elif command in ['enviarmensagem']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["items"] == "" or rpgUser["items"] == None:
                            await message.channel.send(":no_entry: | **%s**, você precisa ter um celular para poder ver suas mensagens, compre-o na **loja**." % (message.author.mention))
                            return

                        if not await self.haveItem(next(iter(item for item in itemsList if itemsList[item]['name'] == "Celular"), None), rpgUser):
                            await message.channel.send(":no_entry: | **%s**, você precisa ter um celular para poder ver suas mensagens, compre-o na **loja**." % (message.author.mention))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 30:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para enviar mensagens, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        if argsCount < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Está faltando argumentos aí... tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode enviar uma mensagem para mim.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode enviar uma mensagem para você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            cMessage = "" if argsCount <= 1 else argsNotSplited.split(" ", 1)[
                                1]
                            if cMessage != "":
                                cursor.execute("insert into messages (user_from_id, user_to_id, message, timestamp) values ('%s','%s','%s','%s')" % (
                                    message.author.id, member.id, cMessage, time.time()))
                                self.database.commit()
                                embed = discord.Embed(description="Mensagem enviada com sucesso para **%s**." % member.mention, colour=0x87CEEB).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                try:
                                    await member.send(embed=discord.Embed(title=":e_mail: | Hey %s! Cheque sua caixa de entrada digitando **%smensagens**, você tem uma nova mensagem de **%s** em **%s**!" % (member.name, self.prefix, message.author.name, message.guild.name), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                except:
                                    await message.channel.send(embed=discord.Embed(title=":e_mail: | Hey %s! Cheque sua caixa de entrada digitando **%smensagens**, você tem uma nova mensagem de %s!" % (member.name, self.prefix, message.author.name), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['comer']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["items"] == None or rpgUser["items"] == "":
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Sua lista de itens está vazia, compre algo para se alimentar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        embed = discord.Embed(title=":cut_of_meat: | Escolha o item que deseja comer %s:" % (await self.getMemberUsername(message.author)), description="Atualmente você possui **%s** de fome." % rpgUser["hunger"], colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        myItemList = eval(rpgUser["items"])
                        i = 1
                        for item in sorted(set(myItemList)):
                            if i > 9:
                                break

                            if not itemsList[int(item)]["food"]:
                                continue

                            embed.add_field(name="%s️⃣ | %s - +%s" % (i, itemsList[int(item)]["name"], itemsList[int(
                                item)]["eating"]), value="Quantidade: **%s**." % myItemList.count(item), inline=False)
                            i += 1

                        if i == 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Sua lista de itens está vazia, compre algo para se alimentar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        msgGive = await message.channel.send(message.author.mention, embed=embed)

                        i = 1
                        for item in sorted(set(myItemList)):
                            if i > 9:
                                break

                            if not itemsList[int(item)]["food"]:
                                continue

                            await msgGive.add_reaction("%s️⃣" % i)
                            i += 1

                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == msgGive.id and user == message.author and client.user.id != user.id)
                        except asyncio.TimeoutError:
                            await msgGive.delete()
                        else:
                            await msgGive.delete()
                            i = 1
                            for item in sorted(set(myItemList)):
                                if i > 9:
                                    break

                                if not itemsList[int(item)]["food"]:
                                    continue

                                if reaction.emoji == "%s️⃣" % i:
                                    hunger = int(rpgUser["hunger"])
                                    eating = int(
                                        itemsList[int(item)]["eating"])
                                    totalHunger = hunger + eating
                                    if hunger >= 100:
                                        await message.channel.send(":no_entry: | **%s**, você não está com fome." % (message.author.mention))
                                        return

                                    if totalHunger > 100:
                                        totalHunger = 100

                                    myItemList.remove(item)
                                    await self.updateUser("items", message.author.id, myItemList, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, totalHunger, message.guild.id)
                                    if rpgUser["health"] < 100:
                                        totalHealth = rpgUser["health"] + \
                                            eating - 1
                                        if totalHealth > 100:
                                            totalHealth = 100
                                        await self.updateUser("health", message.author.id, totalHealth, message.guild.id)
                                    await self.updateLevel(rpgUser, 1, message.channel, message.guild.id)
                                    await message.channel.send(":shallow_pan_of_food: | **Muito bem %s!** Você comeu **%s** e agora está com **%s** de fome." % (message.author.mention, itemsList[int(item)]["name"], totalHunger))
                                i += 1

                elif command in ['soco', 'socar', 'murro']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 30:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para dar um soco, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        punchTime = int(rpgUser["punch_time"])
                        if punchTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **5 minutos** para dar um soco novamente." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa mencionar a pessoa que deseja dar um soco.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        hourNow = datetime.now().hour
                        if hourNow > 23 and hourNow < 7:
                            sort = random.choice([1, 1, 0, 0, 1, 0, 0, 0, 0])
                            if sort == 1:
                                await self.updateUser("stuck", message.author.id, 1, message.guild.id)
                                await self.updateUser("stuck_time", message.author.id, time.time() + 86400, message.guild.id)
                                await message.channel.send(":man_police_officer: | **%s**, sua tentativa de dar um soco falhou e você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                                await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)
                                return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            await self.updateUser("punch_time", message.author.id, time.time() + 300, message.guild.id)
                            sort = random.choice([1, 1, 1, 0, 1, 0, 0, 0, 0])
                            if sort == 1:
                                await message.channel.send(":punch: | **%s**, você errou o soco de **%s**!" % (message.author.mention, member.mention))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode dar um soco em você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserKilled = await self.getUser(member.id, message.guild.id)
                            if rpgUserKilled == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if int(rpgUserKilled["health"]) < 1:
                                await message.channel.send(":skull: | **%s**, esta pessoa está morta!" % (message.author.mention))
                                return

                            punchMessage = await message.channel.send(message.author.mention, embed=discord.Embed(description=":punch: | **%s**, **%s** está tentando te dar um soco, seja mais rápido e desvie!" % (member.mention, message.author.mention), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            await punchMessage.add_reaction("👊🏽")

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=3, check=lambda reaction, user: reaction.message.id == punchMessage.id and user == member and reaction.emoji == "👊🏽" and client.user.id != user.id)
                            except asyncio.TimeoutError:
                                await punchMessage.delete()
                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                await self.updateUser("health", member.id, rpgUserKilled["health"] - 3, message.guild.id)
                                await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                                await message.channel.send(message.author.mention, embed=discord.Embed(title=":punch: | Você deu um soco em %s!" % await self.getMemberUsername(member), colour=0xFFBF00).set_image(url="https://i.gifer.com/9Cbt.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            else:
                                await punchMessage.delete()
                                embed = discord.Embed(title=":punch: | Não foi dessa vez %s!" % await self.getMemberUsername(message.author), description="**%s** foi mais rápido que você e desviou o soco." % member.mention, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                # elif command in ['matar']:
                #     async with message.channel.typing():
                #         rpgUser = await self.getUser(message.author.id, message.guild.id)
                #         if rpgUser == None:
                #             await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                #             return

                #         if int(rpgUser["level"]) < 2:
                #             await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 2** para poder matar alguém.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #             return

                #         if rpgUser["stuck"] == "1":
                #             await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" %(message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                #             return

                #         if int(rpgUser["hunger"]) <= 30:
                #             await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para matar, use **%scomer** para se alimentar!" %(message.author.mention, self.prefix))
                #             return

                #         if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                #             await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" %(message.author.mention))

                #         if int(rpgUser["health"]) <= 15:
                #             await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." %(message.author.mention))
                #             return

                #         killTime = int(rpgUser["kill_time"])
                #         if killTime > time.time():
                #             await message.channel.send(":no_entry: | **%s**, você deve esperar **5 minutos** para matar novamente." %(message.author.mention))
                #             return

                #         hourNow = datetime.now().hour
                #         if hourNow > 23 and hourNow < 7:
                #             sort = random.choice([0, 1, 1, 0, 1, 0, 0, 0, 1])
                #             if sort == 1:
                #                 await self.updateUser("stuck", message.author.id, 1, message.guild.id)
                #                 await self.updateUser("stuck_time", message.author.id, time.time() + 86400, message.guild.id)
                #                 await message.channel.send(":man_police_officer: | **%s**, sua tentativa de matar falhou e você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" %(message.author.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                #                 await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)
                #                 return

                #         if argsCount < 1:
                #             await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa mencionar a pessoa que deseja matar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #             return

                #         memberValue = args[0]
                #         if len(message.mentions) > 0:
                #             member = discord.utils.get(
                #                 message.guild.members, id=message.mentions[0].id)
                #         elif memberValue.isdigit():
                #             member = discord.utils.get(
                #                 client.get_all_members(), id=int(memberValue))
                #         else:
                #             member = discord.utils.get(
                #                 message.guild.members, name=memberValue)

                #         if member:
                #             await self.updateUser("kill_time", message.author.id, time.time() + 300, message.guild.id)
                #             sort = random.choice([1, 1, 1, 0, 1, 0, 0, 0, 0])
                #             if sort == 1:
                #                 await message.channel.send(":skull: | **%s**, você não conseguiu matar, seu fraco(a)." %(message.author.mention))
                #                 return

                #             if member.id == client.user.id:
                #                 await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #                 return

                #             if member.id == message.author.id:
                #                 await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode matar você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #                 return

                #             rpgUserKilled = await self.getUser(member.id, message.guild.id)
                #             if rpgUserKilled == None:
                #                 await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                #                 return

                #             if int(rpgUserKilled["health"]) < 1:
                #                 await message.channel.send(":skull: | **%s**, esta pessoa está morta!" %(message.author.mention))
                #                 return

                #             killMessage = await message.channel.send(message.author.mention, embed=discord.Embed(description=":skull: | **%s**, **%s** está tentando te matar, seja mais rápido e desvie o ataque!"%(member.mention, message.author.mention), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #             await killMessage.add_reaction("☠️")

                #             def check(reaction, user):
                #                 return reaction.message.id == killMessage.id and user == member and reaction.emoji == "☠️" and client.user.id != user.id

                #             try:
                #                 reaction, user = await client.wait_for('reaction_add', timeout=3, check=check)
                #             except asyncio.TimeoutError:
                #                 await killMessage.delete()
                #                 if discord.utils.get(message.author.roles, name=roles[100]["name"]) is None:
                #                     await self.updateUser("wanted", message.author.id, 1, message.guild.id)
                #                 await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 4, message.guild.id)
                #                 if not await self.haveItem(next(iter(item for item in itemsList if itemsList[item]['name'] == "Colete"), None), rpgUserKilled):
                #                     await self.updateUser("health", member.id, rpgUserKilled["health"] - 8, message.guild.id)
                #                 else:
                #                     if rpgUserKilled["westcoast"] - 2 < 1:
                #                         if rpgUserKilled["items"] != None and rpgUserKilled["items"] != "":
                #                             myItemList = eval(rpgUserKilled["items"])
                #                             myItemList.remove(11)
                #                             await self.updateUser("westcoast", member.id, 0, message.guild.id)
                #                             await self.updateUser("items", member.id, myItemList, message.guild.id)
                #                     else:
                #                         await self.updateUser("westcoast", member.id, rpgUserKilled["westcoast"] - 2, message.guild.id)
                #                 await self.updateUser("deaths", member.id, rpgUserKilled["deaths"] + 1, message.guild.id)
                #                 await self.updateUser("kills", message.author.id, rpgUser["kills"] + 1, message.guild.id)
                #                 await self.updateLevel(rpgUser, 4, message.channel, message.guild.id)

                #                 await message.channel.send(message.author.mention, embed=discord.Embed(title=":skull: | Você matou %s!"%await self.getMemberUsername(member), colour=0xFFBF00).set_image(url="https://i.ytimg.com/vi/szXf3hvb_wM/maxresdefault.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                #                 return

                #             else:
                #                 await killMessage.delete()
                #                 embed = discord.Embed(title=":skull: | Não foi dessa vez %s!"%await self.getMemberUsername(message.author), description="**%s** foi mais rápido que você e desviou seu ataque."%member.mention, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                #         else:
                #             embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s"%datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                #         await message.channel.send(message.author.mention, embed=embed)

                elif command in ['ban']:
                    async with message.channel.typing():
                        if not 'administrator' in permissions and not 'ban_members' in permissions:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, você não tem permissão para usar esse comando.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text=datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, você não mencionou a pessoa que deseja banir.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text=datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            reason = "Sem motivo." if argsCount <= 2 else argsNotSplited.split(" ", 1)[
                                1]
                            await member.ban(reason=reason)
                            await message.channel.send(message.author.mention, embed=discord.Embed(title=":white_check_mark: | Usuário punido com sucesso!", description="**%s** foi banido com sucesso pelo motivo ``%s``" % (member.mention, reason), colour=0x3CB371).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text=datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, algo deu errado, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text=datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))

                elif command in ['hacker', 'hackear']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if discord.utils.get(message.author.roles, name=roles[101]["name"]) is None:
                            await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um hacker!", description="Você precisa ser um hacker para poder hackear o banco.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 70:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **70** de fome para hackear, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 40 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 20:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **20** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        hackerTime = int(rpgUser["hacker_time"])
                        if hackerTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **10 minutos** para hackear novamente." % (message.author.mention))
                            return

                        sort = random.choice([1, 1, 1, 0, 1, 0, 0, 0, 0])
                        if sort == 1:
                            xpSort = random.randint(0, 1100)

                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + xpSort, message.guild.id)
                            await self.updateUser("wanted", message.author.id, 1, message.guild.id)
                            await self.updateUser("hacker_time", message.author.id, time.time() + 600, message.guild.id)
                            await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 4, message.guild.id)
                            await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                            embed = discord.Embed(title=":money_with_wings: | Você hackeou %s reais do banco central!" % (xpSort), colour=0xFFBF00).set_image(url="https://thumbs.gfycat.com/ReliableHairyLarva-size_restricted.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            await self.updateUser("stuck", message.author.id, 1, message.guild.id)
                            await self.updateUser("stuck_time", message.author.id, time.time() + 86400, message.guild.id)
                            await message.channel.send(":man_police_officer: | **%s**, sua tentativa de hackear falhou e você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)
                            return

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['assaltar', 'roubar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if int(rpgUser["level"]) < 3:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 3** para poder assaltar alguém.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 30:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para assaltar, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        assaultTime = int(rpgUser["assault_time"])
                        if assaultTime > time.time():
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **5 minutos** para assaltar novamente." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa mencionar a pessoa que deseja assaltar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode roubar você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserAssaulted = await self.getUser(member.id, message.guild.id)
                            if rpgUserAssaulted == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if int(rpgUserAssaulted["health"]) < 1:
                                await message.channel.send(":skull: | **%s**, esta pessoa está morta!" % (message.author.mention))
                                return

                            sort = random.choice([1, 1, 1, 0, 1, 0, 0, 0])
                            xpSort = random.randint(
                                0, int(rpgUserAssaulted["xp_points"] / 4))
                            if sort == 1 and xpSort > 0:
                                await self.updateUser("xp_points", member.id, rpgUserAssaulted["xp_points"] - xpSort, message.guild.id)
                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + xpSort, message.guild.id)
                                await self.updateUser("wanted", message.author.id, 1, message.guild.id)
                                await self.updateUser("assault_time", message.author.id, time.time() + 300, message.guild.id)
                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 4, message.guild.id)
                                await self.updateUser("health", member.id, rpgUserAssaulted["health"] - 2, message.guild.id)
                                await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                                embed = discord.Embed(title=":money_mouth: | Você assaltou %s reais de %s!" % (xpSort, await self.getMemberUsername(member)), colour=0xFFBF00).set_image(url="https://s2.glbimg.com/iFS13spD3Iq4yW9HGerK_F4bzj4=/300x200/i.glbimg.com/og/ig/infoglobo1/f/original/2017/04/29/assalto.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            else:
                                await self.updateUser("stuck", message.author.id, 1, message.guild.id)
                                await self.updateUser("stuck_time", message.author.id, time.time() + 86400, message.guild.id)
                                await message.channel.send(":man_police_officer: | **%s**, seu assalto falhou e você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                                return
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['beijar', 'beijo']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if int(rpgUser["level"]) < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 2** para poder beijar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa mencionar a pessoa que deseja beijar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode beijar você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserToKiss = await self.getUser(member.id, message.guild.id)
                            if rpgUserToKiss == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if rpgUser["married_id"] != "0" and rpgUser["married_id"] != "" and rpgUser["married_id"] != None and member.id != int(rpgUser["married_id"]):
                                marriedMember = discord.utils.get(
                                    message.guild.members, id=int(rpgUser["married_id"]))
                                if marriedMember != None:
                                    await message.channel.send(embed=discord.Embed(description="Hey **%s**, corre aqui! Sua alma gêmea está te traindo!" % marriedMember.mention, colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    # return

                            embed = discord.Embed(title=":kiss: | Hey %s, %s quer te dar um beijo!" % (await self.getMemberUsername(member), await self.getMemberUsername(message.author)), description="**%s**, aceita beijar **%s**?" % (await self.getMemberUsername(member), await self.getMemberUsername(message.author)), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            kissMessage = await message.channel.send(embed=embed)
                            await kissMessage.add_reaction("💋")

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == kissMessage.id and user == member and reaction.emoji == "💋" and client.user.id != user.id)
                            except asyncio.TimeoutError:
                                await kissMessage.delete()
                            else:
                                if rpgUserToKiss["married_id"] != "0" and rpgUserToKiss["married_id"] != "" and rpgUserToKiss["married_id"] != None and member.id != int(rpgUserToKiss["married_id"]):
                                    marriedMember = discord.utils.get(
                                        message.guild.members, id=int(rpgUserToKiss["married_id"]))
                                    if marriedMember != None:
                                        await message.channel.send(embed=discord.Embed(description="Hey **%s**, corre aqui! Sua alma gêmea está te traindo!" % marriedMember.mention, colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                        # return

                                await kissMessage.delete()
                                embed = discord.Embed(title=":kiss: | Você beijou %s!" % await self.getMemberUsername(member), colour=0xFFBF00).set_image(url="https://media1.tenor.com/images/6f4bf3f4b957c8a3d560bcf2f62c2577/tenor.gif?itemid=5072833").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['casar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if int(rpgUser["level"]) < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 2** para poder se casar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 30:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **30** de fome para casar, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa mencionar a pessoa que deseja casar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if rpgUser["married_id"] != "0" and rpgUser["married_id"] != "" and rpgUser["married_id"] != None:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa se divorciar para casar novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode casar com você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserMarried = await self.getUser(member.id, message.guild.id)
                            if rpgUserMarried == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if rpgUserMarried["married_id"] != "0" and rpgUserMarried["married_id"] != "" and rpgUserMarried["married_id"] != None:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Esta pessoa já está casada.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":heart: | %s pediu %s em casamento!" % (await self.getMemberUsername(message.author), await self.getMemberUsername(member)), description="**%s**, aceita se casar com **%s**?" % (await self.getMemberUsername(member), await self.getMemberUsername(message.author)), colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            marriedMessage = await message.channel.send(embed=embed)
                            await marriedMessage.add_reaction("❤️")

                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: reaction.message.id == marriedMessage.id and user == member and reaction.emoji == "❤️" and client.user.id != user.id)
                            except asyncio.TimeoutError:
                                await marriedMessage.delete()
                            else:
                                await marriedMessage.delete()
                                # await self.updateUser("married", member.id, "%s#%s"%(await self.getMemberUsername(message.author), message.author.discriminator), message.guild.id)
                                # await self.updateUser("married", message.author.id, "%s#%s"%(await self.getMemberUsername(member), member.discriminator), message.guild.id)
                                await self.updateUser("married_id", member.id, message.author.id, message.guild.id)
                                await self.updateUser("married_id", message.author.id, member.id, message.guild.id)
                                await self.updateLevel(rpgUser, 3 if rpgUser["level"] < 8 else 2, message.channel, message.guild.id)

                                embed = discord.Embed(title=":couple_with_heart_woman_man: | Você se casou com %s!" % await self.getMemberUsername(member), colour=0xFFBF00).set_image(url="https://img.ibxk.com.br/2017/09/14/casamento-14201449283000.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['divorciar', 'divorcio']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        if rpgUser["married_id"] == "0" or rpgUser["married_id"] == "" or rpgUser["married_id"] == None:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa estar casado para se divorciar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        rpgUserDivorced = await self.getUser(rpgUser["married_id"], message.guild.id)
                        if rpgUserDivorced == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        # await self.updateUser("married", rpgUser["married_id"], "", message.guild.id)
                        # await self.updateUser("married", message.author.id, "", message.guild.id)
                        await self.updateUser("married_id", rpgUser["married_id"], 0, message.guild.id)
                        await self.updateUser("married_id", message.author.id, 0, message.guild.id)
                        await self.updateLevel(rpgUser, 1, message.channel, message.guild.id)

                        member = discord.utils.get(
                            message.guild.members, id=int(rpgUser["married_id"]))
                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            embed = discord.Embed(title=":broken_heart: | %s divorciou-se de %s!" % (await self.getMemberUsername(message.author), await self.getMemberUsername(member)), colour=0x1C1C1C).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_image(url="").set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await message.channel.send(message.author.mention, embed=embed)

                elif command in ['trabalhar']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if int(rpgUser["hunger"]) <= 50:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **50** de fome para trabalhar, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 35 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 10:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **10** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        job = args[0] if argsCount > 0 else "ajuda"
                        addTimeLevel = 10 if rpgUser["level"] < 5 else 25 if rpgUser["level"] >= 5 and rpgUser[
                            "level"] < 10 else 35 if rpgUser["level"] > 10 and rpgUser["level"] < 20 else 50
                        jobTime = int(rpgUser["job_time"])
                        if jobTime > time.time() and not job in ["ajuda", "help", "trabalhos"]:
                            await message.channel.send(":no_entry: | **%s**, você deve esperar **%s segundos** para trabalhar novamente." % (message.author.mention, 40 + addTimeLevel))
                            return

                        if job in ["ajuda", "help", "trabalhos"]:
                            title = "Olá %s, confira os trabalhos disponíveis abaixo:" % await self.getMemberUsername(message.author)
                            result = "- **cadeia** - Trabalhe na cadeia se você não possui reais para pagar sua fiança (Recompensa: **5 à 120 reais** e requer estar **preso**).\n"
                            result += "- **bombeiro** - Trabalhe como bombeiro e salve as vidas da cidade (Recompensa: **300 à 2500 reais**, requer **nível 8 e cargo de Bombeiro**).\n"
                            result += "- **medico** - Trabalhe como médico (Recompensa: **300 à 2100 reais**, requer **nível 6 e cargo de Médico**).\n"
                            result += "- **carteiro** - Trabalhe como carteiro nas ruas da cidade (Recompensa: **10 à 120 reais**).\n"
                            result += "- **lixeiro** - Trabalhe como lixeiro nas ruas da cidade (Recompensa: **10 à 80 reais**).\n"
                            result += "- **cozinheiro** - Trabalhe como cozinheiro (Recompensa: **60 à 470 reais**, requer **nível 4**).\n"
                            result += "- **enfermeiro** - Trabalhe como enfermeiro (Recompensa: **50 à 400 reais**, requer **nível 2**).\n"
                            result += "- **advogado** - Trabalhe como advogado (Recompensa: **100 à 1000 reais**, requer **nível 10 e cargo de Advogado**).\n"
                            result += "- **policia** - Trabalhe como policial e mantenha a cidade em ordem (Recompensa: **300 à 5000 reais**, requer **nível 13 e cargo de Policial**).\n"
                            result += "- **mecanico** - Trabalhe como mecânico (Recompensa: **60 à 450 reais**, requer **nível 4**).\n\n"

                            await message.channel.send(message.author.mention, embed=discord.Embed(title=title, description=result, colour=0xFFBF00).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Roleplay BOT desenvolvido por raddis#4444.").set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)).set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/rpg-1691444-1441510.png"))
                            await message.channel.send(":hammer_pick: | Para trabalhar digite **%strabalhar __profissão__**" % self.prefix)
                        else:
                            if rpgUser["stuck"] == "1" and not job == "cadeia":
                                await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                                return

                            job = job.lower().strip()
                            if job == "bombeiro":
                                if int(rpgUser["level"]) < 8:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 8** para trabalhar como bombeiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if discord.utils.get(message.author.roles, name=roles[102]["name"]) is None:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um bombeiro!", description="Você precisa ser um bombeiro para poder trabalhar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1])
                                if jobSort == 1:
                                    giveSort = random.choice(
                                        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0])
                                    if giveSort == 1:
                                        sort = random.randint(300, 2500)
                                    else:
                                        sort = random.randint(300, 900)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":firefighter: | Você trabalhou como bombeiro e ganhou %s reais! Vários incêndios foram apagados e vidas foram salvas!" % sort, colour=0xA52A2A).set_image(url="https://cdn.discordapp.com/attachments/479367540464812072/780884523792859136/ezgif.com-gif-maker.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":firefighter: | Você não salvou nenhuma vida e por isso não faturou nenhuma real!", colour=0xA52A2A).set_image(url="https://cdn.mensagenscomamor.com/content/images/m000501126.gif?v=1").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                            elif job == "medico" or job == "médico":
                                if int(rpgUser["level"]) < 6:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 6** para trabalhar como médico.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if discord.utils.get(message.author.roles, name=roles[104]["name"]) is None:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um médico!", description="Você precisa ser um médico para poder trabalhar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1])
                                if jobSort == 1:
                                    giveSort = random.choice(
                                        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0])
                                    if giveSort == 1:
                                        sort = random.randint(300, 2100)
                                    else:
                                        sort = random.randint(300, 600)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":ambulance: | Você trabalhou como médico e ganhou %s reais! Várias vidas foram salvas." % sort, colour=0xA52A2A).set_image(url="https://cdn.discordapp.com/attachments/479367540464812072/780965223880327198/ezgif-7-dee919d4ff49.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":ambulance: | Você não teve sucesso em seu trabalho e por isso não faturou nenhuma reai!", colour=0xA52A2A).set_image(url="https://media0.giphy.com/media/CTN6XBCXqtUjK/giphy.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                            elif job == "cadeia":
                                if rpgUser["stuck"] == "0":
                                    await message.channel.send(":no_entry: | **%s**, você não está preso para trabalhar na cadeia." % (message.author.mention))
                                    return

                                sort = random.randint(5, 120)
                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                embed = discord.Embed(title=":pick: | Você trabalhou na cadeia e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://img.gta5-mods.com/q95/images/prison-break-build-a-mission/0bff97-GTAV-Heists-Update-29.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                            elif job == "lixeiro":
                                sort = random.randint(10, 80)
                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                embed = discord.Embed(title=":adult: | Você coletou todo o lixo com sucesso e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://cdn.discordapp.com/attachments/479367540464812072/780963783236911144/ezgif-7-5e68d5337c48.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                            elif job == "carteiro":
                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0])
                                if jobSort == 1:
                                    sort = random.randint(10, 120)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":envelope_with_arrow: | Você entregou todas as correspondências com sucesso e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://img.gta5-mods.com/q75/images/brazilian-postal-service-pack-correios/994d43-GTA5%202016-03-24%2021-53-01-61.png").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":envelope_with_arrow: | Parece que você não está afim de trabalhar hoje né? Infelizmente você não faturou nenhum real em seu trabalho!", colour=0x1C1C1C).set_image(url="https://thumbs.gfycat.com/HighFondHedgehog-max-1mb.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)

                            elif job == "cozinheiro":
                                if int(rpgUser["level"]) < 4:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 4** para trabalhar como cozinheiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0])
                                if jobSort == 1:
                                    sort = random.randint(60, 470)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":cook: | Você trabalhou como cozinheiro e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://i.gifer.com/3Cll.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":cook: | Você não tratou o cliente bem, e por isso não faturou nenhum real!", colour=0x1C1C1C).set_image(url="https://media1.tenor.com/images/141896f669d869020cabfbd99712639f/tenor.gif?itemid=17458708").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)

                            elif job == "enfermeiro":
                                if int(rpgUser["level"]) < 2:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 2** para trabalhar como enfermeiro.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0])
                                if jobSort == 1:
                                    sort = random.randint(50, 400)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    embed = discord.Embed(title=":health_worker: | Você trabalhou como enfermeiro e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://i.imgur.com/GiPiOgi.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":health_worker: | Parece que você não teve sucesso em seu trabalho como enfermeiro...", colour=0x1C1C1C).set_image(url="https://i.ytimg.com/vi/9zv0PI9Az7w/maxresdefault.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)

                            elif job == "mecanico" or job == "mecânico":
                                if int(rpgUser["level"]) < 4:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 4** para trabalhar como mecânico.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0])
                                if jobSort == 1:
                                    sort = random.randint(60, 450)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":mechanic: | Você trabalhou como mecânico e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://1.bp.blogspot.com/-ZxbYyxnnH2c/WDTtT74YvKI/AAAAAAAAk6U/F2wPm_G7V0I5WwumeOg4WMFnSLAoOIv-wCLcB/s1600/1.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":mechanic: | Você bateu o carro do cliente, e por isso não faturou nenhum real no seu trabalho!", colour=0x1C1C1C).set_image(url="https://i.gifer.com/8MNY.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)

                            elif job == "advogado":
                                if int(rpgUser["level"]) < 10:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 10** para trabalhar como advogado.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if discord.utils.get(message.author.roles, name=roles[103]["name"]) is None:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um advogado!", description="Você precisa ser um advogado para poder trabalhar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0])
                                if jobSort == 1:
                                    sort = random.randint(100, 1000)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":person_in_tuxedo: | Você trabalhou como advogado e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://media1.tenor.com/images/b9e78a2e91f98643c1f1fc8a0edec86e/tenor.gif?itemid=17452438").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":person_in_tuxedo: | Você falhou em resolver o caso, e por isso não faturou nenhum real!", colour=0x1C1C1C).set_image(url="https://media1.tenor.com/images/e3f1098df2ad9fa8ccf2b1ddf19bd038/tenor.gif?itemid=17451100").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)

                            elif job == "policia" or job == "polícia" or job == "policial":
                                if int(rpgUser["level"]) < 13:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 13** para trabalhar como policial.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if discord.utils.get(message.author.roles, name=roles[100]["name"]) is None:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um policial!", description="Você precisa ser um policial para poder trabalhar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                jobSort = random.choice(
                                    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1])
                                if jobSort == 1:
                                    giveSort = random.choice(
                                        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1])
                                    if giveSort == 1:
                                        sort = random.randint(300, 5000)
                                    else:
                                        sort = random.randint(300, 2100)
                                    await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + sort, message.guild.id)
                                    await self.updateLevel(rpgUser, 4 if rpgUser["level"] < 5 else 3 if rpgUser["level"] < 10 and rpgUser["level"] > 5 else 2, message.channel, message.guild.id)
                                    await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                                    embed = discord.Embed(title=":police_officer: | Você trabalhou como policial e ganhou %s reais." % sort, colour=0x1C1C1C).set_image(url="https://media0.giphy.com/media/JO4aaDqEX4UGsHQNdb/200.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                else:
                                    embed = discord.Embed(title=":police_officer: | Você capotou a viatura da polícia e não faturou nenhum real!", colour=0x1C1C1C).set_image(url="https://1.bp.blogspot.com/-H3xLduzR_W8/XS9RjYOmMPI/AAAAAAAABlQ/87wiHe9pmqo3naT_p005HfgPu4bGNRSZgCLcBGAs/s1600/CARRO%2BEXPLODINDO.gif").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                                    await self.updateUser("health", message.author.id, rpgUser["health"] - 3, message.guild.id)
                            else:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="O setor de trabalho informado não existe.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            await self.updateUser("job_time", message.author.id, time.time() + 40 + addTimeLevel, message.guild.id)
                            await message.channel.send(message.author.mention, embed=embed)

                elif command in ['prender']:
                    async with message.channel.typing():
                        if discord.utils.get(message.author.roles, name=roles[100]["name"]) is None:
                            await message.channel.send(message.author.mention, embed=discord.Embed(title="Você não é um policial!", description="Você precisa ser um policial para poder prender alguém.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if int(rpgUser["level"]) < 2:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa de **nível 2** para poder prender alguém.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if rpgUser["stuck"] == "1":
                            await message.channel.send(":man_police_officer: | **%s**, você está preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (message.author.mention, datetime.utcfromtimestamp(int(rpgUser["stuck_time"])).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                            return

                        if int(rpgUser["hunger"]) <= 15:
                            await message.channel.send(":fork_knife_plate: | **%s**, você precisa ter mais de **15** de fome para prender, use **%scomer** para se alimentar!" % (message.author.mention, self.prefix))
                            return

                        if int(rpgUser["health"]) <= 30 and random.choice([0, 0, 0, 1, 1, 0]) == 1:
                            await message.channel.send(":anatomical_heart: | Hey **%s**! Você está ficando com pouca vida e em breve não conseguirá mais usar este comando, alimente-se para recuperá-la!" % (message.author.mention))

                        if int(rpgUser["health"]) <= 15:
                            await message.channel.send(":broken_heart: | **%s**, você precisa ter mais de **15** de vida para usar este comando, alimente-se para recuperar." % (message.author.mention))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa informar quem você deseja prender.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        memberValue = args[0]
                        if len(message.mentions) > 0:
                            member = discord.utils.get(
                                message.guild.members, id=message.mentions[0].id)
                        elif memberValue.isdigit():
                            member = discord.utils.get(
                                client.get_all_members(), id=int(memberValue))
                        else:
                            member = discord.utils.get(
                                message.guild.members, name=memberValue)

                        if member:
                            if member.bot:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == client.user.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            if member.id == message.author.id:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode prender você mesmo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                return

                            rpgUserStuck = await self.getUser(member.id, message.guild.id)
                            if rpgUserStuck == None:
                                await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                return

                            if rpgUserStuck["wanted"] == "0":
                                await message.channel.send(":no_entry: | **%s**, esta pessoa não está sendo procurada pela polícia para prendê-la." % message.author.mention)
                                return

                            if rpgUserStuck["stuck"] == "1":
                                await message.channel.send(":no_entry: | **Opa %s!** Esta pessoa já está presa!" % message.author.mention)
                                return

                            if discord.utils.get(member.roles, name=roles[100]["name"]) is not None:
                                await message.channel.send(":no_entry: | **Opa %s!** Esta pessoa é policial e não pode ser presa!" % message.author.mention)
                                return

                            if int(rpgUserStuck["health"]) < 1:
                                await message.channel.send(":skull: | **%s**, esta pessoa está morta!" % (message.author.mention))
                                return

                            await self.updateUser("stuck", member.id, 1, message.guild.id)
                            await self.updateUser("stuck_time", member.id, time.time() + 86400, message.guild.id)
                            await self.updateUser("arrested", message.author.id, rpgUser["arrested"] + 1, message.guild.id)
                            await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 3, message.guild.id)
                            await self.updateUser("health", member.id, rpgUserStuck["health"] - 3, message.guild.id)
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] + 500, message.guild.id)
                            await self.updateLevel(rpgUser, 3, message.channel, message.guild.id)

                            embed = discord.Embed(title=":man_police_officer: | %s agora está preso e %s ganhou 500 reais por seu trabalho!" % (await self.getMemberUsername(member), await self.getMemberUsername(message.author)), colour=0x1C1C1C).set_image(url="https://i.ytimg.com/vi/s4sPGukBQBw/maxresdefault.jpg").set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))
                            await message.channel.send(":man_police_officer: | **%s**, você foi preso até **%s**! Digite **%sfiança** para sair da cadeia!" % (member.mention, datetime.utcfromtimestamp(time.time() + 86400).strftime('%d/%m/%Y %H:%M:%S'), self.prefix))
                        else:
                            embed = discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author))

                        await message.channel.send(message.author.mention, embed=embed)

                elif command in ['fiança']:
                    async with message.channel.typing():
                        rpgUser = await self.getUser(message.author.id, message.guild.id)
                        if rpgUser == None:
                            await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                            return

                        if 700 > int(rpgUser["xp_points"]):
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você precisa ter **700 reais** na carteira para pagar fiança, você possui somente **%s**, digite **%strabalhar cadeia** para conseguir dinheiro." % (rpgUser["xp_points"], self.prefix), colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount > 0:
                            memberValue = args[0]
                            if len(message.mentions) > 0:
                                member = discord.utils.get(
                                    message.guild.members, id=message.mentions[0].id)
                            elif memberValue.isdigit():
                                member = discord.utils.get(
                                    client.get_all_members(), id=int(memberValue))
                            else:
                                member = discord.utils.get(
                                    message.guild.members, name=memberValue)

                            if member:
                                if member.bot:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando com BOT's.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if member.id == client.user.id:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode usar este comando comigo.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                if member.id == message.author.id:
                                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não pode pagar sua própria fiança.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                                    return

                                rpgUserStuck = await self.getUser(member.id, message.guild.id)
                                if rpgUserStuck == None:
                                    await message.channel.send("**Oops!** Ocorreu um erro, contate o proprietário do bot.")
                                    return

                                if rpgUserStuck["stuck"] == "0":
                                    await message.channel.send(":no_entry: | **%s**, esta pessoa não está presa!" % message.author.mention)
                                    return

                                await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - 700, message.guild.id)
                                await self.updateUser("stuck", member.id, 0, message.guild.id)
                                await self.updateUser("stuck_time", member.id, 0, message.guild.id)
                                await self.updateUser("wanted", member.id, 0, message.guild.id)
                                await self.updateUser("hunger", message.author.id, rpgUser["hunger"] - 2, message.guild.id)
                                await self.updateUser("stuck_time", member.id, 0, message.guild.id)
                                await self.updateLevel(rpgUser, 2, message.channel, message.guild.id)

                                await message.channel.send(":man_police_officer: | **%s**, você pagou a fiança de **%s** por **700 reais** e agora ele está livre!" % (message.author.mention, member.mention))
                            else:
                                await message.channel.send(message.author.mention, embed=discord.Embed(description="Não consegui encontrar quem você mencionou, tente novamente.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                        else:
                            if rpgUser["stuck"] == "0":
                                await message.channel.send(":no_entry: | **%s**, você não está preso!" % message.author.mention)
                                return

                            await message.channel.send(":man_police_officer: | **%s**, você pagou **700 reais** e agora você está livre!" % (message.author.mention))
                            await self.updateUser("xp_points", message.author.id, rpgUser["xp_points"] - 700, message.guild.id)
                            await self.updateUser("stuck", message.author.id, 0, message.guild.id)
                            await self.updateUser("stuck_time", message.author.id, 0, message.guild.id)
                            await self.updateUser("wanted", message.author.id, 0, message.guild.id)
                            await self.updateUser("stuck_time", message.author.id, 0, message.guild.id)
                            await self.updateLevel(rpgUser, 2, message.channel, message.guild.id)

                elif command in ['psay']:
                    async with message.channel.typing():
                        if not message.author.id in ownersId:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Você não tem permissão para isso.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        if argsCount < 1:
                            await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, você não digitou a mensagem que deseja enviar.", colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
                            return

                        await message.delete()
                        await message.channel.send(argsNotSplited)

                else:
                    await message.channel.send(message.author.mention, embed=discord.Embed(description="Oops, desculpe **%s**, não consegui encontrar este comando, você o digitou corretamente?" % await self.getMemberUsername(message.author), colour=0xFF0000).set_footer(icon_url="https://cdn0.iconfinder.com/data/icons/weaponry-ultra-colour-collection/60/Weaponary_-_Ultra_Color_-_037_-_Sword_and_Shield-512.png", text="Hoje às %s" % datetime.now().strftime("%H:%M:%S")).set_author(icon_url=message.author.avatar_url, name=await self.getMemberUsername(message.author)))
        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            await self.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


os.system("title Discord RPG Bot by Raddis")
intents = discord.Intents.all()
client = Bot(intents=intents)
client.run(config["token"], reconnect=True)
