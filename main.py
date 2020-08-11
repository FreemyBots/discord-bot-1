# Imports
import discord 
from discord.ext import commands 
from discord.ext.commands import Bot 
import json 
import os 
import asyncio 
import time 
import logging 
import random 
import youtube_dl 

# Bot Variables
TOKEN = 'GET UR OWN'
Prefix = 'gc!'
inviteLink = 'https://discord.gg/cgtU5UQ'
playingStatus = f"{Prefix}help | {inviteLink}"
idchannel = 739256946426904627 # Channel for welcome msg (in FreemyBots server)
badWords = ['nigger', 'fuck', 'cum', 'slut', 'hoe', 'retard', 'rape', 'cunt', 'ass', 'idiot', 'cock', 'gay', 'ass'] 
# IDK i can't even make the censorship thing work correctly lol (line 181)


client = commands.Bot(command_prefix = Prefix)

# Remove the defualt $help command
client.remove_command("help")


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author 

    embed = discord.Embed(colour = discord.Colour.blue()) # Colour
    embed.set_author(name="Gaming Cavern's Command List") 
    embed.add_field(name='``Moderation``', value=f'{Prefix}moderation', inline=False) 
    embed.add_field(name='``Currency``', value=f'{Prefix}currency', inline=False)
    embed.add_field(name='``Fun``', value=f'{Prefix}fun', inline=False)
    
    await ctx.send(author.mention, embed=embed) 

@client.command(pass_context=True)
async def moderation(ctx):
    author = ctx.message.author 

    embed = discord.Embed(colour = discord.Colour.blue()) # Colour 
    embed.set_author(name='Moderation') 
    embed.add_field(name=f'{Prefix}clear', value='Clear messages', inline=False)
    embed.add_field(name=f'{Prefix}kick', value='Kick users', inline=False)
    embed.add_field(name=f'{Prefix}ban', value='Ban users', inline=False)
    embed.add_field(name=f'{Prefix}unban', value='Unban a user via user id', inline=False)
    embed.add_field(name=f'{Prefix}mute', value='Mute a user', inline=False)
    embed.add_field(name=f'{Prefix}unmute', value='Unmute a user', inline=False)
    await ctx.send(author.mention, embed=embed)

@client.command(pass_context=True)
async def fun(ctx):
    author = ctx.message.author

    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name='Fun')
    embed.add_field(name=f'{Prefix}ping', value='Get latency of the bot (expressed in ms)', inline=False)
    embed.add_field(name=f'{Prefix}whois', value='Get account information of a user', inline=False)
    embed.add_field(name=f'{Prefix}say', value='Make the bot repeat anything', inline=False)
    await ctx.send(author.mention, embed=embed)

@client.command(pass_context=True)
async def currency(ctx):
    pass
    
@client.event
async def on_ready():
    activity = discord.Game(name=playingStatus, type=3) 
    await client.change_presence(status=discord.Status.idle, activity=activity) 
    print("The bot is now online")

@client.event
async def on_member_join(member):
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.add_field(name=f'Gaming Cavern', value=f"Hello {member} and welcome to FreemyBots This is the testing bot for Gaming Cavern, type {Prefix} if you are in need of guidance, Gaming Cavern is a growing non toxic community for gamers accross the globe to interact with one another \n If you would like to support us more join {inviteLink} !", inline=False)
    

    
    print(f'{member} has joined a server.')

    await client.get_channel(idchannel).send(f"**Welcome** in {member.mention}. \nHope you enjoy your time here and... **Happy Gaming**")
    await member.send(embed=embed)

"""@client.event
async def on_member_remove(member, idchannel):
   await client.get_channel(idchannel).send(f"{member.mention} has left the server") """

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping: {client.latency}')

@client.command(name='ban', alliases=['banuser'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.Member, *, reason="No reason provided"):
    try:
        await user.ban(reason=reason)
        if reason == 'No reason provided':
            await ctx.send(f"{user} has been banned. {reason}")
        else:
            await ctx.send(f"{user} has been banned. \nReason: {reason}")
        
    except:
        await ctx.send("I can't ban this user.")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.Member, *, reason="No reason provided"):
    try:
        await user.kick(reason=reason)
        if reason == 'No reason provided':
            await ctx.send(f"{user} has been kicked. {reason}")
        else:
            await ctx.send(f"{user} has been kicked. \nReason: {reason}")
    except:
        await ctx.send("I can't kick this user.")

@client.command()
async def whois(ctx, user : discord.Member):
    embed= discord.Embed(
            colour = discord.Colour.green(),
        )
    pos = sum(m.joined_at < user.joined_at for m in ctx.guild.members if m.joined_at is not None)
    embed.set_author(name=f"User Info - {user}")
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=user.id, inline=False)
    embed.add_field(name="Server Nickname:", value=f"{user.display_name}")
            
    embed.add_field(name="Created On:", value=user.created_at.timestamp(), inline=False)
    embed.add_field(name="Join Position:", value=f"{user} is the #{pos} member to join", inline=False)
            
    await ctx.send(embed=embed)

@client.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    try:
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"{user} has been unbanned")
    except:
        await ctx.send(f"{user} is not banned")

@client.command(name='clear', pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount):
    try:
        await ctx.channel.purge(limit=int(amount)+1)
        if amount == '1':
            await ctx.send(f"{amount} message succesfully cleared")
        else:
            await ctx.send(f"{amount} messages succesfully cleared")
        
    except:
        if amount == '1':
            await ctx.send(f"Unable to delete {amount} message")
        else:
            await ctx.send(f"Unable to delete {amount} messages")


@client.command(pass_context=True)
async def unmute(ctx, user):
    try:
        role = discord.utils.get(user.guild.roles, name='Muted')
        await user.remove_roles(role)
        await ctx.send(f"{user} has been unmuted")
    except:
        await ctx.send("There is no role named Muted")
        
@client.command(name='mute')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, user: discord.Member, *, reason=None):
    try:
        role = discord.utils.get(user.guild.roles, name='Muted')
        await user.add_roles(role)
        await ctx.send(f"{user} has been muted")
    except:
        await ctx.send("There is no role named Muted")

@client.command(name='say')
async def say(ctx, *, msg):
    for word in msg.split():
        if word in badWords:
            await ctx.send("That word is not allowed")
            print(f"{ctx.message.author} tried to make me say a bad word")
            break
    if word != badWords:
        await ctx.send(f'{msg} \n \n- **{ctx.message.author}**')



client.run(TOKEN) 
