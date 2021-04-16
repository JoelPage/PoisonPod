import pp.external.xml.Utils as xmlUtils

import pp.core.user as ppUser
import pp.core.utils as ppUtils

class UserManager():
    def __init__(self):
        self.m_hosts = []
        self.m_users = []
        self.m_xmlFilePath = "data/user_manager.xml"
        self.Load()

    def Load(self):
        try:
            print("LoadStarted")
            xmlTree = xmlUtils.fileRead(self.m_xmlFilePath)
            self.CreateHostsFromRoot(xmlTree.getroot())
            self.CreateUsersFromRoot(xmlTree.getroot())
            print("LoadComplete")
        except:
            print("LoadFailed")

    def Save(self):
        root = xmlUtils.create_tree_root('root')
        xmlUtils.create_node(root, 'hosts')
        for host in self.m_hosts:
            host.Serialise(root)
        xmlUtils.create_node(root, 'users')
        for user in self.m_users:
            user.Serialise(root)

        xmlUtils.fileWrite(root, self.m_xmlFilePath)

    def CreateHostsFromRoot(self, root):
        print("Finding Hosts Node")
        for hostsNode in root.findall("hosts"):
            print("Finding Host Nodes")
            for hostNode in hostsNode.findall("host"):
                print("Creating New Host")
                newHost = ppUser.Host("Awaiting Deserialisation", 0)
                newHost.Deserialise(hostNode)
                print(f"Loaded Host {newHost.m_tName}")
                self.m_hosts.append(newHost)

    def CreateUsersFromRoot(self, root):
        self.m_users.clear()
        for usersNode in root.findall("users"):
            for userNode in usersNode.findall("user"):
                newUser = ppUser.User("Awaiting Deserialisation", 0)
                newUser.Deserialise(userNode)
                print(f"Loaded User {newUser.m_tName}")
                self.m_users.append(newUser)

    def GetHosts(self):
        return self.m_hosts

    def GetUsers(self):
        return self.m_users

    def DoesDiscordIDExist(self, list, dID):
        return ppUtils.Contains(list, lambda x: x.m_dID == dID)

    def AddHost(self, dID, tName):
        if self.DoesDiscordIDExist(self.m_hosts, dID):
            return False
        else:
            host = ppUser.Host(dID, tName)
            self.AddHostInternal(host)
            self.Save()
            return True

    def AddUser(self, dID, tName):
        if self.DoesDiscordIDExist(self.m_users, dID):
            return False
        else:
            user = ppUser.User(dID, tName)
            self.AddUserInternal(user)
            self.Save()
            return True

    def AddHostInternal(self, user):
        self.m_hosts.append(user)

    def AddUserInternal(self, user):
        self.m_users.append(user)

    def RemoveUserInternal(self, user):
        self.m_users.remove(user)

    def RemoveHostInternal(self, host):
        self.m_hosts.remove(host)

    def RemoveUserByDiscordID(self, dID):
        if self.DoesDiscordIDExist(self.m_users, dID):
            user = ppUtils.GetElement(self.m_users, lambda x: x.m_dID == dID)
            self.RemoveUserInternal(user)
            self.Save()
            return True
        else:
            return False

    def RemoveHostByDiscordID(self, dID):
        if self.DoesDiscordIDExist(self.m_hosts, dID):
            host = ppUtils.GetElement(self.m_hosts, lambda x: x.m_dID == dID)
            self.RemoveHostInternal(host)
            self.Save()
            return True
        else:
            return False

    def FindUserByID(self, dID):
        if self.DoesDiscordIDExist(self.m_users, dID):
            return ppUtils.GetElement(self.m_users, lambda x: x.m_dID == dID)
        else:
            return None