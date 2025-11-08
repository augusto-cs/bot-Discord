import discord
from discord.ext import commands, tasks
from datetime import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online e pronto pra uso!")

@bot.command()
async def limpar(ctx:commands.Context, quantidade:int):
    await ctx.channel.purge(limit=quantidade + 1)
    
@bot.command()
async def info(ctx:commands.Context, membro:discord.Member = None):
    if membro is None:
        membro = ctx.author
    minha_embed = discord.Embed(title=f"Informações de {membro.display_name}")
    minha_embed.add_field(name="ID do usuário", value=f"{membro.id}")
    data_criacao = membro.created_at.strftime("%d/%m/%Y")
    data_entrada = membro.joined_at.strftime("%d/%m/%Y")
    minha_embed.add_field(name="Conta Criada em", value=data_criacao)
    minha_embed.add_field(name="Entrou no servidor em", value=data_entrada)
    await ctx.send(embed=minha_embed)
    
@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    palavras_proibidas = ["fdp", "filho da puta", "puta", "se mata"]
    for palavra in palavras_proibidas:
        if palavra in msg.content.lower():
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention}, essas palavras são proibidas por aqui, trate de mudar esse vocabulário porco!")
            return
    await bot.process_commands(msg)
    
@bot.event
async def on_member_join(membro: discord.Member):
    canal_boas_vindas = bot.get_channel(1436387254049439794)
    embed_boas_vindas = discord.Embed(title="Bem-vindo ao servidor!", description=f"Olá {membro.mention}, seja muito bem-vindo ao nosso servidor! Leia as regras e divirta-se!")
    embed_boas_vindas.set_thumbnail(url=membro.avatar.url)
    if canal_boas_vindas is not None:
        await canal_boas_vindas.send(embed=embed_boas_vindas)
    else:
        print("ERRO: Canal de boas-vindas não encontrado!")
        
@bot.command()
async def gemini(ctx:commands.Context, *, pergunta:str):
    await ctx.send(f"Ok, {ctx.author.mention}, estou pensando na resposta...")
    
    try:
        model = genai.GenerativeModel('models/gemini-flash-latest')
        response = await model.generate_content_async(pergunta)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Desculpe, {ctx.author.mention}, ocorreu um erro ao tentar obter a resposta: {e}")

bot.run(TOKEN)