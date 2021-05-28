import discord, asyncio

from core.database import Servers
from core.embeds import Embeds
from core.files import Data

commands = discord.ext.commands

class BumpSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Data("config").yaml_read()
        self.settings = Data("settings").json_read()
        global setting_up 
        setting_up = []
    
    @commands.Cog.listener('on_guild_remove')
    async def remove_guild(self, guild):
        Servers(guild.id).delete()
    
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(lambda ctx: ctx.guild not in setting_up)
    @commands.command()
    async def setup(self, ctx):
        guild = ctx.guild
        prefix = Servers(guild.id).getPrefix() if Servers(guild.id).hasPrefix else self.config["prefix"]

        if Servers(guild.id).get():
            return await ctx.send(embed=Embeds(f"Der Server ist schon aufgesetzt benutze `{prefix}delete` um das setup erneut zu starten!").error())

        embed = discord.Embed(
            title="🔄 Setting Up...",
            color=discord.Color.green()
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url_as(static_format="png"))

        embed.description = "Gebe deine Server Beschreibung ein sie muss zwischen 10-2408 Zeichen hab.!"
        await ctx.send(embed=embed)
        try:
            description = (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content
            if len(description) > 2048:
                return await ctx.send(embed=Embeds("Setup abgebrochen deine Beschreibung ist zu lang!").error())
            elif len(description) < 10:
                return await ctx.send(embed=Embeds("Setup abgebrochen deine Beschreibung ist zu kurz!").error())
        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup abgebrochen, Zeit zuende!").error())

        embed.description = "Gebe den Channel an indem der Invite sein soll!"
        await ctx.send(embed=embed)
        try:
            invite = await commands.TextChannelConverter().convert(ctx, (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content)
            
            if not invite.permissions_for(ctx.me).create_instant_invite:
                return await ctx.send(embed=Embeds("Setup abgebrochen ich habe keine Permissions einen Invite zu erstellen.!").error())

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup abgebrochen!").error())
        except commands.ChannelNotFound:
            return await ctx.send(embed=Embeds("Setup abgebrochen, channel wurde nicht gefunden!").error())
        
        embed.description = "Gebe den Channel an wo die Bumps gesendet werden sollen, der Bot brauch Manage Webhooks permissions.!"
        await ctx.send(embed=embed)
        try:
            listing = await commands.TextChannelConverter().convert(ctx, (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content)
            
            if not listing.permissions_for(ctx.me).manage_webhooks:
                return await ctx.send(embed=Embeds("Setup abgebrochen mir fehlt die Permission Manage Webhooks!").error())

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup abgebrochen, Zeit zuende!").error())
        except commands.ChannelNotFound:
            return await ctx.send(embed=Embeds("Setup abgebrochen, Channel nicht gefunden!").error())
        
        embed.description = "Gebe eine Farbe für deinen Bump an: `HEX` !"
        await ctx.send(embed=embed)
        try:
            color = int((await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content.replace("#", ""), 16)

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup abgebrochen, Zeit zuende!").error())
        except ValueError:
            return await ctx.send(embed=Embeds("Setup abgebrochen, die Farbe gibt es nicht!").error())

        webhook = await listing.create_webhook(name=self.config['bot_name'])

        Servers(ctx.guild.id).add(webhook=webhook.id, invite=invite.id, color=color, description=description, icon_url=str(ctx.guild.icon_url_as(static_format="png")), server_name=ctx.guild.name)

        return await ctx.send(embed=discord.Embed(
            title="👌 Setup Beendet",
            description="Dein Server wurde in die Datenbenk eingetragen.",
            color=discord.Color.green()
        ))

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(lambda ctx: ctx.guild not in setting_up)
    @commands.command()
    async def delete(self, ctx):
        if not Servers(ctx.guild.id).get():
            return await ctx.send(embed=Embeds("Der Server hat keine Daten in unserer Datenbank!").error())

        confirmation_message = await ctx.send(embed=discord.Embed(
            title=" ⚠️Willst du das wirklich machen?⚠️",
            description=f"**{ctx.author}**,Du willst dein Server aus der Datenbank löschen,bist du dir Sicher.",
            color=discord.Color.orange()
        ))

        emojis = ["✅", "❎"]

        for emoji in emojis: await confirmation_message.add_reaction(emoji)

        try:
            reaction, user = await self.bot.wait_for(
                'reaction_add',
                timeout=120,
                check=lambda r, u: r.emoji in emojis and r.message.id == confirmation_message.id and u.id == ctx.author.id
            )
        except asyncio.TimeoutError:
            await ctx.send(embed=Embeds("Server wurde nicht gelöscht, da die Zeit abgelaufen ist!").error())
            return await confirmation_message.delete()
        
        if reaction.emoji == emojis[1]:
            return await ctx.send(embed=Embeds("Serverlöschung gestoppt.").error())
        
        db_entry = Servers(ctx.guild.id)

        cache_data = db_entry.get()

        db_entry.delete()

        setting_up.remove(ctx.guild)

        del_message = await ctx.send(embed=discord.Embed(
            title="🗑️ Server gelöscht",
            description="Der Server wurde aus der Datenbank gelöscht, Du hast eine Minute Zeit um das rückgängig zu machen.",
            color=discord.Color.green()
        ))

        await del_message.add_reaction("♻️")

        try:
            await self.bot.wait_for(
                'reaction_add',
                timeout=60,
                check=lambda r,u: r.emoji == "♻️" and r.message.id == del_message.id and u.id == ctx.author.id
            )
        except asyncio.TimeoutError:
            try:
                wh = await self.bot.fetch_webhook(cache_data['webhook'])
                await wh.delete()
            except:
                pass
            return await del_message.remove_reaction("♻️", self.bot.user)

        if Servers(ctx.guild.id).get():
            try:
                wh = await self.bot.fetch_webhook(cache_data['webhook'])
                await wh.delete()
            except:
                pass
            return await ctx.send(embed=discord.Embed(
                title="❎ Restoren des Servers nicht möglich",
                description="Du musst deinen Server nochmal setupen mit =setup",
                color=discord.Color.red()
            ))

        Servers(ctx.guild.id).add(**cache_data)

        return await ctx.send(embed=discord.Embed(
            title="♻️ Server Restored",
            description="Dein Server wurde wieder hergestellt.",
            color=discord.Color.green()
        ))

    @setup.before_invoke
    @delete.before_invoke
    async def add_to_setting_up(self, ctx):
        setting_up.append(ctx.guild)

    @setup.after_invoke
    @delete.after_invoke
    async def remove_from_setting_up(self, ctx):
        try:
            setting_up.remove(ctx.guild)
        except: pass

def setup(bot):
    bot.add_cog(BumpSetup(bot))