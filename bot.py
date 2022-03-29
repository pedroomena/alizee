from discord import Member, Embed, Color
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='>')


ALIZEE_ID = 797314179719364619
WALLACE_ID = 205886015758401537
ANA_ID = 202226964134756352
HE = 884953733983793202
TEST_SV = 230792723471400960

extensions = []


if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    bot.remove_command('help')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')


@bot.event
async def on_message(message):
    if message.author.id == ANA_ID and message.attachments:
        for char in ["🇭", "🇴", "🇪", "❗"]:
            # await message.add_reaction("<:puke:454771752518680587>")
            await message.add_reaction(char)

    if message.author.id == ALIZEE_ID and message.embeds and message.channel.id == HE:
        try:
            for img in message.embeds[0].description.split("imgs-")[1].split(","):
                await message.reply(img)
        except IndexError:
            pass
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return None

    attachment = None
    additional_attachments = []
    if message.attachments:
        attachment = message.attachments[0].proxy_url
        additional_attachments = ",".join([att.proxy_url for att in message.attachments[1:]])

    embed = Embed(
        title=f'{message.author.name} excluiu uma mensagem',
        description=message.content,
        color=Color.random(),
        url=message.jump_url
    )
    embed.set_thumbnail(url=message.author.avatar_url)

    if attachment:
        embed.set_image(url=attachment)
        if additional_attachments:
            embed.description = f"{embed.description}\n\nimgs-{additional_attachments}"

    send_to = message.channel.guild.get_channel(HE)
    if message.channel.guild.id == TEST_SV:
        send_to = message.channel
    await send_to.send(embed=embed)


@bot.command()
async def ver(ctx, member: Member):
    await ctx.send(member.avatar_url)


bot.run(':)')
