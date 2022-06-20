import disnake
import json
from disnake.ext import commands

with open("config.json", "r") as f:
  get = json.load(f)

prefix = get["prefix"]
token = get["token"]
status = get["customstatus"]

class Helper(commands.Bot):
  class select_roles(disnake.ui.View):
    def __init__(self, bot):
      super().__init__(timeout = None)
      self.bot = bot
      
    @disnake.ui.button(style = disnake.ButtonStyle.blurple, label = "Server Updates", custom_id = "persistent_view:red")
    async def red(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      role = disnake.utils.get(inter.guild.roles, id = 952594434489483404)
      roles = [r.id for r in inter.author.roles]
      if role.id in roles:
        await inter.author.remove_roles(role)
        await inter.send(f"{role.mention} was removed from you", ephemeral = True)
      if role.id not in roles:
        await inter.author.add_roles(role)
        await inter.send(f"{role.mention} was given to you", ephemeral = True)
        
    @disnake.ui.button(style = disnake.ButtonStyle.blurple, label = "Bot Updates", custom_id = "persistent_view:green")
    async def green(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      role = disnake.utils.get(inter.guild.roles, id = 951180509696905318)
      roles = [r.id for r in inter.author.roles]
      if role.id in roles:
        await inter.author.remove_roles(role)
        await inter.send(f"{role.mention} was removed from you", ephemeral = True)
      if role.id not in roles:
        await inter.author.add_roles(role)
        await inter.send(f"{role.mention} was given to you", ephemeral = True)
  
  def __init__(self):
    super().__init__(
      command_prefix=prefix, 
      intents = disnake.Intents.all(),
      activity = disnake.Game(name = status)
    )
    self.persistent_view_added = False
      
  async def on_ready(self):
    if not self.persistent_view_added:
      self.add_view(self.select_roles(self))
      self.persistent_view_added = True
    try:
      self.load_extensions("cogs")
    except Exception:
      pass
    
if __name__ == "__main__":
  bot = Helper()
  bot.run(token)