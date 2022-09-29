import datetime
import discord
import requests
from discord.ext import commands, tasks 
import dotenv
from dotenv import load_dotenv
import os

# Token do bot
load_dotenv()
token = os.getenv('token')

# Permissões
intents = discord.Intents.default()
intents.members = True
# Prefixo do bot
bot = commands.Bot(command_prefix='-', intents=intents)

# Ligando o bot
@bot.event
async def on_ready():
    print(f'Estou pronto! Estou conectado como {bot.user}')

# Evento de mensagens
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'palavrao' in message.content:  # Filtra a mensagem e se for 'palavrao' ela é apagada
        await message.channel.send(f'Por favor, {message.author.name}, não ofenda os demais usuários')
        await message.delete()
    if 'horario' in message.content:  # Ativa a função horario_atual digitando 'horario'
        horario_atual.start()
    if 'parar' in message.content:  # Para função horario_atual digitando 'pare'
        horario_atual.stop()
    await bot.process_commands(message)

# Evento de reações
# @bot.event
# async def on_reaction_add(reaction, user):
#    if reaction.emoji == '👍':
#        role = user.guild.get_role(991789476265328790)
#        await user.add_roles(role)
#    elif reaction.emoji == '👎':
#        role = user.guild.get_role(991789729936838707)
#        await user.add_roles(role)

# Comando -oi
@bot.command(name='Saudação', help='Responde educadamente caso digam "oi". Argumentos: oi')
async def send_hello(ctx):
    name = ctx.author.name
    response = 'Olá, ' + name
    await ctx.send(response)

# Comando -calcular (Faz qualquer cálculo desejado pelo usuário)
@bot.command(name='Calcular', help='Calcula expressões matemáticas. Argumentos: Expressão')
async def calcular_expressao(ctx, *expressao):
    expressao = ''.join(expressao)
    resposta = eval(expressao)
    await ctx.send('A resposta é ' + str(resposta))

# Comando -binance (Mostra o valor de um par de moedas)
@bot.command(help='Verifica o preço de um par na binance. Argumentos: moeda, base')
async def binance(ctx, coin, base):
    try:
        resposta = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}')
        coin = coin.upper()
        base = base.upper()
        dados = resposta.json()
        preco = dados.get('price')
        if preco:
            await ctx.send(f"O valor do par {coin}/{base} é {preco}")
        else:
            await ctx.send(f"O par {coin}/{base} é inválido")
    except Exception as error:
        await ctx.send(f"Ops...Deu algum erro!")
        print(error)

# Comando -segredo (Envia uma mensagem privada ao usuário)
@bot.command(name='Segredo ', help='Envia uma mensagem secreta no chat particular. Argumentos: segredo')
async def segredo(ctx):
    try:
        await ctx.author.send('Sou um bot em desenvolvimento...')
    except discord.errors.Forbidden:
        await ctx.send('Não posso te contar o segredo, Habilite receber mensagens de desconhecidos.')

# Comando -foto (Gera uma foto aleatória)
@bot.command(name='Foto', help='Busca uma imagem aleatória. Argumentos: foto')
async def imagem(ctx):
    url = 'https://picsum.photos/1920/1080'
    embed_imagem = discord.Embed(
        title='Resultado da busca de imagem',
        description='Imagem aleatória',
        color=0X0000FF
    )
    embed_imagem.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed_imagem.set_image(url=url)
    embed_imagem.set_footer(text='Feito por' + bot.user.name, icon_url=bot.user.avatar_url)

    embed_imagem.add_field(name='API', value='API utilizada: https://picsum.photos/')
    embed_imagem.add_field(name='Parâmetros', value='{largura}/{altura}')

    embed_imagem.add_field(name='Exemplo', value=url, inline=False)

    await ctx.send(embed=embed_imagem)

# Comando -copiar (Copia a mensagem do usuário e envia)
@bot.command(name='Copiar', help='Copia a mensagem do autor. Argumentos: copiar')
async def copiarmsg(ctx, *arg):
    await ctx.send(f'{len(arg)} arguments: {", ".join(arg)}')

# Comando -entrar (Entra na chamada do usuário)
@bot.command()
async def entrar(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

# Comando -sair (Sai da chamada do usuário)
@bot.command()
async def sair(ctx):
    await ctx.voice_client.disconnect()

# Comando - horario (Envia data atual e horário formatados)
@tasks.loop(seconds=2)
async def horario_atual():
    now = datetime.datetime.now()
    now = now.strftime('%d/%m/%Y as %H:%M:%S')
    channel = bot.get_channel(735474732631195719)
    await channel.send('Data atual: ' + now)

# Executa o bot
# Resetar token toda vez que divulgar o código
bot.run(token)
