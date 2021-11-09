import asyncio
import os

import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Vocal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member : nextcord.Member, before, after):
        if before.channel is None and after.channel is not None:
            
            try:
                while True:
                    if after.afk:
                        return
                    
                    await asyncio.sleep(config['time_for_xp'])
                    
                    if after.channel is None:
                        return
                    
                    guild = member.guild
                    stats = levelling.find_one({"guildid": guild.id, "id": member.id})
                    xp = stats['xp']
                    levelling.update_one({"guildid": guild.id, "id": member.id}, {"$set": {"xp": xp + config['xp_per_time']}})

            except Exception as e:
                print(e)


# Sets-up the cog for Profile+
def setup(client):
    client.add_cog(Vocal(client))