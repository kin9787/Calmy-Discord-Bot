############################################################
# NOTICE: ONLY WORKS FOR discord.py VERSION 0.16.12 OR LOWER 
#############################################################


import random
import requests
import discord
import asyncio
import nacl.secret
from discord.ext.commands import Bot
from discord import Game
from discord.ext import commands

# whole script is aim to create a behavior bot
# check note for future descriptions

#######################################################################################################################
# all variables are located here
BOT_PREFIX = "-"
TOKEN = "GET-YOUR-OWN-TOKEN"
client = commands.Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')


#######################################################################################################################
# all independent functions are located here
async def status_task():
    while True:
        await client.change_presence(game=Game(name='with humans.'))
        await asyncio.sleep(300)
        await client.change_presence(game=Game(name='with myself. :('))
        await asyncio.sleep(300)


#######################################################################################################################
# functions without decorations

# to check connected servers
async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current connected server: ')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(86400)


#######################################################################################################################
# event decoration functions

# prints out bot name & id
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('Bot Identification Number: ' + client.user.id)
    print('----------')
    # changes bot status
    client.loop.create_task(status_task())


# function to state help descriptions and test bot presence
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('-hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('-bot'):
        await client.send_message(message.channel, 'I\'m right here')

    await client.process_commands(message)


# reaction when user joined
@client.event
async def on_member_join(member):
    print('Member joined.')
    wlc_phrase = ['Only one rule: No bullshits please.',
                  'Would you kindly your weapons away.',
                  'Welcome to Atlantis.',
                  'Fights are allowed outside only']
    await client.send_message(client.get_channel('540510607384903684'),
                              'Welcome {0}, to our humble server.'.format(member) +
                              random.choice(wlc_phrase))
    role = discord.utils.get(member.server.roles, name='Peasants')
    await client.add_roles(member, role)


# reaction when user left
@client.event
async def on_member_remove(member):
    print('Member left.')
    goodbye_phrase = ['Come back soon!',
                      'As the wise man once said,\"he\'s definitely a beta.\" ',
                      'I bet he left us for a women.',
                      'Without leaving or saying anything as he left.']
    await client.send_message(client.get_channel('540510607384903684'),
                              'Alert, adventurer {0} has left the channel.'.format(member) +
                              random.choice(goodbye_phrase))


@client.event
async def on_member_ban(member):
    print('Member banned.')
    ban_phrase = ['This is the elders final decision, please be understanding.'
                  'Adventurer {0} has been banned from the server.May we meet again at another place.',
                  'Perhaps we will meet again, some day, some where.']
    await client.send_message(client.get_channel('540510607384903684'),
                              'Attention,after discussing with the elders,'
                              ' we are sorry to announce that adventurer {0}'
                              ' has been banned from the server.'.format(member) +
                              random.choice(ban_phrase).format(member))


@client.event
async def on_member_unban(server, user):
    print('Ban lifted for someone.')
    ban_lifted_phrase = ['HE IS BACK!!!',
                         'Return as a new leaf...or not?',
                         'We welcome you back to our server.',
                         'Good to see you again!']
    await client.send_message(client.get_channel('540510607384903684'),
                              'Good news!{0} has finally return to us after the great argument war!'.format(user) +
                              random.choice(ban_lifted_phrase))


@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, "{0} has reacted to the message:\"{2}\" with  {1}  !".
                              format(user.name, reaction.emoji, reaction.message.content))


@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, "{0} has removed the reaction \'{1}\' from the message: {2}.".
                              format(user.name, reaction.emoji, reaction.message.content))


#######################################################################################################################
# command decorated functions

# summon bot
@client.command(pass_context=True, aliases=['summon', 'Summon'])
async def join_voice(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


# disconnect bot
@client.command(pass_context=True, aliases=['leave', 'bye', 'Leave'])
async def leave_voice(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(brief='Disconnects Calmy', description='Does what it stated.Logout Calmy.',
                aliases=['logoff', 'shutdown'])
async def logout():
    await client.say('Calmy Out!!!')
    print('Calmy Out!!!')
    await client.logout()


# delete messages
@client.command(brief='Delete messages.',
                description='Command = -clear n+1, n = number of messages required to delete. '
                            'Example,required to delete 3 messages: -clear 4', pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Number of message/s deleted : {0}'.format(amount))


# to tell when a member joins the server
@client.command
async def joined(member: discord.Member):
    await client.say('{0.name}joined in {0.joined_at}'.format(member))


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.add_field(name='About Author', value='About the author.', inline=False)
    embed.set_author(name='Help')
    embed.add_field(name='Summon', value='Summons Calmy.', inline=False)
    embed.add_field(name='Leave', value='Disconnect Calmy from voice channel.', inline=False)
    embed.add_field(name='BitCoin', value='Check for BitCoin price.', inline=False)
    embed.add_field(name='Temp', value='Check for current temperature.', inline=False)
    embed.add_field(name='8ball', value='Test your luck with eight ball!', inline=False)
    embed.add_field(name='Logout', value='Shut Down Calmy.', inline=False)

    print('{0} needed help!'.format(author))

    await client.send_message(author, embed=embed)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# extra functions for bot


# 8_ball_function
@client.command(name='eight_ball',
                description='Test your luck in the eight ball of...of....of luck?',
                brief='Test your luck!.',
                aliases=['8_ball', '8ball', 'ball', 'eight ball'],
                pass_context=True)
async def eight_ball(context):
    possible_response = ['Today you will face something that will change your life',
                         'Possible chances of getting laid.Possible',
                         'Stay calm and carry on, don\'t f**king look back',
                         'Alright, it says right here.....you\'re f**ked']

    await client.say(random.choice(possible_response) + ', ' + context.message.author.mention)
    author = context.message.author
    print('{0} spinned the 8 ball!!!'.format(author))


# check for BTC price
@client.command(pass_context=True, brief='Check for BTC price.', aliases=['btc', 'BTC', 'BitCoin'])
async def bitcoin(ctx):
    url = 'http://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say('Bitcoin price is: $' + value + '(USD)')
    author = ctx.message.author
    print('{0} has checked for BitCoin price.'.format(author))


# check for temperature
@client.command(pass_context=True, brief='Check for temperature.', aliases=['temp', 'Temp'])
async def temperature(ctx):
    url_weather = 'http://api.openweathermap.org/data/2.5/weather?q=Malaysia&&APPID=9c5be411701c5a3ef7de494fb9d0420d'
    response_weather = requests.get(url_weather)
    value_weather = response_weather.json()['main']['temp']
    real_value = str(value_weather)
    await client.say('Temperature for today is ' + real_value + ' F ')
    author = ctx.message.author
    print('{0} has checked the temperature.'.format(author))


# check author details
@client.command(pass_context=True, aliases=['about author', 'AboutAuthor', 'aboutauthor', 'About Author'])
async def about_author():
    embed = discord.Embed(
        title='Some info about the creator.',
        description='Created Calmy on 30/1/2019',
        colour=discord.Colour.purple()
    )

    embed.set_footer(text='© 2019 Cereal Monster')
    embed.set_image(url='https://vignette.wikia.nocookie.net/pyruslords/images/5/51/Derp_Face.png/revision'
                        '/latest?cb=20130515193137')
    embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/pyruslords/images/5/51/Derp_Face.png/revision'
                            '/latest?cb=20130515193137')
    embed.set_author(name='Cereal Monster',
                     icon_url='https://vignette.wikia.nocookie.net/pyruslords/images/5/51/Derp_Face.png/revision'
                              '/latest?cb=20130515193137')
    embed.add_field(name='Real Name:', value='You will need to PM me.', inline=False)
    embed.add_field(name='Email:', value='xiiaozenth@gmail.com', inline=False)
    embed.add_field(name='Github Profile Link:', value='https://github.com/kin9787', inline=True)
    embed.add_field(name='Check out my full code on Github!', value='https://github.com/kin9787/Calmy-Discord-Bot.git',
                    inline=True)

    await client.say(embed=embed)

    print('Someone called the master!!!')


#######################################################################################################################
# code starts execute
client.loop.create_task(list_server())
client.run(TOKEN)
