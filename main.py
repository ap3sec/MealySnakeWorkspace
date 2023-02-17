import discord
from discord import app_commands
from alive import alive
import os
import requests

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=1065132267636269077))
            self.synced = True
        print(f"logged in as {self.user}")

client = aclient()
tree = app_commands.CommandTree(client)

# Command section
@tree.command(guild=discord.Object(id=1065132267636269077), name='friendcheck', description='Check if a certain player is on a player\'s friend list')
async def friendcheck(interaction: discord.Interaction, checking: str, looking4: str):
    try:
        url = f"https://api.roblox.com/users/get-by-username?username={checking}"
        response = requests.get(url)
        data = response.json()
        if 'Id' in data:
            checking_id = data['Id']
            looking4_name = looking4.lower()
            url = f"https://friends.roblox.com/v1/users/{checking_id}/friends"
            response = requests.get(url)
            data = response.json()
            for friend in data['data']:
                if friend['name'].lower() == looking4_name:
                    await interaction.response.send_message(f"{looking4} is on the friends list of {checking}.")
                    break
            else:
                await interaction.response.send_message(f"{looking4} is not on the friends list of {checking}.")
        else:
            await interaction.response.send_message("Invalid player username. Please enter a valid username for the first player.")
    except:
        await interaction.response.send_message("An error occurred while processing the request.")

@tree.command(guild=discord.Object(id=1065132267636269077), name='groupcheck', description='Check if a player is a member of a certain group')
async def groupcheck(interaction: discord.Interaction, username: str, group_id: int):
    try:
        url = f"https://api.roblox.com/users/get-by-username?username={username}"
        response = requests.get(url)
        data = response.json()
        if 'Id' in data:
            user_id = data['Id']
            url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
            response = requests.get(url)
            data = response.json()
            for group in data['data']:
                if group['group']['id'] == group_id:
                    group_name = group['group']['name']
                    await interaction.response.send_message(f"{username} is a member of {group_name} ({group_id}).")
                    break
            else:
                await interaction.response.send_message(f"{username} is not a member of {group_name}.")
        else:
            await interaction.response.send_message("Invalid player username. Please enter a valid username.")
    except:
        await interaction.response.send_message("An error occurred while processing the request.")
@tree.command(guild = discord.Object(id=1065132267636269077), name='listgroups', description='lists all groups some1 is in')
async def listgroups(interaction: discord.Interaction, username: str):
    try:
        url = f"https://api.roblox.com/users/get-by-username?username={username}"
        response = requests.get(url)
        data = response.json()
        if 'Id' in data:
            user_id = data['Id']
            url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
            response = requests.get(url)
            data = response.json()
            group_info = []
            for group in data['data']:
                group_id = group['group']['id']
                group_name = group['group']['name']
                group_url = f"https://www.roblox.com/groups/{group_id}"
                group_name_hyperlink = f"[{group_name}]({group_url})"
                group_rank = group['role']['name']
                group_info.append(f"{group_name_hyperlink}\n{group_rank}")
            if group_info:
                group_list = '\n\n'.join(group_info)
                embed = discord.Embed(title=f"{username} is in the following groups:", description=group_list, color=0x00ff00)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{username} is not in any groups.")
        else:
            await interaction.response.send_message("Invalid player username. Please enter a valid username.")
    except:
        await interaction.response.send_message("An error occurred while processing the request.")

        
# Run the bot
alive()
client.run(os.environ['token'])
