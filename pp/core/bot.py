import pp.external.twitch.Utils as tUtils
import pp.external.discord.Utils as dUtils
import pp.external.python.Utils as pUtils

import pp.core.user_manager as ppUserManager
import pp.core.user as ppUser
import pp.core.settings as ppSettings

class Bot():
    def __init__(self):
        self.m_dBot = dUtils.CreateBot("!")
        self.m_userManager = ppUserManager.UserManager()
        self.m_settings = ppSettings.Settings()
        self.InitialiseCallbacks()
        self.InitialiseCommands()
        

    def InitialiseCallbacks(self):

        @self.m_dBot.event
        async def on_ready():
            print(f'{self.m_dBot.user.name} has connected to Discord!')
            self.m_dBot.loop.create_task(self.Start_Async())

    def InitialiseCommands(self):

        # Permission Roles
        roles = ['Moderators']

        @self.m_dBot.command()
        async def whoslive(ctx, *args):
            print("!whoslive")
            usersStr = ""
            wasLive = False 
            for host in self.m_userManager.GetHosts():
                if host.m_isLive:
                    wasLive = True
                    isLiveStr = self.m_settings.m_onlineEmoji
                    usersStr += f"{isLiveStr} (https://twitch.tv/{host.m_tName})\n"

            for user in self.m_userManager.GetUsers():
                if user.m_isLive:
                    wasLive = True
                    isLiveStr = self.m_settings.m_onlineEmoji
                    usersStr += f"{isLiveStr} (https://twitch.tv/{user.m_tName})\n"

            if wasLive == False:
                usersStr = "Nobody is live :("

            dEmbed = dUtils.CreateEmbed("Live PP Community Streamers", usersStr)
            await ctx.send(embed=dEmbed)

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def version(ctx, *args):
            print("!version")
            await ctx.send("Poison Pod Bot v0.0.2\nhttps://github.com/JoelPage/PoisonPod")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setonlineemoji(ctx, *args):
            print("!setonlineemoji")

            emoji = args[0]
            self.m_settings.m_onlineEmoji = emoji
            self.m_settings.Save()

            await ctx.send(f"Online Emoji set to {self.m_settings.m_onlineEmoji}")
            
        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setofflineemoji(ctx, *args):
            print("!setofflineemoji")

            emoji = args[0]
            self.m_settings.m_offlineEmoji = emoji
            self.m_settings.Save()

            await ctx.send(f"Offline Emoji set to {self.m_settings.m_offlineEmoji}")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def addhost(ctx, *args):
            print("!addhost")
            dID = args[0]
            tName = args[1]
            success = self.m_userManager.AddHost(dID, tName)
            if success:
                await ctx.send(f"Host {dID} was succesfully set.")
            else:
                await ctx.send(f"Host {dID} was not set, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def removehost(ctx, *args):
            print("!removehost")
            dID = args[0]
            success = self.m_userManager.RemoveHostByDiscordID(dID)
            if success:
                await ctx.send(f"Host {dID} succesfully removed.")
            else:
                await ctx.send(f"Host {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def adduser(ctx, *args):
            print("!adduser")
            try:
                dID = args[0]
                tName = args[1]
                success = self.m_userManager.AddUser(dID, tName)
                if success:
                    await ctx.send(f"User {dID} was succesfully added.")
                else:
                    await ctx.send(f"User {dID} was not added, for some reason.")
            except:
                await ctx.send(f"You dun goofed.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def removeuser(ctx, *args):
            print("!removeuser")
            dID = args[0]
            success = self.m_userManager.RemoveUserByDiscordID(dID)
            if success:
                await ctx.send(f"User {dID} succesfully removed.")
            else:
                await ctx.send(f"User {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def hosts(ctx, *args):
            print("!hosts")
            hostsStr = ""
            for host in self.m_userManager.GetHosts():
                isLiveStr = self.m_settings.m_offlineEmoji
                if host.m_isLive:
                    isLiveStr = self.m_settings.m_onlineEmoji
                hostsStr += f"{isLiveStr} {host.m_dID} ({host.m_tName})\n"
            dEmbed = dUtils.CreateEmbed("Registered Hosts", hostsStr)
            await ctx.send(embed=dEmbed)

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def users(ctx, *args):
            print("!users")
            usersStr = ""
            for user in self.m_userManager.GetUsers():
                isLiveStr = self.m_settings.m_offlineEmoji
                if user.m_isLive:
                    isLiveStr = self.m_settings.m_onlineEmoji
                usersStr += f"{isLiveStr} {user.m_dID} ({user.m_tName})\n"
            dEmbed = dUtils.CreateEmbed("Registered Users", usersStr)
            await ctx.send(embed=dEmbed)

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def channel(ctx, *args):
            print("!channel")
            await ctx.send(f"The output channel is set to <#{self.m_settings.GetChannelID()}>")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def hostchannel(ctx, *args):
            print("!hostchannel")
            await ctx.send(f"The host output channel is set to <#{self.m_settings.GetHostChannelID()}>")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setchannel(ctx, *args):
            print("!setchannel")

            channelID = args[0]

            try:
                channelID = dUtils.parse_channel(channelID)
            except:
                await ctx.send("Failed to parse channel.")
                return

            channel = self.m_dBot.get_channel(channelID)
            if channel:
                self.m_settings.m_dChannelID = channelID
                self.m_settings.Save()
                await ctx.send(f"Channel set to <#{channelID}>")
            else:
                await ctx.send(f"Channel could not be found.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def sethostchannel(ctx, *args):
            print("!sethostchannel")

            channelID = args[0]

            try:
                channelID = dUtils.parse_channel(channelID)
            except:
                await ctx.send("Failed to parse channel.")
                return

            channel = self.m_dBot.get_channel(channelID)
            if channel:
                self.m_settings.m_dHostChannelID = channelID
                self.m_settings.Save()
                await ctx.send(f"Host channel set to <#{channelID}>")
            else:
                await ctx.send(f"Channel could not be found.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def announceuser(ctx, *args):
            print("!announceuser")

            dID = args[0]

            print(f"########## Announce User Called with ID : {dID} ##########")

            user = self.m_userManager.FindUserByID(dID)
            if user:
                userChannelID = self.m_settings.GetChannelID()
                await self.PostGoLiveEmbed_Async(user, userChannelID, False, force=True)
            else:
                await ctx.send(f"User could not be found.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def announcehost(ctx, *args):
            print("!announcehost")

            dID = args[0]

            host = self.m_userManager.FindHostByID(dID)
            if host:
                hostChannelID = self.m_settings.GetHostChannelID()
                await self.PostGoLiveEmbed_Async(host, hostChannelID, True, force=True)
            else:
                await ctx.send(f"Host could not be found.")

    def Run(self):
        print("Retrieving token!")
        token = pUtils.getEnvVar("DISCORD_TOKEN")
        print("Connecting bot to discord...")
        self.m_dBot.run(token)
        print("Finished running bot!")

    def SaveUserData(self):
        self.m_userManager.Save()

    async def Start_Async(self):
        interval = 30
        await self.m_dBot.wait_until_ready()
        while True:
            hostChannelID = self.m_settings.GetHostChannelID()
            userChannelID = self.m_settings.GetChannelID()
            hosts = self.m_userManager.GetHosts()
            users = self.m_userManager.GetUsers()

            for host in hosts:
                await self.PostGoLiveEmbed_Async(host, hostChannelID, True)

            for user in users:
                await self.PostGoLiveEmbed_Async(user, userChannelID, False)

            self.SaveUserData()

            await pUtils.sleep_async(interval)
        
    async def PostMessage_Async(self, channelID, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message)
        else:
            print(f"Failed to send message, channel with ID {channelID} could not be found.")

    async def PostEmbed_Async(self, channelID, embed, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message, embed=embed)
        else:
            print(f"Failed to send embed, channel with ID {channelID} could not be found.")

    async def PostGoLiveEmbed_Async(self, user, channelID, shouldTag, force=False):
        dID = user.m_dID
        name = user.m_tName
        wasLive = user.m_isLive

        print(f"name : {name}")

        try:
            streamData = tUtils.checkIfLive(name)['data']
            channelData = tUtils.getChannelData(name)['data']
        except Exception as e:
            result = "An error occured: " + str(e)
            print(f"########## return {result} ##########")
            return

        if streamData is None or channelData is None:
            print(f"no streamData or channelData")
            user.SetIsLive(False)
            return

        if len(streamData) <= 0:
            print("streamData length <= 0")
            user.SetIsLive(False)
            return

        if not wasLive or force:
            if user.ShouldNotify() or force:
                
                title = streamData[0]['title'] #could crash if no exist.
                logo = channelData[0]['profile_image_url']
                description = channelData[0]['description']

                tUrl = f"https://www.twitch.tv/{name}"
                # Get title of stream
                dEmbed = dUtils.CreateEmbed(title, description)
                dEmbed.url = tUrl
                dEmbed.set_thumbnail(url=logo)
                dEmbed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-1920x1080.jpg")
                dEmbed.timestamp = pUtils.utcnow()
                dEmbed.set_footer(text="ppbot")
                dEmbed.set_author(name=f"{name}", icon_url=logo)

                message = f"{dID} went live! Check them out at {tUrl}"

                if shouldTag:
                    #dEmbed.add_field(name="Game", value=game, inline=False)
                    message = f"Hey @everyone, {dID} is now live! Come and join us on {tUrl}"

                await self.PostEmbed_Async(channelID, embed=dEmbed, message=message)

        user.SetIsLive(True)
        