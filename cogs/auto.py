import disnake
import motor
import json
from disnake.ext import commands

with open("config.json", "r") as file:
   grab = json.load(file)

db = motor.motor_tornado.MotorClient(grab["mongodb_url"])
category = db["ZeroOn1"]
cluster = category["redeem"]

class buttons(disnake.ui.View):
   message: disnake.Message
   def __init__(self, msg: disnake.Message):
      super().__init__(timeout = 10.0)
      self.msg = msg
      self.logs = msg.guild.get_member(533992347369865216)
   
   async def on_timeout(self):
      self.clear_items()
      await self.message.edit(view = self)
      try:
         embed = disnake.Embed(
            title = "Timed Out!",
            description = f"{self.msg.author} didn't click on the buttons\n[CLICK HERE TO SEE THE MESSAGE]({self.msg.jump_url})",
            color = disnake.Color.red()
         )
         await self.logs.send(embed = embed)
      except Exception:
         pass
      
   @disnake.ui.button(label = "Offline", style = disnake.ButtonStyle.grey, custom_id = "offline")
   async def offline(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      if self.msg.author.id != inter.author.id:
         await inter.send("It's not your thread", ephemeral=True)
         return
      em = disnake.Embed(
         title = "Offline", 
         description ="The bot goes offline when there is a hosting problem or a bug. Always check the channel <#849985663596232735>",
         color = disnake.Color.green())
      em.set_footer(text="Don't forget to close this ticket!")
      await inter.send(embed = em)
   
   @disnake.ui.button(label="Something Else", style= disnake.ButtonStyle.grey, custom_id = "something")
   async def something(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      if self.msg.author.id != inter.author.id:
         await inter.send("It's not your thread", ephemeral=True)
         return
      em = disnake.Embed(
         title = "Something Else", 
         description ="We already have a <#929359181264334858> channel make sure to check it, if it didn't help then you gotta ping <@&849785786974339112>!",
         color = disnake.Color.green())
      em.set_footer(text="Don't forget to close this ticket!")
      await inter.send(embed = em)
   
   @disnake.ui.button(label = "Got it", style = disnake.ButtonStyle.red, custom_id = "close")
   async def close(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      if inter.author.id == inter.guild.owner.id or 533992347369865216:
         pass 
      elif self.msg.author.id != inter.author.id:
         await inter.send("It's not your thread", ephemeral=True)
         return
      
      self.clear_items()
   
      await inter.response.edit_message(view = self)
      await inter.channel.edit(
         locked = True,
         archived = True,
         reason = "They closed their thread"
      )
      self.stop()
      try:
         emb = disnake.Embed(
            title = "Closed",
            description = f"{self.msg.author} Closed their thread\n[CLICK HERE TO SEE THE MESSAGE]({self.msg.jump_url})",
            color = disnake.Color.green()
         )
         await self.logs.send(embed = emb)
      except Exception:
         pass
      
      
class events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
      vote_id: int =  924045541623627836
      support_id: int = 945280157084696616
       
      if message.channel.id == vote_id:
         user = self.bot.get_user(int(message.content)) or await self.bot.fetch_user(int(message.content))                
         channel = self.bot.get_channel(964961393604460545)                                     
         check = await cluster.find_one({"_id" : int(message.content)})
          
         if check is None:
            data = {
             "_id" : int(message.content),
             "votes" : 1
            }
            vote = int(data["votes"])
            await cluster.insert_one(data)
            em = disnake.Embed(color = 0x1e83d4)
            em.set_author(name=f"{f'{user.name}' if user is not None else 'Not found'}",icon_url=f"{f'{user.avatar.url}' if user is not None else 'Not found'}")
            em.add_field(name=f"Votes count : {abs(int(vote))}",value="They just voted for Bumper !!!")
            await channel.send(embed=em)
          
         else:
            votes = int(check["votes"]) + 1 
            await cluster.update_one({"_id" : int(message.content)},{"$set" : {"votes" : votes}})
            user = self.bot.get_user(int(message.content)) or self.bot.fetch_user(int(message.content))
            em = disnake.Embed(color = 0x1e83d4)
            em.set_author(name=f"{f'{user.name}' if user is not None else 'Not found'}",icon_url=f"{f'{user.avatar.url}' if user is not None else 'Not found'}")
            em.add_field(name=f"Votes count : {abs(int(votes))}",value="They just voted for Bumper !!!")
            await channel.send(embed=em)
      
      if message.channel.id == support_id:
         if message.author.bot:
            return
         if message.author.id == 533992347369865216:
            return
         
         thread: disnake.Thread = await message.create_thread(name = f"{message.author.name}'s Ticket")
         embed = disnake.Embed(
            description= "Sometimes the slash commands don't work, it's because there are some problems. If you can't see the slash commands then you gotta wait 1h or maybe less!",
            color = disnake.Color.green()
         )
         embed.set_image(url = "https://media.discordapp.net/attachments/921134360537747457/988061231246110740/unknown.png")
         m = message
         view=buttons(m)
         view.message = await thread.send(embed = embed, view = view)
         
         
def setup(bot):
   bot.add_cog(events(bot))
