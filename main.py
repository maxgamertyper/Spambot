import os
import discord
from discord import Webhook
from discord.ext import tasks, commands
import random
import TenGiphPy
from bs4 import BeautifulSoup
import requests
from replit import db
import aiohttp
import keep_alive

banned_words = [
  'Arse', 'Ass', 'Asshole', 'Chink', 'Isis', 'Islamophobe', 'homophobe',
  'Bombing', 'Sexyhot', 'Bastard', 'Bitch', 'Fucker', 'Cunt', 'Damn', 'Fuck',
  'Goddamn', 'Shit', 'Motherfucker', 'Nigga', 'Nigger', 'Prick', 'Shit',
  'shit', 'ass', 'Shitass', 'bitch', 'Whore', 'Thot', 'Slut', 'Faggot', 'Dick',
  'Pussy', 'Penis', 'Vagina', 'Negro', 'Coon', 'Bitched', 'Sexist', 'Freaking',
  'Cock', 'Sucker', 'Lick', 'Licker', 'Rape', 'Molest', 'Anal', 'Buttrape',
  'Coont', 'Cancer', 'Sex', 'Retard', 'Fuckface', 'Dumbass', '5h1t', '5hit',
  'A_s_s', 'a2m', 'a55', 'adult', 'amateur', 'anal', 'anal', 'impaler†††',
  'anal', 'leakage†††', 'anilingus', 'anus', 'ar5e', 'arrse', 'arse',
  'arsehole', 'ass', 'ass', 'fuck†††', 'asses', 'assfucker', 'ass-fucker',
  'assfukka', 'asshole', 'asshole', 'assholes', 'assmucus†††', 'assmunch',
  'asswhole', 'autoerotic', 'b!tch', 'b00bs', 'b17ch', 'b1tch', 'ballbag',
  'ballsack', 'box†††', 'bangbros', 'bareback', 'bastard', 'beastial',
  'beastiality', 'curtain†††', 'bellend', 'bestial', 'bestiality', 'bi+ch',
  'biatch', 'bimbos', 'birdlock', 'bitch', 'bitch', 'tit†††', 'bitcher',
  'bitchers', 'bitches', 'bitchin', 'bitching', 'bloody', 'blow job', 'blow',
  'me†††', 'mud†††', 'blowjob', 'blowjobs', 'blue', 'waffle†††', 'blumpkin†††',
  'boiolas', 'bollock', 'bollok', 'boner', 'boob', 'boobs', 'booobs',
  'boooobs', 'booooobs', 'booooooobs', 'breasts', 'buceta', 'bugger', 'bum',
  'bunny', 'fucker', 'bust a load†††', 'busty', 'butt', 'butt', 'fuck†††',
  'butthole', 'buttmuch', 'buttplug', 'c0ck', 'c0cksucker', 'carpet',
  'muncher', 'carpetmuncher', 'cawk', 'chink', 'choade†††', 'chota', 'bags†††',
  'cipa', 'cl1t', 'clit', 'clit', 'licker†††', 'clitoris', 'clits', 'clitty',
  'litter†††', 'clusterfuck', 'cnut', 'cock', 'cock', 'pocket†††', 'cock',
  'snot†††', 'cockface', 'cockhead', 'cockmunch', 'cockmuncher', 'cocks',
  'cocksuck', 'cocksucked', 'cocksucker', 'cock-sucker', 'cocksucking',
  'cocksucks', 'cocksuka', 'cocksukka', 'cok', 'cokmuncher', 'coksucka',
  'coon', 'cop', 'some', 'wood†††', 'cornhole†††', 'corp', 'whore†††', 'cox',
  'cum', 'cum', 'chugger†††', 'cum', 'dumpster†††', 'cum', 'freak†††', 'cum',
  'guzzler†††', 'cumdump†††', 'cummer', 'cumming', 'cums', 'cumshot',
  'cunilingus', 'cunillingus', 'cunnilingus', 'cunt', 'cunt', 'hair†††',
  'cuntbag†††', 'cuntlick', 'cuntlicker', 'cuntlicking', 'cunts',
  'cuntsicle†††', 'cunt-struck†††', 'cut', 'rope†††', 'cyalis', 'cyberfuc',
  'cyberfuck', 'cyberfucked', 'cyberfucker', 'cyberfuckers', 'cyberfucking',
  'd1ck', 'damn', 'dick', 'dick', 'hole†††', 'dick', 'shy†††', 'dickhead',
  'dildo', 'dildos', 'dink', 'dinks', 'dirsa', 'dirty', 'Sanchez†††', 'dlck',
  'dog-fucker', 'doggie', 'style', 'doggiestyle', 'doggin', 'dogging',
  'donkeyribber', 'doosh', 'duche', 'dyke', 'dick†††', 'pie†††', 'ejaculate',
  'ejaculated', 'ejaculates', 'ejaculating', 'ejaculatings', 'ejaculation',
  'ejakulate', 'erotic', 'f4nny', 'facial†††', 'fag', 'fagging', 'faggitt',
  'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'fanny', 'fannyflaps',
  'fannyfucker', 'fanyy', 'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck',
  'fecker', 'felching', 'fellate', 'fellatio', 'fingerfuck', 'fingerfucked',
  'fingerfucker', 'fingerfuckers', 'fingerfucking', 'fingerfucks', 'fist',
  'fuck†††', 'fistfuck', 'fistfucked', 'fistfucker', 'fistfuckers',
  'fistfucking', 'fistfuckings', 'fistfucks', 'flange', 'flog', 'log†††',
  'fook', 'fooker', 'fuck', 'hole†††', 'fuck', 'puppet†††', 'fuck',
  'trophy†††', 'fuck', 'mama†††', 'fuck†††', 'fucka', 'fuck-ass†††',
  'fuck-bitch†††', 'fucked', 'fucker', 'fuckers', 'fuckhead', 'fuckheads',
  'fuckin', 'fucking', 'fuckings', 'fuckingshitmotherfucker', 'fuckme',
  'fuckmeat†††', 'fucks', 'fucktoy†††', 'fuckwhit', 'fuckwit', 'fudgepacker',
  'fuk', 'fuker', 'fukker', 'fukkin', 'fuks', 'fukwhit', 'fukwit', 'fux',
  'fux0r', 'gangbang', 'gangbang†††', 'gang-bang†††', 'gangbanged',
  'gangbangs', 'gassy', 'ass†††', 'gaylord', 'gaysex', 'goatse', 'god', 'god',
  'damn', 'god-dam', 'goddamn', 'goddamned', 'god-damned', 'flap†††',
  'hardcoresex', 'heshe', 'hoar', 'hoare', 'hoer', 'homoerotic', 'hore',
  'horniest', 'horny', 'hotsex', 'jackoff', 'jack-off', 'jap', 'jerk',
  'jerk-off', 'jism', 'jiz', 'jizm', 'jizz', 'kawk', 'kinky', 'Jesus†††',
  'knob', 'knob', 'end', 'knobead', 'knobed', 'knobend', 'knobend', 'knobhead',
  'knobjocky', 'knobjokey', 'kock', 'kondum', 'kondums', 'kum', 'kummer',
  'kumming', 'kums', 'kunilingus', 'kwif†††', 'l3i+ch', 'l3itch', 'labia',
  'LEN', 'lmao', 'lmfao', 'lmfao', 'lust', 'lusting', 'm0f0', 'm0fo',
  'm45terbate', 'ma5terb8', 'ma5terbate', 'mafugly†††', 'masochist',
  'masterb8', 'masterbat*', 'masterbat3', 'masterbate', 'master-bate',
  'masterbation', 'masterbations', 'masturbate', 'mof0', 'mofo', 'mo-fo',
  'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked',
  'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking',
  'mothafuckings', 'mothafucks', 'mother', 'fucker', 'mother', 'fucker†††',
  'motherfuck', 'motherfucked', 'motherfucker', 'motherfuckers',
  'motherfuckin', 'motherfucking', 'motherfuckings', 'motherfuckka',
  'motherfucks', 'muff', 'muff', 'puff†††', 'mutha', 'muthafecker',
  'muthafuckker', 'muther', 'mutherfucker', 'n1gga', 'n1gger', 'nazi',
  'dick†††', 'nigg3r', 'nigg4h', 'nigga', 'niggah', 'niggas', 'niggaz',
  'nigger', 'niggers', 'nob', 'nob', 'jokey', 'nobhead', 'nobjocky',
  'nobjokey', 'numbnuts', 'nut', 'butter†††', 'nutsack', 'orgasim', 'orgasims',
  'orgasm', 'orgasms', 'p0rn', 'pawn', 'pecker', 'penis', 'penisfucker',
  'phonesex', 'phuck', 'phuk', 'phuked', 'phuking', 'phukked', 'phukking',
  'phuks', 'phuq', 'pigfucker', 'pimpis', 'piss', 'pissed', 'pisser',
  'pissers', 'pisses', 'pissflaps', 'pissin', 'pissing', 'pissoff', 'poop',
  'porn', 'porno', 'pornography', 'pornos', 'prick', 'pricks', 'pron', 'pube',
  'pusse', 'pussi', 'pussies', 'pussy', 'pussy', 'fart†††', 'pussy',
  'palace†††', 'pussys', 'queaf†††', 'queer', 'rectum', 'retard', 'rimjaw',
  'rimming', 'hit', 's.o.b.', 's_h_i_t', 'sadism', 'sadist', 'sandbar†††',
  'sausage', 'queen†††', 'schlong', 'screwing', 'scroat', 'scrote', 'scrotum',
  'semen', 'sex', 'sh!+', 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin',
  'shagging', 'shemale', 'shi+', 'shit', 'shit', 'fucker†††', 'shitdick',
  'shite', 'shited', 'shitey', 'shitfuck', 'shitfull', 'shithead', 'shiting',
  'shitings', 'shits', 'shitted', 'shitter', 'shitters', 'shitting',
  'shittings', 'shitty', 'skank', 'slope†††', 'slut', 'slut', 'bucket†††',
  'sluts', 'smegma', 'smut', 'snatch', 'son-of-a-bitch', 'spac', 'spunk',
  't1tt1e5', 't1tties', 'teets', 'teez', 'testical', 'testicle', 'tit', 'tit',
  'wank†††', 'titfuck', 'tits', 'titt', 'tittie5', 'tittiefucker', 'titties',
  'tittyfuck', 'tittywank', 'titwank', 'tosser', 'turd', 'tw4t', 'twat',
  'twathead', 'twatty', 'twunt', 'twunter', 'v14gra', 'v1gra', 'vagina',
  'viagra', 'vulva', 'w00se', 'wang', 'wank', 'wanker', 'wanky', 'whoar',
  'whore', 'xrated', 'sucker', 'dumbass', 'Kys', 'Kill', 'Die', 'Cliff',
  'Bridge', 'Shooting', 'Shoot', 'Bomb', 'Terrorist', 'Terrorism', 'Bombed',
  'Necrophilia', 'Mongoloid', 'Furfag', 'Cp', 'Pedo', 'Pedophile',
  'Pedophilia', 'Child', 'predator', 'Predatory', 'Depression', 'Redtube',
  'Loli', 'Lolicon', 'Cub'
]

db['textspam'] = {}
db['pingspam'] = {}
db['emojispam'] = {}
db['imagespam'] = {}
db['gifspam'] = {}
db['chats'] = {}

intents = discord.Intents.default()
bot = discord.AutoShardedBot(intents=intents)

tokens = {'tenor': 'JTZMGFDZMXVO', 'giphy': 'AwsTARN30Ygu4BacRqd3NO4ChecU731X'}
b = TenGiphPy.Tenor(token=tokens['tenor'])

spamlogs = discord.SlashCommandGroup(
  name='spamlogs', description='spamming log related commands')


async def on_spam_started(type, m, user, guild, length, channel):
  try:
    id = db[str(guild.id)]['webid']
  except:
    return
  embed = discord.Embed(color=0x0000ff, timestamp=discord.utils.utcnow())
  embed.add_field(name='Spam:', value='**Started**')
  embed.add_field(name='Message:', value=m, inline=False)
  embed.add_field(name='Type:', value=type, inline=False)
  embed.add_field(name='User:', value=user, inline=False)
  embed.add_field(name='Length:', value=length, inline=False)
  embed.add_field(name='Channel:',
                  value=f'[**here**]({channel.jump_url})',
                  inline=False)
  webs = await guild.webhooks()
  for i in webs:
    if i.id == id:
      w = i
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url(w.url, session=session)
    await webhook.send(embed=embed,
                       username='Spambot',
                       avatar_url=bot.user.avatar.url)


@bot.slash_command(name='sldisable',
                   description='disable the spamlog channel for this server')
async def sldisable(ctx):
  await ctx.defer()
  erembed = discord.Embed(color=0xc22b2b)
  erembed.add_field(
    name='Result:',
    value=
    'You don\'t have permission to use this command or you dont have join logs setup yet'
  )
  sembed = discord.Embed(color=0x11c27b)
  sembed.add_field(name='Result:',
                   value='Join logs have been succesfully disabled')
  if ctx.author.guild_permissions.manage_channels:
    try:
      webid = db[str(ctx.guild.id)]['webid']
    except:
      await ctx.respond(embed=erembed)
    try:
      web = await ctx.guild.webhooks()
      for i in web:
        if i.id == webid:
          webhook = i
      await webhook.delete()
      del db[str(ctx.guild.id)]['webid']
      await ctx.respond(embed=sembed)
    except:
      await ctx.respond(embed=erembed, ephemeral=True)
  else:
    await ctx.respond(embed=erembed, ephemeral=True)


@bot.slash_command(name='slenable', description='turn on spamlogs')
async def slenable(ctx, channel: discord.TextChannel):
  await ctx.defer()
  sembed = discord.Embed(color=0x11c27b)
  sembed.add_field(
    name='Result:',
    value=f'Spambot Logs channel succesfully set as {channel.mention}')
  erembed = discord.Embed(color=0xc22b2b)
  erembed.add_field(name='Result:',
                    value='You don\'t have permission to use this command')
  if ctx.author.guild_permissions.manage_channels:
    token = os.getenv('TOKEN')
    with open('spambot.png', 'rb') as f:
      a = f.read()
      f.close()
    try:
      id = db[str(ctx.guild.id)]['webid']
      w = None
      webs = await ctx.guild.webhooks()
      for i in webs:
        if i.id == id:
          w = i
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(w.url, session=session, bot_token=token)
        await webhook.edit(channel=channel)
      return await ctx.respond(embed=sembed)
    except:
      webhook = await channel.create_webhook(name='Spambot Spam logs',
                                             avatar=a)
      db[str(ctx.guild.id)]['webid'] = webhook.id
      return await ctx.respond(embed=sembed)
  else:
    await ctx.respond(embed=erembed, ephemeral=True)


@bot.slash_command(name='secret', guild_ids=[1106881297009365076])
async def secret(ctx):
  await ctx.defer()
  await ctx.respond('shhhhh')


@bot.slash_command(name='textspam',
                   description='start a textspam in this channel')
async def textspam(ctx, message: str, count: int):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if 'https://' in message or 'www.' in message or '.com' in message or '.net' in message or '.org' in message:
    return await ctx.respond('sorry, links are not allowed in messages')
  for i in banned_words:
    if i in message:
      print(i, message)
      return await ctx.respond(
        'sorry there is an inappropriate word in your text')
  for i in ctx.guild.members:
    if i.mention in message:
      return await ctx.respond(
        'This command is not for pinging please use /pingspam for that')
  if "@everyone" in message or "@here" in message:
    return await ctx.respond(
      'This command is not for pinging please use /pingspam for that')
  if str(ctx.channel.id) in db['textspam']:
    return await ctx.respond(
      'There is already a textspam running in this channel')
  db['textspam'][str(ctx.channel.id)] = {'count': count, 'message': message}
  await on_spam_started('textspam', message, ctx.author, ctx.guild, count,
                        ctx.channel)
  return await ctx.respond(f'Starting textspam lasting **{count}** messages')


@bot.slash_command(name='textstop',
                   description='stop any textspam in this channel')
async def textstop(ctx):
  await ctx.defer()
  if str(ctx.channel.id) in db['textspam']:
    del db['textspam'][str(ctx.channel.id)]
    return await ctx.respond('Stopping textspam in this channel')
  return await ctx.respond('There is no textspam running in this channel')


@bot.slash_command(name='pingspam',
                   description='start a pingspam in this channel')
async def pingspam(ctx, user: discord.Member, count: int):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if str(ctx.channel.id) in db['pingspam']:
    return await ctx.respond(
      'There is already a pingspam running in this channel')
  db['pingspam'][str(ctx.channel.id)] = {
    'count': count,
    'message': user.mention
  }
  await on_spam_started('pingspam', user.mention, ctx.author, ctx.guild, count,
                        ctx.channel)
  return await ctx.respond(f'Starting pingspam lasting **{count}** pings')


@bot.slash_command(name='spamchannels',
                   description='set the channels where spambot will spam')
async def spamchannels(
  ctx, function: discord.Option(choices=["Add", "Remove", "List","Clear","Fill"]),channel:discord.TextChannel=None):
  if not ctx.author.guild_permissions.manage_channels:
    return await ctx.respond("You do not have permission to use this command")
  #,channel:discord.channel=None)
  await ctx.defer()
  if function == "Add":
    if channel is None:
      return await ctx.respond('Provide a channel for this function')
    if str(channel.id) in db[str(ctx.guild.id)]['channels']:
      return await ctx.respond(f'{channel.mention} can already be spammed in')
    else:
      db[str(ctx.guild.id)]['channels'].append(str(channel.id))
      return await ctx.respond(f'{channel.mention} can now be spammed in')
  elif function == "Remove":
    if channel is None:
      return await ctx.respond('Provide a channel for this function')
    if str(channel.id) not in db[str(ctx.guild.id)]['channels']:
      return await ctx.respond(f"{channel.mention} already can't be spammed in")
    else:
      db[str(ctx.guild.id)]['channels'].remove(str(channel.id))
      return await ctx.respond(f'{channel.mention} can no longer be spammed in')
  elif function == "List":
    embed = discord.Embed(title='Spam channels', color=0x9e4ecc)
    channels=[]
    for channelid in db[str(ctx.guild.id)]['channels']:
      channel = await bot.fetch_channel(channelid)
      channels.append(channel.mention)
    embed.add_field(name='Channels:', value=', '.join(channels))
    return await ctx.respond(embed=embed)
  elif function == "Clear":
    db[str(ctx.guild.id)]['channels']=[]
    return await ctx.respond(f"No channels can be spammed in anymore")
  elif function == "Fill":
    db[str(ctx.guild.id)]['channels']=[str(channel.id) for channel in ctx.guild.text_channels]
    return await ctx.respond(f"All channels can be spammed in now")


@bot.slash_command(name='pingstop',
                   description='stop any pingspam in this channel')
async def pingstop(ctx):
  await ctx.defer()
  if str(ctx.channel.id) in db['pingspam']:
    del db['pingspam'][str(ctx.channel.id)]
    return await ctx.respond('Stopping pingspam in this channel')
  return await ctx.respond('There is no pingspam running in this channel')


@bot.slash_command(
  name='emojispam',
  description=
  'start a emojispam in this channel (default includes default discord emojis)'
)
async def emojispam(ctx, count: int, default_emojis: bool = True):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if str(ctx.channel.id) in db['emojispam']:
    return await ctx.respond(
      'There is already a emojispam running in this channel')
  await on_spam_started('emojispam', 'any server or discord emoji', ctx.author,
                        ctx.guild, count, ctx.channel)
  db['emojispam'][str(ctx.channel.id)] = {
    'count': count,
    'default': default_emojis
  }
  return await ctx.respond(f'Starting emojispam lasting **{count}** emojis')


@bot.slash_command(name='emojistop',
                   description='stop any emojispam in this channel')
async def emojistop(ctx):
  await ctx.defer()
  if str(ctx.channel.id) in db['emojispam']:
    del db['emojispam'][str(ctx.channel.id)]
    return await ctx.respond('Stopping emojispam in this channel')
  return await ctx.respond('There is no emojispam running in this channel')


@bot.slash_command(name='imagespam',
                   description='start a imagespam in this channel')
async def imagespam(ctx, prompt: str, count: int):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if str(ctx.channel.id) in db['imagespam']:
    return await ctx.respond(
      'There is already a imagespam running in this channel')
  db['imagespam'][str(ctx.channel.id)] = {'count': count, 'text': prompt}
  await on_spam_started('imagespam', prompt, ctx.author, ctx.guild, count,
                        ctx.channel)
  return await ctx.respond(f'Starting imagespam lasting **{count}** images')


@bot.slash_command(name='imagestop',
                   description='stop any imagespam in this channel')
async def imagestop(ctx):
  await ctx.defer()
  if str(ctx.channel.id) in db['imagespam']:
    del db['imagespam'][str(ctx.channel.id)]
    return await ctx.respond('Stopping imagespam in this channel')
  return await ctx.respond('There is no imagespam running in this channel')


@bot.slash_command(name='gifspam',
                   description='start a gifspam in this channel')
async def gifspam(ctx, prompt: str, count: int):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if str(ctx.channel.id) in db['gifspam']:
    return await ctx.respond(
      'There is already a gifspam running in this channel')
  db['gifspam'][str(ctx.channel.id)] = {'count': count, 'text': prompt}
  await on_spam_started('imagespam', prompt, ctx.author, ctx.guild, count,
                        ctx.channel)
  return await ctx.respond(f'Starting gifspam lasting **{count}** gifs')


@bot.slash_command(name='gifstop',
                   description='stop any gifspam in this channel')
async def gifstop(ctx):
  await ctx.defer()
  if not str(ctx.channel.id) in db[str(ctx.guild.id)]['channels']:
    return await ctx.respond("sorry, you're not allowed to spam in this channel")
  if str(ctx.channel.id) in db['gifspam']:
    del db['gifspam'][str(ctx.channel.id)]
    return await ctx.respond('Stopping gifspam in this channel')
  return await ctx.respond('There is no gifspam running in this channel')


@tasks.loop(seconds=4)
async def textsend():
  if db['textspam'] is not None:
    try:
      for channel in db['textspam']:
        ch = await bot.fetch_channel(channel)
        if db['textspam'][str(channel)]['count'] == 0:
          del db['textspam'][str(channel)]
          continue
        try:
          await ch.send(db['textspam'][str(channel)]['message'])
          db['textspam'][str(channel)]['count'] -= 1
        except:
          del db['textspam'][str(channel)]
          continue
    except RuntimeError:
      pass


@tasks.loop(seconds=4)
async def pingsend():
  if db['pingspam'] is not None:
    try:
      for channel in db['pingspam']:
        ch = await bot.fetch_channel(channel)
        if db['pingspam'][str(channel)]['count'] == 0:
          del db['pingspam'][str(channel)]
          continue
        try:
          await ch.send(db['pingspam'][str(channel)]['message'])
          db['pingspam'][str(channel)]['count'] -= 1
        except:
          del db['pingspam'][str(channel)]
          continue
    except RuntimeError:
      pass


@tasks.loop(seconds=4)
async def emojisend():
  e_list = [
    ':grinning:', ':smiley:', ':smile:', ':grin:', ':laughing:',
    ':face_holding_back_tears:', ':sweat_smile:', ':joy:', ':rofl:',
    ':smiling_face_with_tear:', ':relaxed:', ':blush:', ':innocent:',
    ':slight_smile:', ':upside_down:', ':wink:', ':relieved:', ':heart_eyes:',
    ':smiling_face_with_3_hearts:', ':kissing_heart:', ':kissing:',
    ':kissing_smiling_eyes:', ':kissing_closed_eyes:', ':yum:',
    ':stuck_out_tongue:', ':stuck_out_tongue_closed_eyes:',
    ':stuck_out_tongue_winking_eye:', ':zany_face:',
    ':face_with_raised_eyebrow:', ':face_with_monocle:', ':nerd:',
    ':sunglasses:', ':disguised_face:', ':star_struck:', ':partying_face:',
    ':smirk:', ':unamused:', ':disappointed:', ':pensive:', ':worried:',
    ':confused:', ':confused:', ':slight_frown:', ':frowning2:', ':persevere:',
    ':confounded:', ':tired_face:', ':weary:', ':pleading_face:', ':cry:',
    ':sob:', ':triumph:', ':angry:', ':rage:',
    ':face_with_symbols_over_mouth:', ':exploding_head:', ':flushed:',
    ':hot_face:', ':cold_face:', ':face_in_clouds:', ':scream:', ':fearful:',
    ':cold_sweat:', ':disappointed_relieved:', ':sweat:', ':hugging:',
    ':thinking:', ':face_with_peeking_eye:', ':face_with_hand_over_mouth:',
    ':face_with_open_eyes_and_hand_over_mouth:', ':saluting_face:',
    ':shushing_face:', ':melting_face:', ':lying_face:', ':no_mouth:',
    ':dotted_line_face:', ':neutral_face:', ':face_with_diagonal_mouth:',
    ':expressionless:', ':grimacing:', ':rolling_eyes:', ':hushed:',
    ':frowning:', ':anguished:', ':open_mouth:', ':astonished:',
    ':yawning_face:', ':sleeping:', ':drooling_face:', ':sleepy:',
    ':face_exhaling:', ':dizzy_face:', ':face_with_spiral_eyes:',
    ':zipper_mouth:', ':woozy_face:', ':nauseated_face:', ':face_vomiting:',
    ':sneezing_face:', ':mask:', ':thermometer_face:', ':head_bandage:',
    ':money_mouth:', ':cowboy:', ':smiling_imp:', ':imp:', ':skull:', ':clown:'
  ]
  if db['emojispam'] is not None:
    try:
      for channel in db['emojispam']:
        ch = await bot.fetch_channel(channel)
        e_list = [
          i for i in ch.guild.emojis if i.is_usable()
        ] if db['emojispam'][str(channel)]['default'] == False else e_list + [
          i for i in ch.guild.emojis if i.is_usable()
        ]
        if db['emojispam'][str(channel)]['count'] == 0:
          del db['emojispam'][str(channel)]
          continue
        try:
          await ch.send(random.choice(e_list))
          db['emojispam'][str(channel)]['count'] -= 1
        except:
          del db['emojispam'][str(channel)]
          continue
    except RuntimeError:
      pass


@tasks.loop(seconds=4)
async def imagesend():
  if db["imagespam"] is not None:
    try:
      for channel in db["imagespam"]:
        ch = await bot.fetch_channel(int(channel))
        if db["imagespam"][channel]["count"] == 0:
          del db["imagespam"][channel]
        else:
          db["imagespam"][channel]["count"] -= 1
          text = db["imagespam"][channel]["text"]
          base_url = requests.get(
            f'https://www.google.com/search?q={text}&tbm=isch')
          bs = BeautifulSoup(base_url.content, 'html.parser')
          links = []
          for i in bs.find_all('img'):
            if 'https://encrypted-tbn0.gstatic.com/images?q=' in i['src']:
              links.append(i['src'])
          await ch.send(random.choice(links))
    except RuntimeError:
      pass


@tasks.loop(seconds=4)
async def gifsend():
  if db["gifspam"] is not None:
    try:
      for channel in db["gifspam"]:
        ch = await bot.fetch_channel(int(channel))
        if db["gifspam"][channel]["count"] == 0:
          del db["gifspam"][channel]
          continue
        else:
          db["gifspam"][channel]["count"] -= 1
          text = db["gifspam"][channel]["text"]
          await ch.send(f"{b.random(text)}")
    except RuntimeError:
      pass


@bot.slash_command(name='feedback',
                   description='send feedback to the devs of spambot')
async def feedback(ctx, feedback: str):
  await ctx.defer()
  ch = await bot.fetch_channel(1114756611412602941)
  await ch.send(f"From {ctx.author.mention}: {feedback}")
  return await ctx.respond("Your feedback has been sent. Thank You!")


@bot.slash_command(name='google',
                   description='get a google link to the query provided')
async def google(ctx, text: str):
  await ctx.defer()
  t2 = ''
  for i in text:
    if i == " ":
      i = '+'
    elif i == '+':
      i = '%2B'
    elif i == '/':
      i = '%2F'
    elif i == '!':
      i = '%21'
    elif i == '@':
      i = '%40'
    elif i == '#':
      i = '%23'
    elif i == '$':
      i = '%24'
    elif i == '%':
      i = '%25'
    elif i == '^':
      i = '%5E'
    elif i == '&':
      i = '%26'
    elif i == '(':
      i = '%28'
    elif i == ')':
      i = '%29'
    elif i == '=':
      i = '%3D'
    elif i == '`':
      i = '%60'
    elif i == '[':
      i = '%5B'
    elif i == ']':
      i = '%5D'
    elif i == '{':
      i = '%7B'
    elif i == '}':
      i = '%7D'
    elif i == '\\':
      i = '%5C'
    elif i == '|':
      i = '%7C'
    elif i == ';':
      i = '%3B'
    elif i == ':':
      i = '%3A'
    elif i == '\'':
      i = '%27'
    elif i == ',':
      i = '%2C'
    elif i == '?':
      i = '%3F'
    t2 += i
  await ctx.respond(f"https://www.google.com/search?q={t2}")


@bot.slash_command(name='supportserver',
                   description='Get the link to the support server')
async def supportserver(ctx):
  await ctx.defer()
  embed = discord.Embed(title="SpamBot",
                        description="A fun bot for people of all ages!",
                        color=0x0000ff)
  embed.set_footer(
    icon_url=
    "https://cdn.discordapp.com/attachments/645134064935763993/862304755694567434/unknown.png",
    text="powered by SpamBot devs and you")
  embed.add_field(name="support",
                  value="Need help with our bot come join the discord server")
  embed.add_field(name="Server link:",
                  value="[**here**](https://discord.gg/5dDk34yg4j)")
  await ctx.respond(embed=embed)


@bot.slash_command(name='bored', description='Bored? use this command')
async def bored(ctx):
  await ctx.defer()
  with open("bored.txt", "r") as f:
    content = f.read().splitlines()
    myline = random.choice(content)
    f.close()
  await ctx.respond(myline)


@bot.slash_command(name='credits', descrition='send the credits for this bot')
async def credits(ctx):
  await ctx.defer()
  embed = discord.Embed(title='Spambot Credits', color=0x0000ff)
  embed.add_field(name='Developers:', value='MaxGamer', inline=False)
  embed.add_field(name='Admins:', value='Tedda The Cat', inline=False)
  embed.add_field(name='boiger:', value='frogman.likesfrogs', inline=False)
  embed.add_field(
    name='Mods:',
    value=
    'Horizontal \n mr.muffler \n MagicDragon16 \n xxsavagexx \n Knightfall,',
    inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name='mc', description='view the member count of this bot')
async def mc(ctx):
  await ctx.defer()
  v = 0
  for i in bot.guilds:
    v += i.member_count
  embed = discord.Embed(color=0x9e4ecc)
  embed.add_field(name='Total Members:', value=v, inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name='sc', description='view the member count of this bot')
async def sc(ctx):
  await ctx.defer()
  embed = discord.Embed(color=0x9e4ecc)
  embed.add_field(name='Total Servers:', value=len(bot.guilds), inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name='help',
                   description='get help and information about this bot')
async def help(ctx, type: discord.Option(choices=["Spam", "Random", "Logs"])):
  await ctx.defer()
  sembed = discord.Embed(title='Spam Commands', color=0x0000ff)
  rembed = discord.Embed(title='Random Commands', color=0x0000ff)
  lembed = discord.Embed(title='Log Commands', color=0x0000ff)
  lembed.add_field(
    name="slenable <channel>",
    value=
    "Get a message sent to that channel anytime a spamcommand is activated")
  lembed.add_field(name="sldisable", value="disable spamlogs")
  rembed.add_field(
    name="Credits",
    value="Get the credits for the creators and helpers of the bot")
  rembed.add_field(name="Google <prompt>", value="google any prompt")
  rembed.add_field(name="Bored",
                   value="Get a randomised response related to bordem")
  rembed.add_field(name="sc", value="Get the server count of this bot")
  rembed.add_field(name="mc", value="Get the member count of this bot")
  rembed.add_field(name="feedback <text>",
                   value="Send the devs feedback using your text")
  rembed.add_field(name="Supportserver",
                   value="Get the spambot support server")
  sembed.add_field(
    name='Textspam <message> <count>',
    value=
    'starts a textspam in this channel where the message is the message that you specified and the count specified is how many times it will be spammed',
    inline=False)
  sembed.add_field(name='Textstop',
                   value='stops the textspam in that channel',
                   inline=False)
  sembed.add_field(
    name='Pingspam <user> <count>',
    value=
    'starts a pingspam in this channel where the ping is the user that you specified and the count specified is how many times it will be spammed',
    inline=False)
  sembed.add_field(name='Pingstop',
                   value='stops the pingspam in that channel',
                   inline=False)
  sembed.add_field(
    name='Emojispam <count>',
    value=
    'starts an emojispam in this channel where the emoji is a random discord or server emoji and the count specified is how many times it will be spammed',
    inline=False)
  sembed.add_field(name='Emojistop',
                   value='stops the emojispam in that channel',
                   inline=False)
  sembed.add_field(
    name='Imagespam <prompt> <count>',
    value=
    'starts an Imagespam in this channel where the image is an image related to the prompt and the count specified is how many times it will be spammed',
    inline=False)
  sembed.add_field(name='imagestop',
                   value='stops the imagespam in that channel',
                   inline=False)
  sembed.add_field(
    name='Gifspam <prompt> <count>',
    value=
    'starts a gifspam in this channel where the gif is related to the prompt and the count specified is how many times it will be spammed',
    inline=False)
  sembed.add_field(name='gifstop',
                   value='stops the gifspam in that channel',
                   inline=False)
  sembed.add_field(name="Still need more help?",
                   value="[**Support Server**](https://discord.gg/5dDk34yg4j)")
  lembed.add_field(name="Still need more help?",
                   value="[**Support Server**](https://discord.gg/5dDk34yg4j)")
  rembed.add_field(name="Still need more help?",
                   value="[**Support Server**](https://discord.gg/5dDk34yg4j)")
  if type == 'Spam':
    await ctx.respond(embed=sembed)
  elif type == 'Logs':
    await ctx.respond(embed=lembed)
  elif type == 'Random':
    await ctx.respond(embed=rembed)


@bot.event
async def on_ready():
  print(f'Bot ready with the name {bot.user}')
  await bot.change_presence(activity=discord.Game(
    name=f'Spam {len(bot.guilds)} Servers | /help'))


@bot.event
async def on_connect():
  print(f'Bot connected with the name {bot.user}')
  textsend.start()
  pingsend.start()
  emojisend.start()
  imagesend.start()
  gifsend.start()
  await bot.sync_commands()
  keep_alive.keep_alive()


@bot.event
async def on_guild_join(guild):
  db[str(guild.id)] = {}
  db[str(guild.id)]['channels'] = [str(channel.id) for channel in guild.text_channels]


@bot.event
async def on_guild_remove(guild):
  del db[str(guild.id)]


bot.run(os.getenv('TESTINGTOKEN'))
