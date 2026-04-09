import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ulaanbaatar timezone
UB_TZ = pytz.timezone("Asia/Ulaanbaatar")

# Target date in Ulaanbaatar time
TARGET_DATE = UB_TZ.localize(datetime(2026, 7, 3, 0, 0, 0))

# Relationship start date (for progress bar)
START_DATE = UB_TZ.localize(datetime(2025, 7, 3, 0, 0, 0))

HOURGLASS_FRAMES = ["⏳", "⌛"]
frame_index = 0
active_message = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def countdown(ctx):
    global active_message

    # Stop old animation if running
    if animate_countdown.is_running():
        animate_countdown.cancel()

    # --- EMBED WITH COUPLE PHOTO ---
    embed = discord.Embed(
        title="💖 Бид хоёрын үерхсэний албан ёсны нэг жилийн ой 💖",
        description="✨ Бид хоёрын маань онцгой өдөр ирэх тусам ойртсоор... ✨",
        color=discord.Color.pink()
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/1418660838473990214/1491505401718505775/us.jpg?ex=69d7f026&is=69d69ea6&hm=d60a68b4fc0ddf1ce38368a37d99b861ae8159604b5d350121806959cce59e2c&")

    await ctx.send(embed=embed)

    # Start animated countdown message
    active_message = await ctx.send("⏳ Countdown starting...")
    animate_countdown.start()


@tasks.loop(seconds=1)
async def animate_countdown():
    global frame_index, active_message

    if active_message is None:
        return

    now = datetime.now(UB_TZ)
    remaining = TARGET_DATE - now

    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    seconds = remaining.seconds % 60

    # Hourglass animation frame
    frame = HOURGLASS_FRAMES[frame_index]
    frame_index = (frame_index + 1) % len(HOURGLASS_FRAMES)

    # --- LOOPING DOWNLOAD-STYLE PROGRESS BAR ---
    # This bar fills from 0 → 10 blocks, then resets and repeats
    animate_progress = int((now.second % 10))  # cycles 0–9
    filled_blocks = animate_progress
    empty_blocks = 10 - filled_blocks

    progress_bar = "🩷" * filled_blocks + "🤍" * empty_blocks

    # --- EDIT MESSAGE ---
    await active_message.edit(
        content=(
            f"{frame} **Бид хоёрын үерхсэний албан ёсны нэг жилийн ой ❤️** {frame}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💖 *Бидний онцгой өдөр ойртсоор…* 💖\n\n"
            f"✨ **2026 оны 7-р сарын 3 хүртэл үлдсэн хугацаа:** ✨\n"
            f"🌸 **{days} өдөр**\n"
            f"🌙 **{hours} цаг**\n"
            f"💗 **{minutes} минут**\n"
            f"💕 **{seconds} секунд үлдлээ!**\n\n"
            f"📥 **(Loading):**\n"
            f"{progress_bar}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"❤️ *Хайртайгаа өнгөрүүлэх дараагийн жил бүр илүү сайхан байх болно…* ❤️"
        )
    )

# ⛔ ADD YOUR TOKEN HERE
import os
bot.run(os.getenv("DISCORD_TOKEN"))



