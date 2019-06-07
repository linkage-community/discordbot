from discord import Client as DiscordClient
from aiohttp import ClientSession as HTTPClientSession
from os import environ

DISCORD_TOKEN = environ.DISCORD_TOKEN
SEA_TOKEN = environ.SEA_TOKEN

client = DiscordClient()
async def send(message: str):
    async with HTTPClientSession(headers={'Authorization': 'Bearer {}'.format(SEA_TOKEN)}) as session:
        await session.post(url='https://c.linkage.community/api/v1/posts',
            json={
                'text': message
            })


async def join_member(member, channel):
    await send('[{}] {} was joined.'.format(channel, member))

async def leave_member(member, channel):
    await send('[{}] {} was left.'.format(channel, member))

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        await join_member(member, after.channel)
        return
    if after.channel is None:
        await leave_member(member, before.channel)
        return

client.run(DISCORD_TOKEN)
