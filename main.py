import cleverbotfree
import discord
import time

with open("hidden.txt") as file:
    TOKEN = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

print(f"Token = {TOKEN}")

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name == "chatbot":
        bot = ""
        i = 0
        limit = 5
        while bot == "" and i < limit:
            async with cleverbotfree.async_playwright() as p_w:
                i += 1
                if i > 1:
                    time.sleep(0.3)
                c_b = await cleverbotfree.CleverbotAsync(p_w)
                bot = await c_b.single_exchange(user_message)
                await c_b.close()
        if bot != "":
            print(f"[TOOK {i} TRIES]")
            await message.reply(bot)
        else:
            print("NO RESPONSE!!!!")
            await message.reply(f"**TRIED {limit} TIMES TO GET RESPONSE. FAILED. PLEASE RESEND MESSAGE!**")
        return

client.run(TOKEN)