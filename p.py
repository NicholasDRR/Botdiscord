import datetime

import discord
import requests
from discord.ext import commands, tasks

bot = commands.Bot('-')


@bot.event
async def on_ready():
    print(f'Estou pronto! Estou conectado como {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'viado' in message.content:
        await message.channel.send(f'Por favor, {message.author.name}, não ofenda os demais usuários')
        await message.delete()
    if 'horario' in message.content:
        horario_atual.start()
    if 'pare' in message.content:
        horario_atual.stop()
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '👍':
        role = user.guild.get_role(991789476265328790)
        await user.add_roles(role)
    elif reaction.emoji == '👎':
        role = user.guild.get_role(991789729936838707)
        await user.add_roles(role)


@bot.command(name='oi')
async def send_hello(ctx):
    name = ctx.author.name
    response = 'Olá, ' + name
    await ctx.send(response)


@bot.command(name='calcular')
async def calcular_expressao(ctx, *expressao):
    expressao = ''.join(expressao)
    resposta = eval(expressao)
    await ctx.send('A resposta é ' + str(resposta))


@bot.command()
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


@bot.command(name='segredo')
async def segredo(ctx):
    try:
        await ctx.author.send('O luiz é homossexual')
    except discord.errors.Forbidden:
        await ctx.send('Não posso te contar o segredo, Habilite receber mensagens de desconhecidos.')


@bot.command(name='foto')
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


@bot.command(name='copiar')
async def copiarmsg(ctx, *arg):
    await ctx.send(f'{len(arg)} arguments: {", ".join(arg)}')


@bot.command()
async def entrar(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def sair(ctx):
    await ctx.voice_client.disconnect()


@tasks.loop(seconds=2)
async def horario_atual():
    now = datetime.datetime.now()
    now = now.strftime('%d/%m/%Y as %H:%M:%S')
    channel = bot.get_channel(739854045707108463)
    await channel.send('Data atual: ' + now)


bot.run('OTkxNzQyNjMwOTI3MDE2MDg3.GJamxS.7tdXXtIUrq9QG3yx3XnTcsbS49Xu9v-iSWX8B0')
