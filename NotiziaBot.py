import discord
import json
import requests
import random
import os
from profanity import profanity


intents = discord.Intents.default()
intents.members = True


TOKEN = os.environ['Token']

client = discord.Client(intents=intents)

  

def get_weather():
  response = requests.get("https://api.weatherapi.com/v1/current.json?key=5d508c6aebdd4d399a0170342222506&q=India&aqi=yes")
  json_data = json.loads(response.content)
  temp = json_data['current']['temp_c']
  condn = json_data['current']['condition']['text']
  feel_temp = json_data['current']['feelslike_c']
  aqi = json_data['current']['air_quality']['pm2_5']
  weather_d = [temp, condn, feel_temp, aqi]
  return weather_d

def top_news():
  response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=c2cd6ea35abc474e8e6b071519621ada")
  json_data = json.loads(response.content)
  n = random.randint(1, 15)
  link = json_data['articles'][n]['url']
  return link

def news(country, category):
  response = requests.get("https://newsapi.org/v2/top-headlines?country={}&category={}&apiKey=f7afb8156501427d9873f9cc5806a5f2".format(country, category))
  json_data = json.loads(response.content)
  n = random.randint(1, 15)
  link = json_data['articles'][n]['url']
  return link


@client.event
async def on_member_join(member):
  guild = client.get_guild(836649957242699806)
  channel = client.get_channel(990329919185776710)
  mem = str(member)
  name = mem.split('#')[0]
  await channel.send("Welcome to {} :partying_face:, {}".format(guild, name))

@client.event
async def on_ready():
  print('{0.user} has logged in successfully'.format(client))


@client.event
async def on_message(message):

  msg = (message.content)

  if message.author == client.user:
    return

  if (profanity.contains_profanity(msg)):
    print('Warning')
    return
  
  if msg.startswith('~hello'):
    await message.channel.send('hello! Bitches')
    return
  
  if msg == '~weather':
    weather_d = get_weather()
    output = " **Temperature:** `{} °C`\n**Condition:** _`{}`_\n_**feels like~ **_ `{} °C`\n**AQI(2.5 PM):** `{}`".format(weather_d[0], weather_d[1], weather_d[2], weather_d[3])
    await message.channel.send(output)
    return 
  
  if msg == '~update':
    output = top_news();
    await message.channel.send(output)
    return

  str = msg.split()
  category = str[2]
  country = str[1]
  
  if (str[0] == '~update'):
    output = news(country, category)
    await message.channel.send(output)
    return
  
    
client.run(TOKEN)


