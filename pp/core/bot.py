import pp.external.twitch.Utils as tUtils
import pp.external.discord.Utils as dUtils
import pp.external.python.Utils as pUtils
import pp.external.log.Utils as lUtils

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
            lUtils.info(f'{self.m_dBot.user.name} has connected to Discord!')
            self.m_dBot.loop.create_task(self.Start_Async())

    def InitialiseCommands(self):

        # Permission Roles
        roles = ['Moderators']

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def version(ctx, *args):
            lUtils.info("!version")
            await ctx.send("Poison Pod Bot v0.0.2\nhttps://github.com/JoelPage/PoisonPod")

        @self.m_dBot.command()
        async def whoslive(ctx, *args):
            lUtils.info("!whoslive")
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
        async def setonlineemoji(ctx, *args):
            lUtils.info("!setonlineemoji")

            emoji = args[0]
            self.m_settings.m_onlineEmoji = emoji
            self.m_settings.Save()

            await ctx.send(f"Online Emoji set to {self.m_settings.m_onlineEmoji}")
            
        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setofflineemoji(ctx, *args):
            lUtils.info("!setofflineemoji")

            emoji = args[0]
            self.m_settings.m_offlineEmoji = emoji
            self.m_settings.Save()

            await ctx.send(f"Offline Emoji set to {self.m_settings.m_offlineEmoji}")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def addhost(ctx, *args):
            lUtils.info("!addhost")
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
            lUtils.info("!removehost")
            dID = args[0]
            success = self.m_userManager.RemoveHostByDiscordID(dID)
            if success:
                await ctx.send(f"Host {dID} succesfully removed.")
            else:
                await ctx.send(f"Host {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def adduser(ctx, *args):
            lUtils.info("!adduser")
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
            lUtils.info("!removeuser")
            dID = args[0]
            success = self.m_userManager.RemoveUserByDiscordID(dID)
            if success:
                await ctx.send(f"User {dID} succesfully removed.")
            else:
                await ctx.send(f"User {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def hosts(ctx, *args):
            lUtils.info("!hosts")
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
            lUtils.info("!users")
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
            lUtils.info("!channel")
            await ctx.send(f"The output channel is set to <#{self.m_settings.GetChannelID()}>")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def hostchannel(ctx, *args):
            lUtils.info("!hostchannel")
            await ctx.send(f"The host output channel is set to <#{self.m_settings.GetHostChannelID()}>")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setchannel(ctx, *args):
            lUtils.info("!setchannel")

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
            lUtils.info("!sethostchannel")

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
            lUtils.info("!announceuser")

            dID = args[0]

            lUtils.info(f"########## Announce User Called with ID : {dID} ##########")

            user = self.m_userManager.FindUserByID(dID)
            if user:

                try: 
                    token = tUtils.getOAuthToken()

                    if token == 0:
                        result = "Failed to get auth token"
                        await ctx.send(result)

                    userChannelID = self.m_settings.GetChannelID()
                    await self.PostGoLiveEmbed_Async(user, userChannelID, False, token, force=True)

                except Exception as e:
                    result = "An error occured: " + str(e)
                    lUtils.debug(f"########## return {result} ##########")



            else:
                await ctx.send(f"User could not be found.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def announcehost(ctx, *args):
            lUtils.info("!announcehost")

            dID = args[0]

            host = self.m_userManager.FindHostByID(dID)
            if host:

                try: 
                    token = tUtils.getOAuthToken()

                    if token == 0:
                        result = "Failed to get auth token"
                        await ctx.send(result)

                        hostChannelID = self.m_settings.GetHostChannelID()
                        await self.PostGoLiveEmbed_Async(host, hostChannelID, True, token, force=True)

                except Exception as e:
                    result = "An error occured: " + str(e)
                    lUtils.debug(f"########## return {result} ##########")

            else:
                await ctx.send(f"Host could not be found.")

    def Run(self):
        lUtils.info("Retrieving token!")
        token = pUtils.getEnvVar("DISCORD_TOKEN")
        lUtils.info("Connecting bot to discord...")
        self.m_dBot.run(token)
        lUtils.info("Finished running bot!")

    def SaveUserData(self):
        self.m_userManager.Save()

    async def Start_Async(self):
        interval = 30
        await self.m_dBot.wait_until_ready()
        while True:
            await pUtils.sleep_async(interval)

            try: 
                token = tUtils.getOAuthToken()

                if token == 0:
                    result = "Failed to get auth token"
                    continue

                hostChannelID = self.m_settings.GetHostChannelID()
                userChannelID = self.m_settings.GetChannelID()
                hosts = self.m_userManager.GetHosts()
                users = self.m_userManager.GetUsers()

                for host in hosts:
                    await self.PostGoLiveEmbed_Async(host, hostChannelID, True, token)

                for user in users:
                    await self.PostGoLiveEmbed_Async(user, userChannelID, False, token)

                self.SaveUserData()

            except Exception as e:
                result = "An error occured: " + str(e)
                lUtils.info(f"########## return {result} ##########")
                continue

    async def PostMessage_Async(self, channelID, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message)
        else:
            lUtils.info(f"Failed to send message, channel with ID '{channelID}' could not be found.")

    async def PostEmbed_Async(self, channelID, embed, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message, embed=embed)
        else:
            lUtils.info(f"Failed to send embed, channel with ID '{channelID}' could not be found.")

    async def PostGoLiveEmbed_Async(self, user, channelID, shouldTag, token, force=False):
        dID = user.m_dID
        name = user.m_tName
        wasLive = user.m_isLive

        lUtils.info(f"name : {name}")

        try:
            streamData = tUtils.checkIfLive(name, token)['data']
            channelData = tUtils.getChannelData(name, token)['data']
        except Exception as e:
            result = "An error occured: " + str(e)
            lUtils.info(f"########## return {result} ##########")
            return

        if streamData is None or channelData is None:
            lUtils.info(f"no streamData or channelData")
            user.SetIsLive(False)
            return

        if len(streamData) <= 0:
            lUtils.info("streamData length <= 0")
            user.SetIsLive(False)
            return

        if not wasLive or force:
            if user.ShouldNotify() or force:
                
                title = streamData[0]['title'] #could crash if no exist.
                logo = channelData[0]['profile_image_url']
                #description = channelData[0]['description']
                gameName = streamData[0]['game_name']

                tUrl = f"https://www.twitch.tv/{name}"
                # Get title of stream
                dEmbed = dUtils.CreateEmbed(title, "")
                dEmbed.url = tUrl
                dEmbed.set_thumbnail(url=logo)
                dEmbed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-1920x1080.jpg/?={pUtils.utcnowtimestamp()}")

                dEmbed.timestamp = pUtils.utcnow()
                dEmbed.set_footer(text="ppbot")

                dEmbed.add_field(name="Streaming", value=gameName)

                message = f"{dID} went live! Check them out at {tUrl}"

                if shouldTag:
                    #dEmbed.add_field(name="Game", value=game, inline=False)
                    message = f"Hey @everyone, {dID} is now live! Come and join us on {tUrl}"

                await self.PostEmbed_Async(channelID, embed=dEmbed, message=message)

        user.SetIsLive(True)
        