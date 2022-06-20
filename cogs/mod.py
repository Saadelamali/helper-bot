import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.warns = {}
      self.dangers = []
   
   @commands.command(aliases = ["Warn", "WARN"])
   @commands.guild_only()
   @commands.has_guild_permissions(administrator = True)
   async def warn(self, ctx: commands.Context, members: commands.Greedy[disnake.Member]):
      for member in members:
         if self.warns[str(member.id)] is None:
            self.warns[str(member.id)] = 1
            continue
         self.warns[str(member.id)] + 1
         if self.warns[str(member.id)] == 10:
            self.dangers.append(member.id)
      if len(self.dangers) == 0:
         pass
      elif len(self.dangers) != 0:
         r = []
         for i in self.dangers:
            user = ctx.guild.get_member(i) or await self.bot.fetch_user(i)
            if user.id in ctx.guild.members:
               r.append(f"{user.name} - {user.id}")
               await user.timeout(duration = 86400.0)
               try:
                  await user.send(f"You have been timed out for 24h in **{ctx.guild.name}** ```Reason: You have more than 10 warnings!```")
               except Exception:
                 await ctx.send(f"{user} has been timed out for 24h ```Reason: They have more than 10 warnings!```")
            else:
               del self.warns[str(user.id)]
      users = [u for u in members if u not in self.dangers]
      tmfr = '\n'.join(users)
      tmft = '\n'.join(r)
      
      em = disnake.Embed(
         title = "Results",
         color = disnake.Color.green()
      )
      em.add_field(
         name = "Warned users",
         value = f"{'Empty' if (len(users) == 0) else tmfr}"
      )
      em.add_field(
         name = "Timed out users",
         value = f"{'Empty' if (len(self.dangers) == 0) else tmft}"  
      )
      for i in range(len(self.dangers)):
         self.dangers.pop(0)

      await ctx.send(embed = em)
   
   @commands.command(aliases = ["Warnings", "WARNINGS"])
   @commands.has_guild_permissions()
   @commands.guild_only()
   async def warnings(self, ctx, member: disnake.Member):
      if self.warns[str(member.id)] is None:
         await ctx.send(f"They have 0 warning")
      else:
         await ctx.send(f"They have {self.warns[str(member.id)]} warning{'' if self.warns[str(member.id)] <= 1 else 's'}")
      
   @commands.command(aliases = ["Clear", "CLEAR"])
   @commands.guild_only()
   @commands.has_guild_permissions()
   async def clear(self, ctx, member: disnake.Member):
      if self.warns[str(member.id)] is None:
         await ctx.send("This user doesn't have warnings")
      else:
         del self.warns[str(member.id)]
         await ctx.send(f"Successfully cleared {member}'s warnings")
      

          
         
          



def setup(bot):
   bot.add_cog((bot))