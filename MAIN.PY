import random
import time
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# Your Telegram Bot token from BotFather
BOT_TOKEN = '6440429530:AAF3bN2GIS51OjBpPXJfkk5LYOp9Os2crI4'

# Your supergroup invite link or ID
SUPERGROUP_LINK = 'https://t.me/MINE_352'  # Replace with your actual supergroup link or ID

# Your random messages
RANDOM_MESSAGES = [
    "GOOD MORNING, @{username}!",
]

# Command to trigger the bot
COMMAND = "/mentionall"

# Create a TelegramClient object
client = TelegramClient('bot', api_id=None, api_hash=None).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=SUPERGROUP_LINK, pattern=COMMAND))
async def handler(event):
    sender = await event.get_sender()
    if not sender.bot:  # Ignore commands from other bots
        async for member in client.iter_participants(SUPERGROUP_LINK):
            if member.username:
                # Select a random message
                random_message = random.choice(RANDOM_MESSAGES)
                
                # Replace "{username}" in the message with the member's username
                message = random_message.format(username=member.username)
                
                # Try sending the message, handle FloodWaitError
                try:
                    await client.send_message(SUPERGROUP_LINK, message)
                except FloodWaitError as e:
                    # If FloodWaitError occurs, wait for the specified duration and retry
                    wait_time = e.seconds
                    print(f"FloodWaitError: Waiting for {wait_time} seconds...")
                    time.sleep(wait_time)
                    await client.send_message(SUPERGROUP_LINK, message)

# Start the client and listen for events
print("Bot is running...")
client.run_until_disconnected()
