import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
moderation_enabled = False
BAD_WORDS = {
    "хуй", "хуя", "хуем", "хуёвый", "хуеплет", "хуесос", "хуила", "хуист", "хуйню", "хуйней", "хуёв", "хуякс",
    "пизда", "пизды", "пиздец", "пиздить", "пизданутый", "пиздюк", "пиздючка", "пиздячить", "пиздёныш",
    "ебать", "ебал", "ебало", "ебаный", "ебанутый", "ебашить", "ебло", "ебливый", "ебучий", "ебучка",
    "сука", "суки", "сукин", "сучка", "сучий", "сучонок", "сучье", "сучьи",
    "блядь", "бляди", "блядовать", "блядский", "блядун", "бляха", "бляха-муха",
    "гандон", "гандонище", "гандоны", "гандончик",
    "мразь", "мразота", "мразишка", "мразота",
    "долбоёб", "долбаёб", "долбанутый", "долбодятел", "долбить", "долбищик",
    "еблан", "ебливый", "ебланчик", "ебланутый",
    "пидор", "пидорас", "пидоры", "пидорок", "пидрила", "пидрёнок",
    "чмо", "чмошник", "чмошный",
    "шлюха", "шлюшки", "шлюхан", "шлюхенок",
    "говно", "говнистый", "говнюк", "говнодав", "говноед", "говняшка",
    "дерьмо", "дерьмище", "дерьмовый",
    "залупа", "залупный", "залупить", "залупаться", "залупленый",
    "жопа", "жопный", "жопастый", "жопень", "жопошник",
    "дрочить", "дрочило", "дрочёный", "дрочун", "дрочер",
    "сперма", "спермотоксикоз", "спермовозка",
    "мандa", "мандовошка", "мандить", "мандёж", "мандюкать",
    "нахуй", "нахуя", "нахер", "нахрен", "нах",
    "пошёл", "пошла", "пошли", "пошёл ты", "иди нахуй", "иди в жопу",
    "срать", "срущий", "насрать", "насрано", "насранный",
    "трахать", "трахан", "траханный", "трахатель", "трахаться"
}  # Добавлены почти все маты и их формы

GIF_URL = "https://s6.gifyu.com/images/bz4wb.gif"

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Бот {bot.user} запущен и команды синхронизированы!')

@bot.tree.command(name="boton", description="Включает бота")
async def boton(interaction: discord.Interaction):
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ Этот бот работает только в разрешённом канале!", ephemeral=True)
        return
    global moderation_enabled
    moderation_enabled = True
    await interaction.response.send_message("✅ Модерация включена!")

@bot.tree.command(name="botoff", description="Выключает бота")
async def botoff(interaction: discord.Interaction):
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ Этот бот работает только в разрешённом канале!", ephemeral=True)
        return
    global moderation_enabled
    moderation_enabled = False
    await interaction.response.send_message("❌ Модерация выключена!")

@bot.event
async def on_message(message):
    global moderation_enabled
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return
    if moderation_enabled and message.author != bot.user:
        if any(bad_word in message.content.lower() for bad_word in BAD_WORDS):
            await message.reply(GIF_URL)
    await bot.process_commands(message)

bot.run(TOKEN)
