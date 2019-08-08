from discord import Client as DiscordClient
from aiohttp import ClientSession as HTTPClientSession
from os import environ

DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
SEA_TOKEN = environ.get('SEA_TOKEN')

client = DiscordClient()
async def send(message: str):
    async with HTTPClientSession(headers={'Authorization': 'Bearer {}'.format(SEA_TOKEN)}) as session:
        await session.post(url='https://c.linkage.community/api/v1/posts',
            json={
                'text': message
            })


async def join_member(member_name, channel):
    await send('[{}] {} was joined.'.format(channel, member_name))
async def leave_member(member_name, channel):
    await send('[{}] {} was left.'.format(channel, member_name))
async def move_member(member_name, before_channel, after_channel):
    await send('[{}] {} was moved from {}.'.format(after_channel, member_name, before_channel))

async def handle_channel_change(member, before_channel, after_channel):
    # block any case without changing channel
    if before_channel == after_channel:
        return

    member_name = member.nick or str(member)

    if before_channel is None:
        await join_member(member_name, after_channel)
        return
    if after_channel is None:
        await leave_member(member_name, before_channel)
        return
    await move_member(member_name, before_channel, after_channel)

@client.event
async def on_voice_state_update(member, before, after):
    await handle_channel_change(member, before.channel, after.channel)

client.run(DISCORD_TOKEN)
