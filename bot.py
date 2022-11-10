import unicodedata
from io import BytesIO
from typing import List
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from discord import Member, Embed, Color, File, RawMessageDeleteEvent, RawMessageUpdateEvent, Message
from discord.ext import commands

bot = commands.Bot(command_prefix=">")


ALIZEE_ID = 797314179719364619
HE = 884953733983793202
TEST_SV = 230792723471400960

extensions = []


if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    bot.remove_command("help")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")


async def send_message(*, channel, **kwargs):
    send_to = channel.guild.get_channel(HE)
    if channel.guild.id == TEST_SV:
        send_to = channel
    await send_to.send(**kwargs)


async def on_cached_message_delete(message: Message):
    if message.author.bot:
        return None

    files = []
    embed = Embed(
        title=f"{message.author.name} excluiu uma mensagem",
        description=message.content,
        color=Color.random(),
        url=message.jump_url
    )
    embed.set_thumbnail(url=message.author.avatar_url)

    if message.attachments:
        att_len = len(message.attachments)
        files = [File(BytesIO(await att.read()), filename=att.filename) for att in message.attachments]
        embed.set_footer(text=f"contem {att_len} anexo{'s' if att_len > 1 else ''}")
    await send_message(channel=message.channel, embed=embed, files=files)


@bot.event
async def on_raw_message_edit(payload: RawMessageUpdateEvent):
    before = payload.cached_message

    if before and before.author.bot:
        await bot.process_commands(before)
        return

    after = await (
        bot
        .get_guild(id=int(payload.data["guild_id"]))
        .get_channel(payload.channel_id)
        .fetch_message(payload.message_id)
    )

    if before and before.content == after.content:
        await bot.process_commands(before)
        return

    embed = Embed(
        title=f"{after.author.name} editou uma mensagem",
        color=Color.random(),
        url=after.jump_url
    )
    embed.set_thumbnail(url=after.author.avatar_url)
    embed.add_field(
        name="antiga",
        value=before.content if before else "a mensagem nao esta no meu cache, nao sei o que estava aqui",
        inline=False
    )
    embed.add_field(name="nova", value=after.content, inline=False)
    await send_message(channel=after.channel, embed=embed)


@bot.event
async def on_raw_message_delete(payload: RawMessageDeleteEvent):
    message = payload.cached_message

    if message:
        await on_cached_message_delete(message)
        return

    channel = bot.get_guild(id=payload.guild_id).get_channel(payload.channel_id)
    embed = Embed(
        title=f"uma mensagem foi deletada",
        description=f"a mensagem nao estava no meu cache 😔. sei que estava no canal `{channel.name}`",
        color=Color.random(),

    )
    await send_message(channel=channel, embed=embed)


@bot.command(aliases=["ver", "foto"])
async def avatar(ctx, member: Member):
    await ctx.send(member.avatar_url)


def normalize_word(word: str) -> str:
    return unicodedata.normalize("NFD", word).encode("ascii", "ignore").decode("utf-8")


def get_meaning_url(word: str) -> str:
    normalized_word = normalize_word(word)
    site = "https://www.dicio.com.br"
    return f"{site}/{normalized_word}"


def get_page_html(url: str) -> str:
    page = urlopen(url)
    return page.read().decode("utf-8")


def get_meaning_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [span.string for span in soup.select(".textonovo > span:not([class])") if len(span.contents) == 1]


def format_meaning_message(meanings: List[str]) -> str:
    return "\n".join([f"● {_meaning}" for _meaning in meanings])


@bot.command(aliases=["significado"])
async def meaning(ctx, word: str):
    url = get_meaning_url(word)

    try:
        html = get_page_html(url)
    except HTTPError:
        await ctx.send("nao achei")
        return

    raw_meanings = get_meaning_from_html(html)
    meanings = format_meaning_message(raw_meanings)
    await ctx.send(f"Significado de **{word}**\n\n{meanings}")


bot.run(":)")
