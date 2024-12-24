from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import requests
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, OMDB_API_KEY

bot = Client("imdb_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_mention = message.from_user.mention
    bot_name = (await bot.get_me()).first_name
    welcome_text = (
        f"Sᴀʟᴜᴛ🖐  {user_mention},\n"
        f"Mᴏɴ Nᴏᴍ ᴇsᴛ {bot_name}, Jᴇ ᴘᴇᴜx ᴛᴇ ғᴏᴜʀɴɪʀ ᴅᴇs ғɪʟᴍs, ᴅᴇs sᴇ‌ʀɪᴇs αɳιɱҽʂ﹐ "
        f"ɪʟ sᴜғғɪᴛ ᴊᴜsᴛᴇ ᴅᴇ ʀᴇᴊᴏɪɴᴅʀᴇ ᴍᴇs ᴄᴀɴᴀᴜx ᴇᴛ ᴅᴇ ᴘʀᴏғɪᴛᴇʀ 😍"
    )
    image_url = "https://envs.sh/JSU.jpg"
    buttons = [
        [InlineKeyboardButton("❄️About", callback_data="about"), InlineKeyboardButton("😋À propos", callback_data="commands")],
        [InlineKeyboardButton("AntiFlix", url="https://t.me/AntiFlix_A"), InlineKeyboardButton("αɳιɱҽ ƈɾσɯ", url="https://t.me/Anime_Crow")]
    ]
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@bot.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query):
    bot_name = (await bot.get_me()).mention
    about_text = (
        "╭───────────⍟\n"
        f"• ᴍʏ ɴᴀᴍᴇ : {bot_name}\n"
        f"• ᴘʀᴏɢʀᴀᴍᴇʀ : [🇰ιηg¢єу](https://kingcey.t.me)\n"
        f"• ɴᴇᴛᴡᴏʀᴋ : [ANITFLIX](https://t.me/AntiFlix_A)\n"
        f"• ᴄʜᴀᴛ ɢʀᴏᴜᴘ : [SUPPORT](https://t.me/Antiflix_d)\n"
        f"• ᴍʏ ᴏᴡɴᴇʀ / ᴅᴇᴠᴇʟᴏᴘᴇʀ : [🇰ιηg¢єу](https://kingcey.t.me)\n"
        "╰───────────────⍟"
    )
    await callback_query.message.delete()
    await bot.send_message(chat_id=callback_query.message.chat.id, text=about_text, disable_web_page_preview=True)

@bot.on_callback_query(filters.regex("commands"))
async def commands_callback(client, callback_query):
    bot_name = (await bot.get_me()).first_name
    commands_text = (
        "**_Voici mes commandes_**\n"
        "        ────────────────\n\n"
        "•> **/imdb [films, séries, animés] tapez /imdb suivi du nom de votre animes, films, ou séries.**\n"
        "•> **juste pour le contact, @kingcey et @aniflix_official vos animes et films ici**\n\n"
        "╭───[🔅ANTIFLIX🔅]────⍟\n"
        "│\n"
        f"├🔸🤖 Moɴ ɴoм: {bot_name}\n"
        "│\n"
        "├🔸📝 Lαɴɢυαɢe: **Ƥутнση3**\n"
        "│\n"
        "├🔹📚 Bιвlιoтнe‌qυe: **[Pчrogrαm](pyrogram.org)**\n"
        "│\n"
        "├🔹📡 He‌вerɢe‌ ѕυr: **[ANTIFLIX](https://t.me/AntiFlix_A)**\n"
        "│\n"
        "├🔸👨‍💻 De‌veloppeυr: **[🇰ιηg¢єу](https://kingcey.t.me)**\n"
        "│\n"
        "├🔸🔔 Mα Cнαι‌ɴe: **[AntiFlix Actu](https://t.me/AntiFlix_Actu)**\n"
        "│\n"
        "╰─────────[ 😎 ]────────⍟"
    )
    await callback_query.message.delete()
    await bot.send_message(chat_id=callback_query.message.chat.id, text=commands_text, disable_web_page_preview=True)

@bot.on_message(filters.command("imdb") & filters.private)
async def imdb_search(client, message):
    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply("❌ Veuillez fournir un mot-clé après la commande `/imdb`.")
        return
    keyword = query[1]
    url = f"http://www.omdbapi.com/?s={keyword}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "False":
        await message.reply("❌ Aucune requête trouvée pour votre mot-clé.")
        return
    buttons = []
    for result in data.get("Search", []):
        buttons.append(
            [InlineKeyboardButton(result.get("Title"), callback_data=f"imdb_{result.get('imdbID')}")]
        )
    await message.reply(
        f"🔍 Résultats trouvés pour `{keyword}` :",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@bot.on_callback_query(filters.regex(r"^imdb_"))
async def imdb_details(client, callback_query):
    imdb_id = callback_query.data.split("_")[1]
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "False":
        await callback_query.message.edit("❌ Impossible d'obtenir les détails de cette requête.")
        return
    title = data.get("Title", "N/A")
    genre = data.get("Genre", "N/A")
    rating = data.get("imdbRating", "N/A")
    year = data.get("Released", "N/A")
    plot = data.get("Plot", "N/A")
    types = data.get("Type", "N/A")
    poster = data.get("Poster", None)
    if poster and poster != "N/A":
        poster = poster.replace("SX300", "UX600")
    caption = (
        f"**🔖 Tɪᴛʀᴇ :** {title}\n"
        f"**🎭 Gᴇɴʀᴇ :** {genre}\n"
        f"**🎖 Nᴏᴛᴀᴛɪᴏɴ :** {rating} / 10\n"
        f"**📆 Aɴɴᴇ‌ᴇ :** {year}\n"
        f"**𝚃𝚈𝙿𝙴𝚂 :** {types}\n\n"
        f"**Synopsis :** 👇👇👇\n{plot}"
    )
    if poster and poster != "N/A":
        await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=poster,
            caption=caption,
        )
    else:
        await callback_query.message.edit(caption)

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast(client, message):
    admin_id = YOUR_ADMIN_ID
    if message.from_user.id != admin_id:
        await message.reply("❌ Vous n'êtes pas autorisé à utiliser cette commande.")
        return
    if not message.reply_to_message:
        await message.reply("❌ Répondez à un message pour le diffuser.")
        return
    try:
        with open("users.txt", "r") as file:
            user_ids = file.readlines()
            user_ids = [int(user.strip()) for user in user_ids]
    except FileNotFoundError:
        await message.reply("❌ Aucun utilisateur trouvé.")
        return
    await message.reply(f"🔄 Diffusion en cours à {len(user_ids)} utilisateurs...")
    successful = 0
    failed = 0
    for user_id in user_ids:
        try:
            await message.reply_to_message.copy(chat_id=user_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1
    await message.reply(f"✅ Diffusion terminée.\n• Réussie : {successful}\n• Échouée : {failed}")

@bot.on_message(filters.private & ~filters.service)
async def save_user(client, message):
    user_id = message.from_user.id
    try:
        with open("users.txt", "r") as file:
            user_ids = file.readlines()
            user_ids = [int(user.strip()) for user in user_ids]
    except FileNotFoundError:
        user_ids = []
    if user_id not in user_ids:
        user_ids.append(user_id)
        with open("users.txt", "w") as file:
            for uid in user_ids:
                file.write(f"{uid}\n")

bot.run()