import discord
from discord import Colour, Member, Embed
from discord.client import Client
from discord.utils import get
from asyncio import sleep
from discord.ext.commands import (Bot, Cog, CommandError, Context,
                                MissingPermissions, command, has_permissions)
from os import getenv
from discord.ui import Button, View
import math
intents=discord.Intents.all()

class Bot(discord.Client):
    async def on_ready(self):
        self.recruiting = {}
        self.doui = 931790877096042567
        self.rank = 931805598419402773
        print('Ready fuck')

    async def on_member_join(self, member):
        guild = member.guild
        ch = self.get_channel(931599808643346483)
        count_user = sum(1 for member in guild.members if not member.bot)
        embed = Embed(
            title="ようこそApexJPへ！",
            description=f"{member.name}がApexJPに参加しました！",
            color=Colour.blue(),
        )
        embed.add_field(
            name="ルールの確認",
            value="<#931602033209925663>でルールを確認しよう！",
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"{count_user}人目のユーザーです！")
        await ch.send(embed=embed)

    async def on_member_remove(self,member):
        guild = member.guild
        ch = self.get_channel(931599808643346483)
        count_user = sum(1 for member in guild.members if not member.bot)
        embed = Embed(
            title="メンバーが去りました",
            description=f"{member.name}がサーバーを抜けました。",
            color=Colour.red(),
        )
        embed.add_field(
            name="さようなら",
            value="またのお越しをお待ちしています。",
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"サーバーの人数が{count_user}人に減りました...")
        await ch.send(embed=embed)

    async def fetch_rank(self,member):
        pass

    async def rank_check(self,member):
        pass

    async def remove_reaction(self,payload):
        message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        member = await self.get_guild(payload.guild_id).fetch_member(payload.user_id)
        await message.remove_reaction("✋", member)

    async def on_raw_reaction_add(self,payload):
        self.ranks = {"predetor":1,"master":1,"diamond":2,"platinum":3,"gold":4,"silver":5,"blonz":5}
        print(payload.emoji.name)
        guild= self.get_guild(931599635481526332)
        user = guild.get_member(payload.user_id)
        if payload.message_id == self.doui:
            role = guild.get_role(931600625152696501)
            await user.add_roles(role) 
        if payload.message_id == self.rank:
            guild= self.get_guild(931599635481526332)
            predetor = guild.get_role(931620349043433522)
            master = guild.get_role(931620277882859632)
            diamond = guild.get_role(931620231602917437)
            platinum = guild.get_role(931620179979419719)
            gold = guild.get_role(931620122043515010)
            silver = guild.get_role(931620007501254688)
            blonz = guild.get_role(931620154624847932)

            user = guild.get_member(payload.user_id)
            if payload.emoji.name == "predetor":
                await user.add_roles(predetor)

            if payload.emoji.name == "mastar":
                await user.add_roles(master)

            if payload.emoji.name == "diamond":
                await user.add_roles(diamond)

            if payload.emoji.name == "platinum":
                await user.add_roles(platinum)

            if payload.emoji.name == "gold":
                await user.add_roles(gold)

            if payload.emoji.name == "silver":
                await user.add_roles(silver)

            if payload.emoji.name == "bronz":
                await user.add_roles(blonz)

        if payload.user_id == self.user.id:
            print("b")
            return
        if payload.message_id in self.recruiting:
            print("sanka")
            recruit = self.recruiting[payload.message_id]
            

            for roles in user.roles:
                print(roles.name)
                try:
                    self.us = self.ranks[roles.name]
                except KeyError:
                    pass
            ch = self.get_channel(931603818456699060)
            nowrank = self.recruiting[payload.message_id]["rank"]
            if nowrank != self.us:
                self.recruiting[payload.message_id]["rank"] = self.us
            if math.fabs(nowrank - self.us) >= 2:
                await ch.send("あなたは適正ランクまで達していません。",delete_after=10)
                return
            if payload.user_id == recruit['author']:
                await self.remove_reaction(payload)
                return
            if recruit['player'] >= len(recruit['players']):
                recruit['players'].append(f'<@{payload.user_id}>')

    async def on_raw_reaction_remove(self,payload):
        if payload.message_id in self.recruiting:
            recruit = self.recruiting[payload.message_id]
            if payload.user_id == recruit['author']:
                await self.get_channel(payload.channel_id).send(f'<@{payload.user_id}> あなたは募集した人なので既に参加しています。', delete_after=3)
            recruit['players'].remove(f'<@{payload.user_id}>')
        if payload.message_id == self.doui:
            guild= self.get_guild(931599635481526332)
            role = guild.get_role(931600625152696501)
            user = guild.get_member(payload.user_id)
            await user.remove_roles(role)
        if payload.message_id == self.rank:
            guild= self.get_guild(931599635481526332)
            predetor = guild.get_role(931620349043433522)
            master = guild.get_role(931620277882859632)
            diamond = guild.get_role(931620231602917437)
            platinum = guild.get_role(931620179979419719)
            gold = guild.get_role(931620122043515010)
            silver = guild.get_role(931620007501254688)
            blonz = guild.get_role(931620154624847932)

            user = guild.get_member(payload.user_id)
            if payload.emoji.name == "predetor":
                await user.remove_roles(predetor)

            if payload.emoji.name == "mastar":
                await user.remove_roles(master)

            if payload.emoji.name == "diamond":
                await user.remove_roles(diamond)

            if payload.emoji.name == "platinum":
                await user.remove_roles(platinum)

            if payload.emoji.name == "gold":
                await user.remove_roles(gold)

            if payload.emoji.name == "silver":
                await user.remove_roles(silver)

            if payload.emoji.name == "bronz":
                await user.remove_roles(blonz)

    async def on_message(self,message):
        prefix = "a."
        if message.author.bot:
            return
        if message.content.startswith(prefix):
            command = message.content[len(prefix):]
            arg = message.content.split(' ')[1:]
            if command == "get_rank_role":
                if message.author.id == 916458388106383370:
                    embed = Embed(title = "ルールに同意できる方は、✋を押してください")
                    send_msg = await message.channel.send(embed = embed)
                    await send_msg.add_reaction("✋")

            if command == "select_rank":
                if message.author.id == 916458388106383370:
                    p = "<:predetor:931622099632668683>"
                    m = "<:mastar:931622132776042657>"
                    d = "<:diamond:931622162958254180>"
                    pl = "<:platinum:931622182994444348>"
                    g = "<:gold:931622199301931018>"
                    s = "<:silver:931622206822305823>"  
                    b = "<:bronz:931622213398974524>"
                    embed = Embed(title = f"自分のランクのリアクションを押してください。",description="\nプレデター:<:predetor:931622099632668683>\nマスター:<:mastar:931622132776042657>\nダイヤモンド:<:diamond:931622162958254180>\nプラチナ:<:platinum:931622182994444348>\nゴールド:<:gold:931622199301931018>\nシルバー:<:silver:931622206822305823>\nブロンズ:<:bronz:931622213398974524>")
                    send_msg = await message.channel.send(embed = embed) 
                    await send_msg.add_reaction(p)
                    await send_msg.add_reaction(m)
                    await send_msg.add_reaction(d)
                    await send_msg.add_reaction(pl)
                    await send_msg.add_reaction(g)
                    await send_msg.add_reaction(s)
                    await send_msg.add_reaction(b)

            if command.startswith("r"):
                self.ranks = {"predetor":1,"master":1,"diamond":2,"platinum":3,"gold":4,"silver":5,"blonz":5}
                if message.channel.id != 931603818456699060:
                    await message.delete()
                    await message.channel.send("<#931603818456699060> で、このコマンドを実行してください。", delete_after=10)
                    return
                if (arg[0] == "1" or arg[0] == "2") and not len(arg) <= 1:
                    if arg[1] == "r" or arg[1] == "c":
                        if arg[1] == "r":
                            mode = "rank"
                        else:
                            mode = "casual"
                        await message.delete()

                        for roles in message.author.roles:
                            print(roles.name)
                            try:
                                self.us = self.ranks[roles.name]
                                self.rank_centar = roles.name
                            except KeyError:
                                pass
                        embed = discord.Embed(title=f"募集内容",colour = discord.Colour.blurple())
                        embed.add_field(name="募集者",value=f"<@{message.author.id}>",inline=False)
                        embed.add_field(name="ゲームモード",value=mode,inline=False)
                        embed.add_field(name="募集人数",value='1/{}'.format(int(arg[0])+1),inline=False)
                        embed.add_field(name="メンバー",value=f"<@{message.author.id}>",inline=False)
                        embed.add_field(name="基準ランク",value=f"{self.rank_centar}",inline=False)
                        send_msg = await message.channel.send(embed=embed)
                        self.recruiting[send_msg.id] = {}
                        self.recruiting[send_msg.id]['message'] = send_msg
                        self.recruiting[send_msg.id]['author'] = f'<@{message.author.id}>'
                        self.recruiting[send_msg.id]['player'] = int(arg[0])+1
                        self.recruiting[send_msg.id]['players'] = []
                        self.recruiting[send_msg.id]['rank'] = self.us
                        self.recruiting[send_msg.id]['players'].append(f'<@{message.author.id}>')
                        await send_msg.add_reaction("✋")
                        recruit = self.recruiting[send_msg.id]
                        await sleep(1)
                        while not recruit['player'] == len(recruit['players']):
                            embed = discord.Embed(title=f"募集内容",colour = discord.Colour.blurple())
                            embed.add_field(name="募集者",value=recruit['author'],inline=False)
                            embed.add_field(name="ゲームモード",value=mode,inline=False)
                            embed.add_field(name="募集人数",value='{}/{}'.format(len(recruit['players']), recruit['player']),inline=False)
                            embed.add_field(name="メンバー",value=','.join(recruit['players']),inline=False)
                            embed.add_field(name="基準ランク",value=f"{self.rank_centar}",inline=False)
                            await send_msg.edit(content=None,embed=embed)
                            await sleep(1)
                        embed = discord.Embed(title=f"募集完了",colour=discord.Colour.blurple())
                        embed.add_field(name="募集者", value=recruit['author'],inline=False)
                        embed.add_field(name="ゲームモード", value=mode,inline=False)
                        embed.add_field(name="メンバー", value=','.join(recruit['players']),inline=False)
                        embed.add_field(name="基準ランク",value=f"{self.rank_centar}",inline=False)
                        channel = await message.guild.create_voice_channel(f"{message.author.name}-チャンネル",category=discord.utils.get(message.guild.categories, id=931632504811683890))
                        link = await channel.create_invite()
                        button = Button(label="🔊チャンネルに参加", url=link.url)
                        view = View()
                        view.add_item(button)
                        await send_msg.edit(content=None,embed=embed,view=view)
                    else:
                        await message.channel.send('ランクの場合は \"r\" \nカジュアルの場合は \"c\"\n入力してください。')
                else:
                    await message.channel.send("募集最大人数がオーバーしているかモードの選択がされていません。")

client = Bot(intents = intents)
client.run(getenv('token'))
