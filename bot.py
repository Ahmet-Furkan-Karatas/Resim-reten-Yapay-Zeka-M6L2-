import discord
from discord.ext import commands
from config import TOKEN, API_KEY, SECRET_KEY
from AIGenerator import FusionBrainAPI
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='generate')
async def generate_image(ctx, *, prompt: str = None):
    if not prompt:
        await ctx.send("Lütfen bir açıklama girin. Örnek: `!generate uçan araba gelecekte`")
        return

    await ctx.send("🎨 Görsel oluşturuluyor...")

    try:
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
        
        model_id = api.get_pipeline()
        uuid = api.generate(prompt, model_id)
        files = api.check_generation(uuid)

        image_base64 = files[0]
        image = api.decode_base64_to_image(image_base64)

        image_path = "output/generated_image.png"
        image.save(image_path)

        await ctx.send(file=discord.File(image_path))

        os.remove(image_path)

    except Exception as e:
        await ctx.send(f"❌ Bir hata oluştu: {e}")

bot.run(TOKEN)
