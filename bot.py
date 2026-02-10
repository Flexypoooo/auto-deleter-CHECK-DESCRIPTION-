import discord
from discord.ext import commands, tasks
import asyncio


TOKEN = 'YOUR_BOT_TOKEN'

CHANNEL_IDS = [
yourid,
yourid,
yourchannelid
]

class MaintenanceBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # You need 'messages' to purge them, and 'message_content' 
        # is good practice if you plan to add commands later.
        intents.messages = True 
        intents.guilds = True
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.auto_clear.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

#---EDIT-TASKS.LOOP-(HOURS=1)-TO-THE-AMOUNT-OF-HOURS-YOU-WANT-IT-TO-DELETE/WIPE-AT
    @tasks.loop(hours=1) 
    async def auto_clear(self):
        await self.wait_until_ready()
        
        print("Starting scheduled channel clear...")
        for channel_id in CHANNEL_IDS:
            try:
                channel = self.get_channel(channel_id) or await self.fetch_channel(channel_id)
                
                if isinstance(channel, discord.TextChannel):
                    deleted = await channel.purge(limit=100)
                    print(f"Cleared {len(deleted)} messages from {channel.name}")
                else:
                    print(f"ID {channel_id} is not a text channel.")
                    
            except discord.NotFound:
                print(f"Channel {channel_id} not found.")
            except discord.Forbidden:
                print(f"Missing permissions to purge channel {channel_id}.")
            except Exception as e:
                print(f"Error in {channel_id}: {e}")

bot = MaintenanceBot()
bot.run(TOKEN)
