import pp.external.xml.Utils as xmlUtils

import pp.core.user as ppUser
import pp.core.utils as ppUtils

class UserManager():
    def __init__(self):
        self.m_host = ppUser("init", 0)
        self.m_users = []
        self.m_xmlFilePath = "data/user_manager.xml"
        self.Load()

    def Load(self):
        try:
            xmlTree = xmlUtils.fileRead(self.m_xmlFilePath)
            self.CreateHostsFromRoot(xmlTree.getroot())
            self.CreateUsersFromRoot(xmlTree.getroot())
            
        except:
            pass

    def Save(self):
        root = xmlUtils.create_tree_root('root')
        xmlUtils.create_node(root, 'hosts')
        self.m_host.Serialise(root)
        xmlUtils.create_node(root, 'users')
        for user in self.m_users:
            user.Serialise(root)

        xmlUtils.fileWrite(root, self.m_xmlFilePath)

    def CreateHostsFromRoot(self, root):
        for hostsNode in root.findall("hosts"):
            for hostNode in usersNode.findall("host"):
                newHost = ppUser.Host("Awaiting Deserialisation", 0)
                newHost.Deserialise(hostNode)
                print(f"Loaded Host {newHost.m_tName}")
                self.m_host = newHost

    def CreateUsersFromRoot(self, root):
        self.m_users.clear()
        for usersNode in root.findall("users"):
            for userNode in usersNode.findall("user"):
                newUser = ppUser.User("Awaiting Deserialisation", 0)
                newUser.Deserialise(userNode)
                print(f"Loaded User {newUser.m_tName}")
                self.m_users.append(newUser)

    def GetHost(self):
        return self.m_host

    def GetUsers(self):
        return self.m_users

    def DoesDiscordIDExist(self, dID):
        return ppUtils.Contains(self.m_users, lambda x: x.m_dID == dID)

    def SetHost(self, dID, tName):
        if self.DoesDiscordIDExist(dID):
            return False
        else:
            host = ppUser.Host(dID, tName)
            self.m_host = host
            self.Save()
            return True

    def AddUser(self, dID, tName):
        if self.DoesDiscordIDExist(dID):
            return False
        else:
            user = ppUser.User(dID, tName)
            self.AddUserInternal(user)
            self.Save()
            return True

    def AddUserInternal(self, user):
        self.m_users.append(user)

    def RemoveUserInternal(self, user):
        self.m_users.remove(user)

    def RemoveUserByDiscordID(self, dID):
        if self.DoesDiscordIDExist(dID):
            user = ppUtils.GetElement(self.m_users, lambda x: x.m_dID == dID)
            self.RemoveUserInternal(user)
            self.Save()
            return True
        else:
            return False