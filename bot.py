from discord import Member
from discord.ext import commands

bot = commands.Bot(command_prefix='>')


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


WALLACE_ID = 205886015758401537


@bot.event
async def on_message_delete(message):
    if message.author.id in [WALLACE_ID]:
        if message.content:
            _message = 'wallace excluiu: "{}"'.format(message.content)
        else:
            _message = '\n'.join([i.proxy_url for i in message.attachments])
        await message.channel.send(_message)


@bot.command()
async def ver(ctx, member: Member):
    await ctx.send(member.avatar_url)


bot.run(':)')
