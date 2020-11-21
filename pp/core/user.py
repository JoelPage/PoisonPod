import pp.external.python.Utils as pUtils
import pp.external.xml.Utils as xmlUtils

class User():
    def __init__(self, dID, tName):
        print("User __init__")
        self.m_dID = dID 
        self.m_tName = tName
        self.m_isLive = False
        self.m_wasLastLiveTimestamp = 1

    def Deserialise(self, node):
        self.m_dID = xmlUtils.get_value_text(node, 'dID')
        self.m_tName = xmlUtils.get_value_text(node, 'tName')
        self.m_isLive = xmlUtils.get_value_bool(node, 'isLive')
        self.m_wasLastLiveTimestamp = xmlUtils.get_value_int(node, 'wasLastLiveTimestamp')

    def Serialise(self, root):
        usersNode = root.find('users')
        userNode = xmlUtils.create_node(usersNode, 'user')
        xmlUtils.create_and_set_node_text_if_exists(userNode, 'dID', self.m_dID)
        xmlUtils.create_and_set_node_text_if_exists(userNode, 'tName', self.m_tName)
        xmlUtils.create_and_set_node_text_bool(userNode, 'isLive', self.m_isLive)
        xmlUtils.create_and_set_node_text_int_if_exists(userNode, 'wasLastLiveTimestamp', self.m_wasLastLiveTimestamp)

    def SetIsLive(self, isLive):
        if isLive:
            self.m_isLive = True
            self.m_wasLastLiveTimestamp = pUtils.utcnowtimestamp()
        else:
            self.m_isLive = False
        
    def ShouldNotify(self):
        print(pUtils.utcnowtimestamp())
        print(self.m_wasLastLiveTimestamp)
        timeSinceLastLive = pUtils.utcnowtimestamp() - self.m_wasLastLiveTimestamp
        return (timeSinceLastLive > 600) 