import discord
from discord.ext import commands
from config import TOKEN, API_KEY, SECRET_KEY
from AIGenerator import FusionBrainAPI
import os
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

# 1. start/help komutu
@bot.command(name='start')
async def start(ctx):
    mesaj = """
    Merhaba! Ben bir görsel üretme botuyum.
    `!generate <metin>` komutunu kullanarak bana bir sahne tarif edebilirsin, ben de senin için görselini oluşturayım!
    Örneğin: `!generate uzayda yürüyen kedi`
    """
    await ctx.send(mesaj)

# 2. Botun şarkı söylüyormuş gibi görünmesi
@bot.command(name='sing')
async def sing(ctx):
    lyrics_list = [
        [
            "🎵 Göster herkese gerçek yüzünü",
            "🎶 Onlar arkadan havlar",
            "🎵 Rav-rav-rav-rav-rav-rav-rav",
            "🎶 Dedim ki 'Her şey bende var'",
            "🎵 Var-var-var-var-var-var-var",
            "🎶 Onlar arkadan havlar",
            "🎵 Rav-rav-rav-rav-rav-rav-rav",
            "🎶 Dedim ki 'Her şey bende var'",
            "🎵 Var-var-var-var-var-var-var"
        ],
        [
            "🎵 (Fark var) Seninle iyi arasında büyük bi'",
            "🎶 (Fark var) Benimle senin aranda kocaman bi'",
            "🎵 (Fark var) Kötüyle benim aramda irice bi'",
            "🎶 (Fark var) İyiyle kötü arasında duran",
            "🎵 (Fark var) Seninle iyi arasında büyük bi'",
            "🎶 (Fark var) Benimle senin aranda kocaman bi'",
            "🎵 (Fark var) Kötüyle benim aramda irice bi'",
            "🎶 (Fark var) İyiyle kötü arasında duran"
        ]
    ]

    chosen_lyrics = random.choice(lyrics_list)
    for line in chosen_lyrics:
        await ctx.send(line)

# 3 ve 4. Görüntü üretiliyor mesajı + sonra silme + klasörden silme
@bot.command(name='generate')
async def generate_image(ctx, *, prompt: str = None):
    if not prompt:
        await ctx.send("Lütfen bir açıklama girin. Örnek: `!generate uçan araba gelecekte`")
        return

    status_msg = await ctx.send("🎨 Görsel oluşturuluyor...")

    try:
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
        model_id = api.get_pipeline()
        uuid = api.generate(prompt, model_id)
        files = api.check_generation(uuid)

        image_base64 = files[0]
        image = api.decode_base64_to_image(image_base64)

        image_path = "output/generated_image.png"
        image.save(image_path)

        await status_msg.delete()  # 4. Oluşturuluyor mesajını sil
        await ctx.send(file=discord.File(image_path))

        os.remove(image_path)  # 3. Görseli dosyadan sil

    except Exception as e:
        await ctx.send(f"❌ Bir hata oluştu: {e}")

bot.run(TOKEN)
